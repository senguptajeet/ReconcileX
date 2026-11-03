import pandas as pd

def rename_columns(df: pd.DataFrame, mapping_dict: dict) -> pd.DataFrame:
    """
    Renames columns in a DataFrame based on a provided mapping dictionary.
    Format of mapping_dict: {'Original_Name': 'Standardized_Name'}
    """
    # Create a copy so we don't accidentally modify the original dataset
    mapped_df = df.copy()
    mapped_df.rename(columns=mapping_dict, inplace=True)
    return mapped_df

def suggest_mapping(columns_a: list, columns_b: list) -> dict:
    """
    Suggests column mappings by comparing stripped, lowercase strings.
    Returns a dictionary of suggested mappings: {'Column_B': 'Column_A'}
    """
    suggestions = {}
    
    # Create a simplified version of Dataset A's columns (lowercase, no spaces)
    # e.g., "Invoice Number" becomes "invoicenumber"
    simplified_a = {col.lower().replace(' ', ''): col for col in columns_a}
    
    for col_b in columns_b:
        simplified_b = col_b.lower().replace(' ', '')
        if simplified_b in simplified_a:
            # If a match is found, link the original Dataset B name to the original Dataset A name
            suggestions[col_b] = simplified_a[simplified_b]
            
    return suggestions