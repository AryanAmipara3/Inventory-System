from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QAbstractItemView, QHeaderView
)
from PySide6.QtCore import Qt
from db import get_connection
from utils.hash_utils import hash_password


class UserMaster(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Master")
        self.setMinimumSize(700, 500)

        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #3A7AFE;
                background-color: #f0f8ff;
            }
            QPushButton {
                padding: 10px 16px;
                border-radius: 6px;
                background-color: #3A7AFE;
                color: white;
            }
            QPushButton:hover {
                background-color: #155EDC;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                font-weight: bold;
                padding: 6px;
            }
            QTableWidget::item {
                padding: 6px;
            }
        """)

        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Form inputs
        form_layout = QHBoxLayout()
        form_layout.setSpacing(10)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.role_input = QComboBox()
        self.role_input.setPlaceholderText("Select Role")
        self.role_input.addItems(["admin", "operator"])

        self.add_btn = QPushButton("Add User")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_user)

        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.role_input)
        form_layout.addWidget(self.add_btn)

        layout.addLayout(form_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Role"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

        # Delete button
        self.delete_btn = QPushButton("Delete Selected User")
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.clicked.connect(self.delete_selected_user)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

    def load_users(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users ORDER BY id ASC")
        users = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(users))
        for row_idx, (uid, username, role) in enumerate(users):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(uid)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(username))
            self.table.setItem(row_idx, 2, QTableWidgetItem(role))

    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                (username, hash_password(password), role)
            )
            conn.commit()
            QMessageBox.information(self, "Success", "User added successfully.")
            self.username_input.clear()
            self.password_input.clear()
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not add user:\n{str(e)}")
        finally:
            cursor.close()
            conn.close()

    def delete_selected_user(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "No user selected.")
            return

        user_id = int(self.table.item(selected, 0).text())
        if user_id == 1:
            QMessageBox.warning(self, "Restricted", "Cannot delete default admin.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Deletion",
            "Are you sure you want to delete this user?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
            conn.commit()
            QMessageBox.information(self, "Deleted", "User removed successfully.")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not delete user:\n{str(e)}")
        finally:
            cursor.close()
            conn.close()