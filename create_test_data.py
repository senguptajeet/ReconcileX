import pandas as pd
pd.DataFrame({"Invoice Number": [1], "Customer": ["A"], "Amount": [100]}).to_csv("A_Sales.csv", index=False)
pd.DataFrame({"invoice number": [1], "Client": ["A"], "amount": [100]}).to_csv("B_Bank.csv", index=False)