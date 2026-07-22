# basket_prep.py
"""
Usage:
  python basket_prep.py                 # θα ψάξει για "POS_dataset.xlsx" στο cwd
  python basket_prep.py myfile.xlsx     # ή δώσε όνομα/μονοπάτι

Το script υποθέτει ότι το Excel έχει 3 φύλλα:
 - "POS Data" (στήλες: Basket_ID, Date_, Barcode, Quantity, Value_, LoyaltyCard_ID)
 - "Loyalty" (στήλες: Cardholder, Status, LoyaltyCard_ID (προαιρετικό))
 - "Hierachy Categories & Barcodes" (στήλες: Barcode, Category A, Category B, Category C)
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA

DEFAULT_XLSX = "POS_dataset.xlsx"  # default όνομα αν δεν δώσεις

def excel_date_to_datetime(series):
    # Αν η στήλη Date_ είναι αριθμός (Excel serial) ή ήδη datetime, χειρίζεται και τα 2
    try:
        if pd.api.types.is_integer_dtype(series) or pd.api.types.is_float_dtype(series):
            return pd.to_datetime(series, unit='D', origin='1899-12-30', errors='coerce')
        else:
            return pd.to_datetime(series, errors='coerce')
    except Exception:
        return pd.to_datetime(series, errors='coerce')

def read_data(xlsx_path):
    xlsx_path = Path(xlsx_path)
    if not xlsx_path.exists():
        raise FileNotFoundError(f"Could not find file: {xlsx_path}")
    xls = pd.ExcelFile(xlsx_path, engine='openpyxl')
    # Χρήση των ονομάτων φύλλων που έδωσες
    pos = pd.read_excel(xls, sheet_name='POS Data', dtype={'Barcode':str})
    loyalty = pd.read_excel(xls, sheet_name='Loyalty') if 'Loyalty' in xls.sheet_names else pd.DataFrame()
    hierarchy = pd.read_excel(xls, sheet_name='Hierachy Categories & Barcodes', dtype={'Barcode':str}) \
                if 'Hierachy Categories & Barcodes' in xls.sheet_names else pd.DataFrame()
    return pos, loyalty, hierarchy

def basic_checks(pos):
    print("ROWS, COLS:", pos.shape)
    print("Columns:", list(pos.columns))
    print("Preview:\n", pos.head())
    print("Missing per col:\n", pos.isna().sum())

def clean_pos(pos):
    pos = pos.copy()
    # Normalize column names just in case
    pos = pos.rename(columns=lambda c: c.strip())
    # Date conversion
    if 'Date_' in pos.columns:
        pos['Date_'] = excel_date_to_datetime(pos['Date_'])
    # Ensure Barcode is string and zero-padded to 12
    if 'Barcode' in pos.columns:
        pos['Barcode'] = pos['Barcode'].astype(str).str.strip().replace({'nan': None})
        pos['Barcode_fixed'] = pos['Barcode'].fillna('').apply(lambda x: x.zfill(12) if x!='' else '')
    # Rename Quantity/Value_ to canonical names used below
    if 'Quantity' in pos.columns:
        pos['Sum_Units'] = pd.to_numeric(pos['Quantity'], errors='coerce')
    else:
        pos['Sum_Units'] = pd.to_numeric(pos.get('Sum_Units'), errors='coerce')
    if 'Value_' in pos.columns:
        pos['Sum_Value'] = pd.to_numeric(pos['Value_'], errors='coerce')
    else:
        pos['Sum_Value'] = pd.to_numeric(pos.get('Sum_Value'), errors='coerce')
    # Loyalty card id
    if 'LoyaltyCard_ID' in pos.columns:
        pos['Card_ID'] = pos['LoyaltyCard_ID'].astype(str).replace({'nan': ''})
    else:
        pos['Card_ID'] = pos.get('Card_ID','').astype(str)
    # Flags
    pos['is_negative_units'] = pos['Sum_Units'] < 0
    pos['is_negative_value'] = pos['Sum_Value'] < 0
    near_int = np.isclose(pos['Sum_Units'], pos['Sum_Units'].round(), atol=1e-6)
    pos['noninteger_units_flag'] = (~near_int) & pos['Sum_Units'].notna()
    pos['barcode_invalid_flag'] = ~pos['Barcode_fixed'].str.match(r'^\d{12}$')
    pos['unit_price'] = pos['Sum_Value'] / pos['Sum_Units'].replace(0, np.nan)
    return pos

def aggregate_baskets(pos, hierarchy=None):
    # groupby Basket_ID
    agg = {
        'Sum_Units': 'sum',
        'Sum_Value': 'sum',
        'Barcode_fixed': pd.Series.nunique,
        'unit_price': 'mean',
        'is_negative_units': 'sum',
        'noninteger_units_flag': 'sum'
    }
    b = pos.groupby('Basket_ID').agg(agg).rename(columns={
        'Sum_Units':'total_items',
        'Sum_Value':'total_value',
        'Barcode_fixed':'unique_products',
        'unit_price':'avg_unit_price'
    }).reset_index()
    b['avg_items_per_product'] = b['total_items'] / b['unique_products'].replace(0, np.nan)
    b['prop_negative_lines'] = pos.groupby('Basket_ID')['is_negative_units'].mean().reindex(b['Basket_ID']).values
    # date per basket
    if 'Date_' in pos.columns:
        first_dates = pos.groupby('Basket_ID')['Date_'].min().reindex(b['Basket_ID']).values
        b['date'] = pd.to_datetime(first_dates)
    # category exposures if hierarchy provided
    if hierarchy is not None and not hierarchy.empty:
        # Hierarchy: expect Barcode, Category A/B/C
        prod_map = hierarchy[['Barcode','Category A']].drop_duplicates().set_index('Barcode')
        pos2 = pos.set_index('Barcode_fixed').join(prod_map, how='left').reset_index()
        pos2 = pos2.rename(columns={'Barcode_fixed':'Barcode_fixed'})
        cat_counts = pos2.groupby(['Basket_ID','Category A']).size().unstack(fill_value=0)
        if not cat_counts.empty:
            cat_counts.columns = [f"cat_{c}" for c in cat_counts.columns]
            b = b.set_index('Basket_ID').join(cat_counts).reset_index()
            cat_cols = [c for c in b.columns if str(c).startswith('cat_')]
            b[cat_cols] = b[cat_cols].div(b['unique_products'].replace(0,1), axis=0)
    return b

def create_custom_basket_category(b):
    b = b.copy()
    b['basket_type'] = 'other'
    # example thresholds using percentiles
    try:
        p75_value = b['total_value'].quantile(0.75)
        b.loc[(b['unique_products'] >= 8) & (b['total_value'] >= p75_value*0.6), 'basket_type'] = 'big_shop'
    except Exception:
        pass
    b.loc[(b['unique_products'] <= 3) & (b['total_items'] >= 5), 'basket_type'] = 'top_up'
    b.loc[(b['total_items'] <= 3) & (b['total_value'] <= 5), 'basket_type'] = 'impulse'
    b.loc[b['prop_negative_lines'] > 0.3, 'basket_type'] = 'returns'
    return b

def make_clustering_ready(b, out_path):
    out_path = Path(out_path)
    out_path.mkdir(parents=True, exist_ok=True)
    cat_cols = [c for c in b.columns if str(c).startswith('cat_')]
    numeric_cols = ['total_items','total_value','unique_products','avg_unit_price','avg_items_per_product','prop_negative_lines']
    Xcols = [c for c in numeric_cols if c in b.columns] + cat_cols
    X = b[Xcols].fillna(0)
    pipeline = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    X_scaled = pipeline.fit_transform(X)
    pca = PCA(n_components=min(10, X_scaled.shape[1])) if X_scaled.shape[1] > 1 else None
    if pca is not None:
        X_pca = pca.fit_transform(X_scaled)
        pd.DataFrame(X_pca, index=b['Basket_ID']).to_csv(out_path / "baskets_pca.csv")
    pd.DataFrame(X_scaled, index=b['Basket_ID'], columns=[f"scaled_{c}" for c in X.columns]).to_csv(out_path / "baskets_scaled.csv")
    b.to_csv(out_path / "baskets_enriched.csv", index=False)
    print("Saved:", out_path)
    return b

def main():
    infile = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_XLSX
    pos, loyalty, hierarchy = read_data(infile)
    basic_checks(pos)
    pos_clean = clean_pos(pos)
    baskets = aggregate_baskets(pos_clean, hierarchy)
    baskets = create_custom_basket_category(baskets)
    make_clustering_ready(baskets, Path("output"))

if __name__ == "__main__":
    main()
