from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QMessageBox, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.goods_receiving import GoodsReceiving
from modules.user_master import UserMaster
from modules.product_master import ProductMaster
from modules.inventory import Inventory
from modules.sales import SalesForm


class Dashboard(QWidget):
    def __init__(self, role, username):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setMinimumSize(600, 400)
        self.role = role
        self.username = username

        self.setStyleSheet("""
            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QLabel#subLabel {
                font-size: 14px;
                color: gray;
                margin-bottom: 20px;
            }
            QPushButton {
                font-size: 15px;
                padding: 12px;
                border-radius: 8px;
                background-color: #448aff;
                color: white;
            }
            QPushButton:hover {
                background-color: #1a73e8;
            }
        """)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        # Title
        self.title_label = QLabel("Dashboard")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.sub_label = QLabel(f"Welcome, {self.username} ({self.role.capitalize()})")
        self.sub_label.setObjectName("subLabel")
        self.sub_label.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.sub_label)

        # Button Grid
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)

        buttons = []
        if self.role == "admin":
            buttons.append("User Master")
        if self.role in ["admin", "operator"]:
            buttons += ["Product Master", "Goods Receiving", "Inventory", "Sales"]

        for idx, label in enumerate(buttons):
            btn = QPushButton(label)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(lambda _, l=label: self.open_module(l))
            row, col = divmod(idx, 2)
            self.grid_layout.addWidget(btn, row, col)

        main_layout.addLayout(self.grid_layout)
        self.setLayout(main_layout)

    def open_module(self, label):
        if label == "User Master":
            self.module = UserMaster()
        elif label == "Product Master":
            self.module = ProductMaster()
        elif label == "Goods Receiving":
            self.module = GoodsReceiving()
        elif label == "Inventory":
            self.module = Inventory()
        elif label == "Sales":
            self.module = SalesForm()

        self.module.show()