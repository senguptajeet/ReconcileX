import pandas as pd
import os

def read_file(file_path: str, sheet_name: str = None) -> pd.DataFrame:
    """
    Reads an Excel or CSV file into a Pandas DataFrame.
    Cleans up column names and drops completely empty rows/columns.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} was not found.")

    file_extension = os.path.splitext(file_path)[1].lower()

    try:
        # Load the file based on its extension
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Please upload .csv or .xlsx")

        # Clean column names (convert to string and remove extra spaces)
        df.columns = df.columns.astype(str).str.strip()

        # Remove rows and columns that are completely empty (all NaN values)
        df.dropna(how='all', inplace=True)
        df.dropna(axis=1, how='all', inplace=True)

        # Reset the index so row numbers are sequential after dropping blank rows
        df.reset_index(drop=True, inplace=True)

        return df

    except Exception as e:
        raise RuntimeError(f"Failed to read data from {file_path}. Error: {str(e)}")