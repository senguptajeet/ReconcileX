import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTableView, QTabWidget, QHeaderView, 
                               QPushButton, QFileDialog, QMessageBox, QLineEdit)
from PySide6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, Signal
import pandas as pd
from reports.excel_exporter import export_to_excel

class PandasModel(QAbstractTableModel):
    def __init__(self, dataframe=pd.DataFrame()):
        super().__init__()
        self._df = dataframe
    def rowCount(self, parent=None): return len(self._df.index)
    def columnCount(self, parent=None): return len(self._df.columns)
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return str(self._df.iloc[index.row(), index.column()])
        return None
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal: return str(self._df.columns[section])
            if orientation == Qt.Orientation.Vertical: return str(self._df.index[section])
        return None

class ResultsScreen(QWidget):
    start_new_requested = Signal()

    def __init__(self):
        super().__init__()
        self.current_results = {}
        self.proxies = [] 
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Reconciliation Results")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # --- KPI Row ---
        kpi_layout = QHBoxLayout()
        self.lbl_matched = self.create_kpi_card("Exact Matches", "0", "#27ae60")
        self.lbl_tol = self.create_kpi_card("Tolerance Matches", "0", "#8e44ad") 
        self.lbl_fuzzy = self.create_kpi_card("Fuzzy Matches", "0", "#2980b9") 
        self.lbl_unmatched_a = self.create_kpi_card("Unmatched (A)", "0", "#e74c3c")
        self.lbl_unmatched_b = self.create_kpi_card("Unmatched (B)", "0", "#e67e22")
        
        kpi_layout.addWidget(self.lbl_matched)
        kpi_layout.addWidget(self.lbl_tol)
        kpi_layout.addWidget(self.lbl_fuzzy)
        kpi_layout.addWidget(self.lbl_unmatched_a)
        kpi_layout.addWidget(self.lbl_unmatched_b)
        layout.addLayout(kpi_layout)

        # --- Interactive Search Bar ---
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search across all records (Invoice, Name, Amount)...")
        self.search_bar.textChanged.connect(self.filter_tables)
        layout.addWidget(self.search_bar)

        # --- Data Tabs ---
        self.tabs = QTabWidget()
        self.table_matched = QTableView()
        self.table_tol = QTableView()
        self.table_fuzzy = QTableView()
        self.table_unmatched_a = QTableView()
        self.table_unmatched_b = QTableView()
        
        self.tabs.addTab(self.table_matched, "Exact Matches")
        self.tabs.addTab(self.table_tol, "Tolerance Matches")
        self.tabs.addTab(self.table_fuzzy, "Fuzzy Matches")
        self.tabs.addTab(self.table_unmatched_a, "Unmatched (A)")
        self.tabs.addTab(self.table_unmatched_b, "Unmatched (B)")
        layout.addWidget(self.tabs)

        # --- Action Buttons ---
        btn_layout = QHBoxLayout()
        
        self.btn_export = QPushButton("💾 Export Results to Excel")
        self.btn_export.setStyleSheet("background-color: #198754; color: white; border-color: #198754;")
        self.btn_export.clicked.connect(self.export_data)
        
        self.btn_start_new = QPushButton("Start New Reconciliation")
        self.btn_start_new.setStyleSheet("background-color: #6c757d; color: white; border-color: #6c757d;")
        self.btn_start_new.clicked.connect(self.start_new_requested.emit)
        
        self.btn_exit = QPushButton("✖ Exit")
        self.btn_exit.setStyleSheet("background-color: #dc3545; color: white; border-color: #dc3545;")
        self.btn_exit.clicked.connect(self.close_application)
        
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_start_new)
        btn_layout.addWidget(self.btn_exit)
        layout.addLayout(btn_layout)

    def create_kpi_card(self, title, initial_value, color):
        card = QLabel(f"<div style='text-align: center;'>"
                      f"<div style='font-size: 14px; color: #7f8c8d;'>{title}</div>"
                      f"<div style='font-size: 24px; font-weight: bold; color: {color};'>{initial_value}</div>"
                      f"</div>")
        card.setStyleSheet(f"background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px;")
        card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return card

    def update_kpi_card(self, card: QLabel, title: str, value: str, color: str):
        card.setText(f"<div style='text-align: center;'>"
                     f"<div style='font-size: 14px; color: #7f8c8d;'>{title}</div>"
                     f"<div style='font-size: 24px; font-weight: bold; color: {color};'>{value}</div>"
                     f"</div>")

    def create_proxy_model(self, df: pd.DataFrame) -> QSortFilterProxyModel:
        model = PandasModel(df)
        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(model)
        proxy.setFilterKeyColumn(-1) 
        proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxies.append(proxy)
        return proxy

    def display_results(self, results: dict):
        self.current_results = results
        self.proxies.clear() 
        self.search_bar.clear() 

        df_exact = results['matched_exact']
        df_tol = results.get('matched_tolerance', pd.DataFrame())
        df_fuzzy = results.get('matched_fuzzy', pd.DataFrame())
        df_unmatched_a = results['unmatched_a']
        df_unmatched_b = results['unmatched_b']

        self.update_kpi_card(self.lbl_matched, "Exact Matches", str(len(df_exact)), "#27ae60")
        self.update_kpi_card(self.lbl_tol, "Tolerance Matches", str(len(df_tol)), "#8e44ad")
        self.update_kpi_card(self.lbl_fuzzy, "Fuzzy Matches", str(len(df_fuzzy)), "#2980b9")
        self.update_kpi_card(self.lbl_unmatched_a, "Unmatched (A)", str(len(df_unmatched_a)), "#e74c3c")
        self.update_kpi_card(self.lbl_unmatched_b, "Unmatched (B)", str(len(df_unmatched_b)), "#e67e22")

        self.table_matched.setModel(self.create_proxy_model(df_exact))
        self.table_tol.setModel(self.create_proxy_model(df_tol))
        self.table_fuzzy.setModel(self.create_proxy_model(df_fuzzy))
        self.table_unmatched_a.setModel(self.create_proxy_model(df_unmatched_a))
        self.table_unmatched_b.setModel(self.create_proxy_model(df_unmatched_b))

    def filter_tables(self, text):
        search_pattern = f".*{text}.*" if text else ""
        first_match_index = -1
        
        for index, proxy in enumerate(self.proxies):
            proxy.setFilterRegularExpression(search_pattern)
            if text and first_match_index == -1 and proxy.rowCount() > 0:
                first_match_index = index
                
        if first_match_index != -1:
            self.tabs.setCurrentIndex(first_match_index)

    def export_data(self):
        if not self.current_results: return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Reconciliation Report", "ReconcileX_Report.xlsx", "Excel Files (*.xlsx)")
        if file_path:
            try:
                export_to_excel(self.current_results, file_path)
                QMessageBox.information(self, "Success", f"Report successfully saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to save report.\nError: {str(e)}")

    def close_application(self):
        sys.exit()