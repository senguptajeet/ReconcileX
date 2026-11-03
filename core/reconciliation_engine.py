import pandas as pd
from core.column_mapper import rename_columns
from core.matcher_exact import find_exact_matches
from core.matcher_tolerance import find_tolerance_matches
from core.matcher_fuzzy import find_fuzzy_matches

def run_reconciliation(df_a: pd.DataFrame, df_b: pd.DataFrame, mapping_dict: dict, 
                       match_columns: list, tolerance_col: str = None, 
                       tolerance_value: float = 0.0, fuzzy_col: str = None, 
                       fuzzy_threshold: int = 85) -> dict:
    """
    Master orchestrator: 1. Exact Match -> 2. Tolerance Match -> 3. Fuzzy Match
    """
    df_b_mapped = rename_columns(df_b, mapping_dict)
    
    for col in match_columns:
        if col not in df_a.columns or col not in df_b_mapped.columns:
            raise ValueError(f"Error: Match column '{col}' is missing.")
            
    # Phase 1: Exact matching
    exact_results = find_exact_matches(df_a, df_b_mapped, match_columns)
    unmatched_a = exact_results['unmatched_a']
    unmatched_b = exact_results['unmatched_b']
    
    matched_tolerance = pd.DataFrame()
    matched_fuzzy = pd.DataFrame()
    
    # Phase 2: Tolerance matching
    if tolerance_col and tolerance_col in match_columns and tolerance_value > 0.0:
        exact_cols = [col for col in match_columns if col != tolerance_col]
        if exact_cols:
            tol_results = find_tolerance_matches(unmatched_a, unmatched_b, exact_cols, tolerance_col, tolerance_value)
            matched_tolerance = tol_results['matched_tolerance']
            unmatched_a = tol_results['remaining_unmatched_a']
            unmatched_b = tol_results['remaining_unmatched_b']

    # Phase 3: Fuzzy matching
    if fuzzy_col and fuzzy_col in match_columns and fuzzy_threshold > 0:
        # We exact match on everything EXCEPT the fuzzy column to avoid memory crashes
        exact_cols_for_fuzzy = [col for col in match_columns if col != fuzzy_col]
        if exact_cols_for_fuzzy:
            fuzzy_results = find_fuzzy_matches(unmatched_a, unmatched_b, exact_cols_for_fuzzy, fuzzy_col, fuzzy_threshold)
            matched_fuzzy = fuzzy_results['matched_fuzzy']
            unmatched_a = fuzzy_results['remaining_unmatched_a']
            unmatched_b = fuzzy_results['remaining_unmatched_b']

    return {
        'matched_exact': exact_results['matched'],
        'matched_tolerance': matched_tolerance,
        'matched_fuzzy': matched_fuzzy,
        'unmatched_a': unmatched_a,
        'unmatched_b': unmatched_b
    }