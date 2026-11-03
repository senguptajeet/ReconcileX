from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QStackedWidget, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from ui.import_screen import ImportScreen
from ui.mapping_screen import MappingScreen
from ui.results_screen import ResultsScreen
from core.file_reader import read_file
from core.column_mapper import suggest_mapping
from workers.recon_worker import ReconciliationWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReconcileX - Smart Excel Reconciliation")
        self.setMinimumSize(1000, 700)

        # Initialize core data holders
        self.df_a = None
        self.df_b = None

        # Setup main layout with Sidebar and Main Content Area
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar ---
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #2c3e50; color: white;")
        sidebar_layout = QVBoxLayout(sidebar)
        
        app_title = QLabel("ReconcileX")
        app_title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px 0;")
        app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        sidebar_layout.addWidget(app_title)
        sidebar_layout.addWidget(QLabel("🏠 Dashboard"))
        sidebar_layout.addWidget(QLabel("➕ New Reconciliation"))
        sidebar_layout.addStretch()
        
        main_layout.addWidget(sidebar)

        # --- Stacked Widget (Handles Screen Switching) ---
        self.stacked_widget = QStackedWidget()
        
        self.import_screen = ImportScreen()
        self.mapping_screen = MappingScreen()
        self.results_screen = ResultsScreen()

        self.stacked_widget.addWidget(self.import_screen)
        self.stacked_widget.addWidget(self.mapping_screen)
        self.stacked_widget.addWidget(self.results_screen)

        main_layout.addWidget(self.stacked_widget)

        # --- Signal Connections ---
        self.import_screen.files_selected.connect(self.handle_files_selected)
        self.mapping_screen.back_requested.connect(self.go_back_to_import)
        self.results_screen.start_new_requested.connect(self.go_back_to_import)
        self.mapping_screen.mapping_confirmed.connect(self.handle_mapping_confirmed)

    def handle_files_selected(self, path_a, path_b):
        try:
            self.df_a = read_file(path_a)
            self.df_b = read_file(path_b)
            
            mapping = suggest_mapping(self.df_a.columns.tolist(), self.df_b.columns.tolist())
            
            self.mapping_screen.populate_columns(
                self.df_a.columns.tolist(), 
                self.df_b.columns.tolist(), 
                mapping
            )
            
            self.stacked_widget.setCurrentWidget(self.mapping_screen)
            
        except Exception as e:
            print(f"Error loading files: {e}")
            QMessageBox.critical(self, "Load Error", f"Failed to load datasets.\nError: {str(e)}")

    def handle_mapping_confirmed(self, mapping_dict, match_columns, tolerance_val, fuzzy_col, fuzzy_thresh):
        print("Starting background reconciliation worker...")
        
        self.mapping_screen.btn_confirm.setText("⏳ Processing... Please wait")
        self.mapping_screen.btn_confirm.setEnabled(False)

        self.worker = ReconciliationWorker(
            df_a=self.df_a, 
            df_b=self.df_b, 
            mapping_dict=mapping_dict, 
            match_columns=match_columns,
            tolerance_val=tolerance_val,
            fuzzy_col=fuzzy_col,
            fuzzy_thresh=fuzzy_thresh
        )
        
        self.worker.finished_success.connect(self.handle_reconciliation_success)
        self.worker.finished_error.connect(self.handle_reconciliation_error)
        self.worker.start()

    def handle_reconciliation_success(self, results):
        print("Reconciliation complete!")
        self.mapping_screen.btn_confirm.setText("Confirm Mapping & Run Reconciliation")
        self.mapping_screen.btn_confirm.setEnabled(True)
        
        self.results_screen.display_results(results)
        self.stacked_widget.setCurrentWidget(self.results_screen)

    def handle_reconciliation_error(self, error_message):
        print(f"Error during reconciliation: {error_message}")
        self.mapping_screen.btn_confirm.setText("Confirm Mapping & Run Reconciliation")
        self.mapping_screen.btn_confirm.setEnabled(True)
        QMessageBox.critical(self, "Reconciliation Error", f"An error occurred during processing:\n{error_message}")

    def go_back_to_import(self):
        """Switches the UI back to the first screen for a new reconciliation."""
        self.stacked_widget.setCurrentWidget(self.import_screen)