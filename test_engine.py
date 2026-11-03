import pandas as pd
from core.reconciliation_engine import run_reconciliation

print("Starting Two-Phase Engine Pipeline test...\n")

# 1. Simulate Dataset A (Sales System)
data_a = {
    "Invoice ID": ["INV-01", "INV-02", "INV-03"],
    "Amount": [100.0, 500.0, 200.0]
}
df_a = pd.DataFrame(data_a)

# 2. Simulate Dataset B (Bank Statement) with DIFFERENT column names
# INV-01 matches exactly. INV-02 is off by $1.00. INV-09 is unknown.
data_b = {
    "Txn Ref": ["INV-01", "INV-02", "INV-09"],
    "Total Paid": [100.0, 499.0, 999.0]
}
df_b = pd.DataFrame(data_b)

mapping_dict = {"Txn Ref": "Invoice ID", "Total Paid": "Amount"}
match_columns = ["Invoice ID", "Amount"]

print("Running engine with $2.00 tolerance on 'Amount'...")

# 3. Run the Engine!
try:
    results = run_reconciliation(
        df_a=df_a, 
        df_b=df_b, 
        mapping_dict=mapping_dict, 
        match_columns=match_columns,
        tolerance_col="Amount",
        tolerance_value=2.00 # We allow a $2 difference
    )
    
    print("\n--- PHASE 1: EXACT MATCHES ---")
    print(results['matched_exact'])
    
    print("\n--- PHASE 2: TOLERANCE MATCHES ---")
    print(results['matched_tolerance'] if not results['matched_tolerance'].empty else "None")
    
    print("\n--- LEFTOVER UNMATCHED A ---")
    print(results['unmatched_a'])
    
    print("\n--- LEFTOVER UNMATCHED B ---")
    print(results['unmatched_b'])
    
except Exception as e:
    print(f"PIPELINE FAILED: {e}")