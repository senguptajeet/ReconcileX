from PySide6.QtCore import QThread, Signal
import pandas as pd
from core.reconciliation_engine import run_reconciliation

class ReconciliationWorker(QThread):
    # Signals to communicate back to the Main Window safely
    finished_success = Signal(dict)
    finished_error = Signal(str)

    def __init__(self, df_a: pd.DataFrame, df_b: pd.DataFrame, mapping_dict: dict, 
                 match_columns: list, tolerance_val: float, fuzzy_col: str, fuzzy_thresh: int):
        super().__init__()
        self.df_a = df_a
        self.df_b = df_b
        self.mapping_dict = mapping_dict
        self.match_columns = match_columns
        self.tolerance_val = tolerance_val
        self.fuzzy_col = fuzzy_col
        self.fuzzy_thresh = fuzzy_thresh

    def run(self):
        """This method executes in a background thread when thread.start() is called."""
        try:
            results = run_reconciliation(
                df_a=self.df_a, 
                df_b=self.df_b, 
                mapping_dict=self.mapping_dict, 
                match_columns=self.match_columns,
                tolerance_col="Amount", 
                tolerance_value=self.tolerance_val,
                fuzzy_col=self.fuzzy_col,
                fuzzy_threshold=self.fuzzy_thresh
            )
            # Emit the results back to the main UI thread
            self.finished_success.emit(results)
            
        except Exception as e:
            # Emit the error message if something fails
            self.finished_error.emit(str(e))