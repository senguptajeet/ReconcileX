import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QLineEdit, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, Signal

class ImportScreen(QWidget):
    files_selected = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.file_a_path = ""
        self.file_b_path = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Import Datasets")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # --- Dataset A Input ---
        layout.addWidget(QLabel("Dataset A (e.g., Company Sales / System Records):"))
        row_a = QHBoxLayout()
        self.input_a = QLineEdit()
        self.input_a.setReadOnly(True)
        btn_browse_a = QPushButton("Browse...")
        btn_browse_a.clicked.connect(self.browse_file_a)
        row_a.addWidget(self.input_a)
        row_a.addWidget(btn_browse_a)
        layout.addLayout(row_a)

        # --- Dataset B Input ---
        layout.addWidget(QLabel("Dataset B (e.g., Bank Statement / Vendor Records):"))
        row_b = QHBoxLayout()
        self.input_b = QLineEdit()
        self.input_b.setReadOnly(True)
        btn_browse_b = QPushButton("Browse...")
        btn_browse_b.clicked.connect(self.browse_file_b)
        row_b.addWidget(self.input_b)
        row_b.addWidget(btn_browse_b)
        layout.addLayout(row_b)

        layout.addStretch()

        # --- Action Buttons ---
        btn_layout = QHBoxLayout()
        
        self.btn_exit = QPushButton("✖ Exit Application")
        self.btn_exit.setStyleSheet("background-color: #dc3545; color: white; border-color: #dc3545;")
        self.btn_exit.clicked.connect(self.close_application)
        
        self.btn_next = QPushButton("Load and Proceed ➔")
        self.btn_next.setStyleSheet("background-color: #198754; color: white; border-color: #198754;")
        self.btn_next.clicked.connect(self.validate_and_proceed)

        btn_layout.addWidget(self.btn_exit)
        btn_layout.addWidget(self.btn_next)
        layout.addLayout(btn_layout)

    def browse_file_a(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Dataset A", "", "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)")
        if path:
            self.file_a_path = path
            self.input_a.setText(path)

    def browse_file_b(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Dataset B", "", "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)")
        if path:
            self.file_b_path = path
            self.input_b.setText(path)

    def validate_and_proceed(self):
        if not self.file_a_path or not self.file_b_path:
            QMessageBox.warning(self, "Missing Files", "Please select both datasets before proceeding.")
            return
        self.files_selected.emit(self.file_a_path, self.file_b_path)

    def close_application(self):
        sys.exit()