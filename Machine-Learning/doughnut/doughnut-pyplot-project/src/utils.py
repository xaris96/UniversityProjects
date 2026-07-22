def preprocess_data(df):
    """
    Preprocess the input DataFrame for doughnut chart plotting.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing data for the doughnut chart.
    
    Returns:
    pd.DataFrame: A DataFrame ready for plotting.
    """
    df.columns = df.columns.str.strip()  # Strip whitespace from column names
    df['domain'] = df.get('domain', '').astype(str).str.strip()  # Ensure 'domain' is a string
    return df


def get_ratio_column(df):
    """
    Identify the appropriate ratio column from the DataFrame.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    
    Returns:
    str: The name of the ratio column.
    """
    ratio_cols = [c for c in df.columns if 'ratio' in c.lower()]
    prefer = [c for c in ratio_cols if 'end' in c.lower()] + ratio_cols
    
    if prefer:
        return prefer[0]
    elif 'value' in df.columns:
        return 'value'
    else:
        return None


def scale_ratios(df, raw):
    """
    Scale the ratios in the DataFrame.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    raw (str): The name of the raw ratio column.
    
    Returns:
    pd.DataFrame: The DataFrame with scaled ratios.
    """
    vals = df[raw].astype(float).values
    if vals.max() > 1.0:
        df['ratio_pct'] = vals
        df['ratio_scaled'] = (df['ratio_pct'] / 100.0).clip(lower=0)
    else:
        df['ratio_scaled'] = vals.clip(0, 1)
        df['ratio_pct'] = df['ratio_scaled'] * 100.0
    return df


def normalize_labels(label_map):
    """
    Normalize the keys in the label mapping dictionary.
    
    Parameters:
    label_map (dict): The label mapping dictionary.
    
    Returns:
    dict: A new dictionary with normalized keys.
    """
    return {str(k).strip().lower(): v for k, v in label_map.items()}