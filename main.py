import sys
from PySide6.QtWidgets import QApplication
from auth.login_window import LoginWindow
from app_style import apply_theme

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_theme(app)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())