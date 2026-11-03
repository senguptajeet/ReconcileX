import pandas as pd
from core.matcher_fuzzy import find_fuzzy_matches

print("Starting Fuzzy Matcher test...\n")

# 1. Simulate leftover records. Notice the Amounts match perfectly, but names differ.
data_a = {
    "Amount": [500.00, 1200.00, 300.00],
    "Customer": ["Reliance Industries", "Tata Motors Ltd", "Infosys"]
}
unmatched_a = pd.DataFrame(data_a)

data_b = {
    "Amount": [500.00, 1200.00, 999.00],
    "Customer": ["Reliance Ind.", "Tata Motor Limited", "Wipro"]
}
unmatched_b = pd.DataFrame(data_b)

print("--- UNMATCHED A (Sales) ---")
print(unmatched_a)
print("\n--- UNMATCHED B (Bank) ---")
print(unmatched_b)

# 2. Run Fuzzy Matching (Match exactly on Amount, fuzzy match on Customer)
print("\nRunning Fuzzy Matcher (Threshold: 80)...\n")
results = find_fuzzy_matches(
    unmatched_a=unmatched_a, 
    unmatched_b=unmatched_b, 
    exact_cols=["Amount"], 
    fuzzy_col="Customer", 
    threshold=80
)

# 3. Display Results
print("--- NEWLY MATCHED (FUZZY) ---")
if not results['matched_fuzzy'].empty:
    print(results['matched_fuzzy'][['Amount', 'Customer_A', 'Customer_B', 'Fuzzy_Score']])
else:
    print("None")

print("\n--- REMAINING UNMATCHED A ---")
print(results['remaining_unmatched_a'])