import pandas as pd
from core.normalization import standardize_strings, standardize_numbers, standardize_dates

print("Starting normalization test...\n")

# 1. Create a messy DataFrame simulating real-world Excel problems
messy_data = {
    "Invoice Number": [" INV-100 ", "inv-101", "INV  102"],
    "Amount": ["$5,000.50", "₹ 1,200.00", "300.999"],
    "Date": ["12-Oct-2023", "10/13/2023", "2023.10.14"]
}
df = pd.DataFrame(messy_data)

print("--- ORIGINAL MESSY DATA ---")
print(df)
print(df.dtypes) # Look at the data types (they will all be 'object' / strings)

# 2. Apply our normalization functions
df["Invoice Number"] = standardize_strings(df["Invoice Number"])
df["Amount"] = standardize_numbers(df["Amount"])
df["Date"] = standardize_dates(df["Date"])

print("\n--- CLEANED & NORMALIZED DATA ---")
print(df)
print(df.dtypes) # Look at the new data types (Float and Datetime!)

print("\nNotice how amounts are now strict decimals, text is uniform, and dates are standardized!")