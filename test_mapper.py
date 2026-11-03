import pandas as pd
from core.column_mapper import suggest_mapping, rename_columns

print("Starting Column Mapper test...\n")

# 1. Simulate column headers from two different systems
dataset_a_columns = ["Invoice Number", "Customer Name", "Total Amount", "Txn Date"]
dataset_b_columns = ["invoice number", "Client", "totalamount", "Date"]

print(f"Dataset A headers: {dataset_a_columns}")
print(f"Dataset B headers: {dataset_b_columns}\n")

# 2. Test auto-suggestions
print("--- Auto-Suggesting Mappings ---")
suggestions = suggest_mapping(dataset_a_columns, dataset_b_columns)
for b_col, a_col in suggestions.items():
    print(f"Match found: '{b_col}' (Dataset B) -> '{a_col}' (Dataset A)")

# 3. Simulate a user finalizing the map (accepting suggestions + adding a manual one)
final_mapping = suggestions.copy()
final_mapping["Client"] = "Customer Name"  # Manual map by user
print("\nFinal Mapping Rules:", final_mapping)

# 4. Apply mapping to a dummy Dataset B
data_b = {
    "invoice number": ["INV-01"],
    "Client": ["ABC Corp"],
    "totalamount": [500.00]
}
df_b = pd.DataFrame(data_b)

print("\n--- Dataset B BEFORE mapping ---")
print(df_b.columns.tolist())

df_b_mapped = rename_columns(df_b, final_mapping)

print("\n--- Dataset B AFTER mapping ---")
print(df_b_mapped.columns.tolist())