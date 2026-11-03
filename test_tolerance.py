import pandas as pd
from core.matcher_tolerance import find_tolerance_matches

print("Starting Tolerance Matcher test...\n")

# 1. Simulate leftover UNMATCHED records from Dataset A (Sales)
data_a = {
    "Invoice ID": ["INV-001", "INV-002", "INV-003"],
    "Amount": [100.00, 500.00, 200.00]
}
unmatched_a = pd.DataFrame(data_a)

# 2. Simulate leftover UNMATCHED records from Dataset B (Bank)
# Notice INV-001 is off by $0.50, INV-002 is off by $5.00, INV-009 is a different record
data_b = {
    "Invoice ID": ["INV-001", "INV-002", "INV-009"],
    "Amount": [99.50, 495.00, 999.00]
}
unmatched_b = pd.DataFrame(data_b)

print("--- UNMATCHED A (Sales) ---")
print(unmatched_a)
print("\n--- UNMATCHED B (Bank) ---")
print(unmatched_b)

# 3. Run the Tolerance Matcher
# We want to match on 'Invoice ID', with a tolerance of $2.00 on 'Amount'
print("\nRunning Tolerance Matcher (Threshold: $2.00)...")
results = find_tolerance_matches(
    unmatched_a=unmatched_a, 
    unmatched_b=unmatched_b, 
    exact_cols=["Invoice ID"], 
    tolerance_col="Amount", 
    tolerance_value=2.00
)

# 4. Display Results
print("\n--- NEWLY MATCHED (WITHIN TOLERANCE) ---")
print(results['matched_tolerance'][['Invoice ID', 'Amount_A', 'Amount_B', 'Tolerance_Diff']])

print("\n--- REMAINING UNMATCHED A ---")
print(results['remaining_unmatched_a'])

print("\n--- REMAINING UNMATCHED B ---")
print(results['remaining_unmatched_b'])