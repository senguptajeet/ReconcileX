from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QScrollArea, QFrame, QLineEdit, QMessageBox)
from PySide6.QtCore import Qt, Signal

class MappingScreen(QWidget):
    # Sends back: mapping_dict, match_columns, tolerance_val, fuzzy_col, fuzzy_thresh
    mapping_confirmed = Signal(dict, list, float, str, int)
    back_requested = Signal()

    def __init__(self):
        super().__init__()
        self.columns_a = []
        self.columns_b = []
        self.mapping_dropdowns = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Map Columns & Settings")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # --- Settings Panel ---
        settings_frame = QFrame()
        settings_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;")
        settings_layout = QVBoxLayout(settings_frame)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Amount Tolerance ($):"))
        self.input_tolerance = QLineEdit("0.00")
        row1.addWidget(self.input_tolerance)
        row1.addStretch()
        settings_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Fuzzy Match Column:"))
        self.dropdown_fuzzy_col = QComboBox()
        self.dropdown_fuzzy_col.addItem("None")
        row2.addWidget(self.dropdown_fuzzy_col)
        
        row2.addWidget(QLabel("   Fuzzy Threshold (0-100):"))
        self.input_fuzzy_thresh = QLineEdit("85")
        row2.addWidget(self.input_fuzzy_thresh)
        row2.addStretch()
        settings_layout.addLayout(row2)

        layout.addWidget(settings_frame)

        # --- Dynamic Mapping Area ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # --- Action Buttons ---
        btn_layout = QHBoxLayout()
        
        self.btn_back = QPushButton("← Back to Import")
        self.btn_back.setStyleSheet("background-color: #6c757d; color: white; border-color: #6c757d;")
        self.btn_back.clicked.connect(self.back_requested.emit)
        
        self.btn_confirm = QPushButton("Confirm Mapping & Run Reconciliation")
        self.btn_confirm.setStyleSheet("background-color: #0d6efd; color: white; border-color: #0d6efd;")
        self.btn_confirm.clicked.connect(self.emit_mapping)
        
        btn_layout.addWidget(self.btn_back)
        btn_layout.addWidget(self.btn_confirm)
        layout.addLayout(btn_layout)

    def populate_columns(self, cols_a, cols_b, suggested_mapping):
        self.columns_a = cols_a
        self.columns_b = cols_b
        self.mapping_dropdowns.clear()

        # Update Fuzzy Column Dropdown
        self.dropdown_fuzzy_col.clear()
        self.dropdown_fuzzy_col.addItem("None")
        self.dropdown_fuzzy_col.addItems(cols_b)

        # Clear existing dynamic rows
        for i in reversed(range(self.scroll_layout.count())): 
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Build new dynamic rows
        for col_b in cols_b:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            
            lbl_b = QLabel(f"Dataset B: <b>{col_b}</b>")
            lbl_arrow = QLabel("➔ Maps to:")
            
            combo_a = QComboBox()
            combo_a.addItem("--- Do Not Map ---")
            combo_a.addItems(cols_a)
            
            if col_b in suggested_mapping:
                index = combo_a.findText(suggested_mapping[col_b])
                if index >= 0:
                    combo_a.setCurrentIndex(index)
                    
            self.mapping_dropdowns[col_b] = combo_a
            
            row_layout.addWidget(lbl_b)
            row_layout.addWidget(lbl_arrow)
            row_layout.addWidget(combo_a)
            self.scroll_layout.addWidget(row_widget)
            
        self.scroll_layout.addStretch()

    def emit_mapping(self):
        mapping_dict = {}
        match_columns = []
        
        for col_b, combo_a in self.mapping_dropdowns.items():
            mapped_val = combo_a.currentText()
            if mapped_val != "--- Do Not Map ---":
                mapping_dict[col_b] = mapped_val
                match_columns.append(mapped_val)

        if not mapping_dict:
            QMessageBox.warning(self, "No Mapping", "Please map at least one column before proceeding.")
            return

        try:
            tol_val = float(self.input_tolerance.text() or 0.0)
            fuz_thresh = int(self.input_fuzzy_thresh.text() or 85)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for Tolerance and Threshold.")
            return

        fuzzy_col_b = self.dropdown_fuzzy_col.currentText()
        fuzzy_col_mapped = None
        
        if fuzzy_col_b != "None":
            if fuzzy_col_b in mapping_dict:
                fuzzy_col_mapped = mapping_dict[fuzzy_col_b]
            else:
                QMessageBox.warning(self, "Invalid Fuzzy Column", "The selected fuzzy column must be mapped to Dataset A.")
                return

        self.mapping_confirmed.emit(mapping_dict, match_columns, tol_val, fuzzy_col_mapped, fuz_thresh)