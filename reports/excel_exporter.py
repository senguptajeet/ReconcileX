import pandas as pd

def export_to_excel(results: dict, output_path: str):
    """
    Exports the reconciliation results dictionary to a multi-sheet Excel file.
    Automatically adjusts column widths for a professional finish.
    """
    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        
        # Define friendly names for our Excel tabs
        sheet_mapping = {
            'matched_exact': 'Exact Matches',
            'matched_tolerance': 'Tolerance Matches',
            'matched_fuzzy': 'Fuzzy Matches',
            'unmatched_a': 'Unmatched (Dataset A)',
            'unmatched_b': 'Unmatched (Dataset B)'
        }
        
        for dict_key, sheet_name in sheet_mapping.items():
            df = results.get(dict_key, pd.DataFrame())
            
            # Only create a tab if there is actually data in this category
            if not df.empty:
                # Write data to the sheet (without the pandas index numbers)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Access the XlsxWriter worksheet object to apply formatting
                worksheet = writer.sheets[sheet_name]
                
                # Auto-adjust column widths
                for i, col in enumerate(df.columns):
                    # Find the length of the longest item in the column, or the header itself
                    max_len = max(df[col].astype(str).map(len).max(), len(str(col))) + 2
                    worksheet.set_column(i, i, max_len)