import pandas as pd

def find_exact_matches(df_a: pd.DataFrame, df_b: pd.DataFrame, match_columns: list) -> dict:
    """
    Compares two DataFrames based on a list of columns and identifies exact matches.
    
    Returns a dictionary containing:
    - 'matched': DataFrame of records found in both.
    - 'unmatched_a': DataFrame of records only in Dataset A.
    - 'unmatched_b': DataFrame of records only in Dataset B.
    """
    
    # Perform an outer merge to keep all records from both datasets.
    # indicator=True creates a special column '_merge' detailing where the row came from.
    merged = pd.merge(df_a, df_b, on=match_columns, how='outer', indicator=True)
    
    # Filter based on the indicator column
    matched = merged[merged['_merge'] == 'both'].copy()
    unmatched_a = merged[merged['_merge'] == 'left_only'].copy()
    unmatched_b = merged[merged['_merge'] == 'right_only'].copy()
    
    # Clean up the helper column before returning the data
    matched.drop(columns=['_merge'], inplace=True)
    unmatched_a.drop(columns=['_merge'], inplace=True)
    unmatched_b.drop(columns=['_merge'], inplace=True)
    
    return {
        'matched': matched,
        'unmatched_a': unmatched_a,
        'unmatched_b': unmatched_b
    }