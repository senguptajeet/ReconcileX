import pandas as pd

def find_tolerance_matches(unmatched_a: pd.DataFrame, unmatched_b: pd.DataFrame, 
                           exact_cols: list, tolerance_col: str, tolerance_value: float) -> dict:
    """
    Finds matches where exact_cols match perfectly, but the tolerance_col 
    differs by an amount less than or equal to the tolerance_value.
    """
    # If there are no unmatched records left, just return empty/original DataFrames
    if unmatched_a.empty or unmatched_b.empty:
        return {
            'matched_tolerance': pd.DataFrame(),
            'remaining_unmatched_a': unmatched_a,
            'remaining_unmatched_b': unmatched_b
        }

    # 1. Merge the unmatched datasets on the exact columns (e.g., Invoice ID)
    # suffixes=('_A', '_B') ensures our Amount columns become Amount_A and Amount_B
    merged = pd.merge(unmatched_a, unmatched_b, on=exact_cols, suffixes=('_A', '_B'))
    
    if merged.empty:
        return {'matched_tolerance': pd.DataFrame(), 'remaining_unmatched_a': unmatched_a, 'remaining_unmatched_b': unmatched_b}

    # 2. Calculate the difference
    col_a = f"{tolerance_col}_A"
    col_b = f"{tolerance_col}_B"
    merged['Tolerance_Diff'] = (merged[col_a] - merged[col_b]).abs()
    
    # 3. Filter for matches within our allowed threshold
    matched_tolerance = merged[merged['Tolerance_Diff'] <= tolerance_value].copy()
    
    # 4. Remove these newly matched records from our unmatched piles (Prevent duplicates)
    # We grab the keys of the records we just matched
    matched_keys = matched_tolerance[exact_cols].drop_duplicates()
    
    if not matched_keys.empty:
        # 'how=left' with indicator=True helps us find records in unmatched_a that are NOT in matched_keys
        rem_a = pd.merge(unmatched_a, matched_keys, on=exact_cols, how='outer', indicator=True)
        remaining_a = rem_a[rem_a['_merge'] == 'left_only'].drop(columns=['_merge'])
        
        rem_b = pd.merge(unmatched_b, matched_keys, on=exact_cols, how='outer', indicator=True)
        remaining_b = rem_b[rem_b['_merge'] == 'left_only'].drop(columns=['_merge'])
    else:
        remaining_a = unmatched_a.copy()
        remaining_b = unmatched_b.copy()
        
    return {
        'matched_tolerance': matched_tolerance,
        'remaining_unmatched_a': remaining_a,
        'remaining_unmatched_b': remaining_b
    }