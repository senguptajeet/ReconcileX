import pandas as pd
import numpy as np

def standardize_strings(series: pd.Series) -> pd.Series:
    """
    Cleans text columns: converts to uppercase, strips whitespace, 
    removes duplicate spaces, and handles empty values.
    """
    # Convert to string, upper case, strip edge spaces, and replace multiple spaces with one
    cleaned = series.astype(str).str.upper().str.strip().str.replace(r'\s+', ' ', regex=True)
    
    # Convert string representations of empty values back to actual pandas NA (nulls)
    cleaned = cleaned.replace(['NAN', 'NONE', 'NULL', '<NA>', ''], pd.NA)
    return cleaned

def standardize_numbers(series: pd.Series) -> pd.Series:
    """
    Cleans financial/numeric columns: removes currencies, commas, 
    converts to numeric types, and rounds to 2 decimals.
    """
    # Remove anything that isn't a digit, a minus sign, or a decimal point
    cleaned = series.astype(str).str.replace(r'[^\d.-]', '', regex=True)
    
    # Convert to numeric, turn errors (like totally blank cells) into NaN, and round to 2 decimals
    return pd.to_numeric(cleaned, errors='coerce').round(2)

def standardize_dates(series: pd.Series) -> pd.Series:
    """
    Cleans date columns: converts various string date formats into standard Pandas datetime objects.
    Replaces dots/slashes with dashes and handles mixed formatting.
    """
    # Convert to string and normalize separators to dashes
    cleaned = series.astype(str).str.replace('.', '-', regex=False)
    cleaned = cleaned.str.replace('/', '-', regex=False)
    
    # format='mixed' tells Pandas to figure out US vs Euro formats row-by-row
    return pd.to_datetime(cleaned, errors='coerce', format='mixed')