from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from db import get_connection
from utils.hash_utils import check_password
from dashboard import Dashboard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Inventory System")
        self.setMinimumSize(400, 300)
        self.setStyleSheet("""
            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            QLineEdit:focus {
                border: 1px solid #448aff;
            }
            QPushButton {
                padding: 10px;
                font-size: 14px;
                border-radius: 8px;
                background-color: #448aff;
                color: white;
            }
            QPushButton:hover {
                background-color: #1a73e8;
            }
        """)

        # Title
        self.title_label = QLabel("Login")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)

        # Centered layout
        form_layout = QVBoxLayout()
        form_layout.addStretch()
        form_layout.addWidget(self.title_label)
        form_layout.addSpacing(15)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.login_btn)
        form_layout.addStretch()
        form_layout.setContentsMargins(40, 20, 40, 20)

        self.setLayout(form_layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, role FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and check_password(password, result[0]):
            role = result[1]
            self.dashboard = Dashboard(role, username)
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")