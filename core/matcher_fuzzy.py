import pandas as pd
from thefuzz import fuzz

def find_fuzzy_matches(unmatched_a: pd.DataFrame, unmatched_b: pd.DataFrame, 
                       exact_cols: list, fuzzy_col: str, threshold: int = 85) -> dict:
    """
    Finds matches where exact_cols (e.g., Amount) match perfectly, but the fuzzy_col 
    (e.g., Customer Name) has slight text variations, scoring above the threshold.
    """
    if unmatched_a.empty or unmatched_b.empty or not exact_cols:
        return {
            'matched_fuzzy': pd.DataFrame(),
            'remaining_unmatched_a': unmatched_a,
            'remaining_unmatched_b': unmatched_b
        }

    # 1. Merge on the exact columns first to prevent memory explosion
    merged = pd.merge(unmatched_a, unmatched_b, on=exact_cols, suffixes=('_A', '_B'))
    
    if merged.empty:
        return {'matched_fuzzy': pd.DataFrame(), 'remaining_unmatched_a': unmatched_a, 'remaining_unmatched_b': unmatched_b}

    # 2. Calculate the Fuzzy Similarity Score (0 to 100)
    col_a = f"{fuzzy_col}_A"
    col_b = f"{fuzzy_col}_B"
    
    def calculate_score(row):
        # token_sort_ratio handles out-of-order words well
        return fuzz.token_sort_ratio(str(row[col_a]).lower(), str(row[col_b]).lower())
        
    merged['Fuzzy_Score'] = merged.apply(calculate_score, axis=1)
    
    # 3. Filter for matches that meet or exceed our threshold
    matched_fuzzy = merged[merged['Fuzzy_Score'] >= threshold].copy()
    
    # 4. Remove these newly matched records from the leftover piles
    if not matched_fuzzy.empty:
        # Create a unique key using the exact columns + the original fuzzy column values
        # To drop them correctly from Dataset A
        keys_a = matched_fuzzy[exact_cols + [col_a]].rename(columns={col_a: fuzzy_col}).drop_duplicates()
        rem_a = pd.merge(unmatched_a, keys_a, on=exact_cols + [fuzzy_col], how='outer', indicator=True)
        remaining_a = rem_a[rem_a['_merge'] == 'left_only'].drop(columns=['_merge'])
        
        # To drop them correctly from Dataset B
        keys_b = matched_fuzzy[exact_cols + [col_b]].rename(columns={col_b: fuzzy_col}).drop_duplicates()
        rem_b = pd.merge(unmatched_b, keys_b, on=exact_cols + [fuzzy_col], how='outer', indicator=True)
        remaining_b = rem_b[rem_b['_merge'] == 'left_only'].drop(columns=['_merge'])
    else:
        remaining_a = unmatched_a.copy()
        remaining_b = unmatched_b.copy()
        
    return {
        'matched_fuzzy': matched_fuzzy,
        'remaining_unmatched_a': remaining_a,
        'remaining_unmatched_b': remaining_b
    }