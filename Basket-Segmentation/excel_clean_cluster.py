# excel_clean_cluster.py
import os
from collections import Counter
import pandas as pd
import numpy as np

# Για clustering/plots
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

FILE = "baskets.csv"   # όνομα αρχείου - βάλε το σωστό όνομα

def peek_file(path, n=20, encodings=('utf-8','cp1253','latin1')):
    print(f"\n--- Preview first {n} lines (trying encodings) ---")
    for enc in encodings:
        print(f"\n[encoding={enc}]")
        try:
            with open(path, encoding=enc, errors='replace') as f:
                for i,line in enumerate(f,1):
                    print(i, line.rstrip('\n'))
                    if i>=n: break
            break
        except Exception as e:
            print("  failed:", e)

def detect_sep(path, n=200, enc='utf-8'):
    counts = Counter()
    with open(path, encoding=enc, errors='replace') as f:
        for i,line in enumerate(f):
            if i>=n: break
            counts[','] += line.count(',')
            counts[';'] += line.count(';')
            counts['\t'] += line.count('\t')
    print("\nSeparator counts (first {} lines):".format(n))
    print(counts)
    # choose the one with most hits
    sep = counts.most_common(1)[0][0]
    print("-> guessing sep =", repr(sep))
    return sep

def try_read(path):
    # try multiple encodings and separators
    attempts = []
    encodings = ['utf-8','cp1253','latin1']
    seps = [',',';','\t']
    for enc in encodings:
        for sep in seps:
            try:
                print(f"\nAttempt read with encoding={enc} sep={repr(sep)} engine='python' ...")
                df = pd.read_csv(path, sep=sep, engine='python', encoding=enc, on_bad_lines='error')
                print("SUCCESS with", enc, sep)
                return df, enc, sep
            except Exception as e:
                attempts.append((enc,sep,str(e)))
                print(" failed:", str(e).splitlines()[0])
    print("\nAll attempts failed. Summary of attempts (first 10):")
    for a in attempts[:10]:
        print(a)
    return None, None, None

def find_bad_lines(path, sep=',', enc='utf-8', nlines=5000):
    print(f"\nScanning up to {nlines} lines to find lines with wrong number of fields (sep='{sep}', enc='{enc}')")
    with open(path, encoding=enc, errors='replace') as f:
        header = next(f)
        expected = len(header.rstrip('\n').split(sep))
        print("Expected columns from header:", expected)
        bad = []
        for i,line in enumerate(f,2):
            if i>nlines: break
            n = len(line.rstrip('\n').split(sep))
            if n != expected:
                bad.append((i, n, line.rstrip('\n')[:200]))
        print("Found", len(bad), "bad lines (show up to 20):")
        for b in bad[:20]:
            print(b)
    return bad

def clean_with_python_engine(path, sep, enc):
    # read with engine='python' allowing messy quoting
    print("\nReading with engine='python', on_bad_lines='warn' ...")
    df = pd.read_csv(path, sep=sep, engine='python', encoding=enc, on_bad_lines='warn', low_memory=False)
    return df

def run_clustering(df, out_csv="Basket_Segmentation.csv", n_clusters=3):
    # Check required columns
    required = ['total_value','total_units','unique_products','unique_categories','used_loyalty_card','avg_value_per_product']
    for col in required:
        if col not in df.columns:
            print("ERROR: missing required column:", col)
            return
    X = df[required].fillna(0).astype(float)
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(Xs)
    df.to_csv(out_csv, index=False)
    print("Saved clustering to", out_csv)
    # basic plot
    plt.figure(figsize=(7,5))
    plt.scatter(df['total_value'], df['total_units'], c=df['cluster'], s=6)
    plt.xlabel('total_value'); plt.ylabel('total_units'); plt.title('Clusters')
    plt.tight_layout()
    plt.savefig("clusters_scatter.png", dpi=150)
    print("Saved scatter plot to clusters_scatter.png")
    return df

if __name__ == "__main__":
    if not os.path.exists(FILE):
        print("File not found:", FILE); raise SystemExit

    # 1) preview
    peek_file(FILE, n=12)

    # 2) detect sep (quick)
    guessed_sep = detect_sep(FILE, n=500)

    # 3) try read with a few options
    df, enc, sep = try_read(FILE)
    if df is None:
        # try to find bad lines using guessed sep and common encodings
        bad = find_bad_lines(FILE, sep=guessed_sep, enc='utf-8', nlines=2000)
        if len(bad)==0:
            bad = find_bad_lines(FILE, sep=guessed_sep, enc='cp1253', nlines=2000)
        print("\nIf there are bad lines, open the file in Excel, go to those line numbers and inspect fields (commas/quotes/newlines).")
        print("Alternative: open original Excel file and Save As -> CSV (UTF-8) or .xlsx and re-run.")
        raise SystemExit

    print("\nDataframe loaded: shape=", df.shape)
    print("Columns:", df.columns.tolist())
    # Μετατροπή ελληνικών δεκαδικών (8,69 -> 8.69)
    df = df.replace(',', '.', regex=True)
    for col in ['total_value','total_units','unique_products','unique_categories',
                'loyalty_count','used_loyalty_card','avg_value_per_product','items_per_product']:
        df[col] = pd.to_numeric(df[col], errors='coerce')


    # If df loaded but columns seem wrong (e.g., only 3 cols), suggest to reexport from Excel as .xlsx and read with pandas.read_excel
    if df.shape[1] < 6:
        print("\nIt looks like the dataframe has few columns. If this is an export artifact, try opening the original Excel and Save As -> CSV (UTF-8) or save as .xlsx and use pd.read_excel.")
        # try read xlsx
        xlsx = FILE.replace('.csv','.xlsx')
        if os.path.exists(xlsx):
            print("Found xlsx:", xlsx, "trying read_excel ...")
            df = pd.read_excel(xlsx)
            print("read_excel shape:", df.shape)

    # At this point assume df is read correctly. If it is the aggregated basket summary, run clustering.
    # If your file is raw POS data, you must run the PowerQuery M steps first to produce Basket_Summary CSV, then run clustering.
    # Here we check if 'total_value' exists:
    if 'total_value' not in df.columns:
        print("\nThe file does not contain 'total_value' column. If this is raw POS data, export the Basket_Summary CSV from Excel (one row per Basket_ID) and rerun.")
        raise SystemExit

    # run clustering
    df_out = run_clustering(df, out_csv="Basket_Segmentation.csv", n_clusters=3)
    print("\nDone.")
