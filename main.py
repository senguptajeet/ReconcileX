import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Initialize the native desktop application
    app = QApplication(sys.argv)
    
    # Force PyInstaller to bundle the SVG rendering engine for the dropdown arrows
    import PySide6.QtSvg 

    # Load the Bootstrap 5 QSS theme
    style_path = os.path.join(os.path.dirname(__file__), "assets", "style.qss")
    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Warning: Stylesheet not found at {style_path}. Using default system styles.")

    # Launch the main UI window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()