import pandas as pd
from core.matcher_exact import find_exact_matches

print("Starting Exact Matcher test...\n")

# 1. Simulate Dataset A (e.g., Company Sales Records)
data_a = {
    "Invoice_Number": ["INV-001", "INV-002", "INV-003", "INV-004"],
    "Amount": [100.00, 250.50, 300.00, 50.00]
}
df_a = pd.DataFrame(data_a)

# 2. Simulate Dataset B (e.g., Bank Statement)
data_b = {
    "Invoice_Number": ["INV-001", "INV-002", "INV-009", "INV-010"],
    "Amount": [100.00, 250.50, 999.00, 10.00]
}
df_b = pd.DataFrame(data_b)

print("--- DATASET A (Sales) ---")
print(df_a)
print("\n--- DATASET B (Bank) ---")
print(df_b)

# 3. Run the Exact Matcher (matching on Invoice_Number AND Amount)
print("\nRunning reconciliation engine...")
results = find_exact_matches(df_a, df_b, match_columns=["Invoice_Number", "Amount"])

# 4. Display Results
print("\n--- MATCHED RECORDS ---")
print(results['matched'] if not results['matched'].empty else "None")

print("\n--- UNMATCHED IN A (Missing from Bank) ---")
print(results['unmatched_a'] if not results['unmatched_a'].empty else "None")

print("\n--- UNMATCHED IN B (Unknown Bank Receipts) ---")
print(results['unmatched_b'] if not results['unmatched_b'].empty else "None")