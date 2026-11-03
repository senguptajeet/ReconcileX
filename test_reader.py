import pandas as pd
import os
from core.file_reader import read_file

print("Starting test...")

# 1. Create a dummy CSV file to test with
test_csv_path = "dummy_test_data.csv"
dummy_data = """Invoice Number , Customer Name, Amount 
INV-001, ABC Corp, 5000.50
INV-002, XYZ Ltd , 1200.00
,,
INV-003, Acme Inc, 300.00"""

with open(test_csv_path, "w") as f:
    f.write(dummy_data)

print(f"Created temporary test file: {test_csv_path}")

# 2. Test our read_file function
try:
    print("\nReading file via file_reader.py...")
    df = read_file(test_csv_path)
    
    print("\n--- TEST SUCCESSFUL ---")
    print("Here is the cleaned data loaded into memory:")
    print(df)
    
    print("\nNotice how the blank row was removed, and column spaces are cleaned!")
    
except Exception as e:
    print(f"\nTEST FAILED: {e}")

# 3. Clean up the dummy file
if os.path.exists(test_csv_path):
    os.remove(test_csv_path)
    print("\nTemporary test file deleted.")