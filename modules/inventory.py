from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QAbstractItemView, QLineEdit, QHBoxLayout, QHeaderView
)
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
from db import get_connection


class Inventory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Overview")
        self.setMinimumSize(800, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }

            QLabel {
                font-weight: bold;
                font-size: 18px;
                padding: 10px;
            }

            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1.5px solid #0078d7;
                background-color: #ffffff;
            }

            QTableWidget {
                background-color: white;
                border-radius: 10px;
                gridline-color: #d0d0d0;
                font-size: 13px;
                alternate-background-color: #f9f9f9;
            }

            QHeaderView::section {
                background-color: #0078d7;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search product...")
        self.search_input.textChanged.connect(self.filter_table)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Product", "Stock", "Min Stock", "Max Sale Limit", "Alert"])
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)

        top_layout = QHBoxLayout()
        label = QLabel("Inventory Stock Overview")
        label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        top_layout.addWidget(label)
        top_layout.addStretch()
        top_layout.addWidget(self.search_input)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_inventory()
        self.table.cellChanged.connect(self.handle_cell_changed)

    def load_inventory(self):
        self.table.blockSignals(True)
        self.low_stock_alerts = []

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.name, i.quantity, i.min_stock
            FROM inventory i
            JOIN products p ON i.product_id = p.id
        """)
        self.rows = cursor.fetchall()

        self.table.setRowCount(len(self.rows))
        for i, (pid, name, stock, min_stock) in enumerate(self.rows):
            max_sale_limit = stock

            # Product Name
            item_name = QTableWidgetItem(name)
            item_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(i, 0, item_name)

            # Stock
            stock_item = QTableWidgetItem(str(stock))
            stock_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(i, 1, stock_item)

            # Min Stock (Editable)
            min_stock_item = QTableWidgetItem(str(min_stock) if min_stock is not None else "0")
            self.table.setItem(i, 2, min_stock_item)

            # Max Sale Limit
            max_sale_item = QTableWidgetItem(str(max_sale_limit))
            max_sale_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(i, 3, max_sale_item)

            # Alert Column
            alert_item = QTableWidgetItem("")
            alert_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(i, 4, alert_item)

            # Color Highlighting
            if min_stock is not None and stock < min_stock:
                alert_item.setText("⚠ Below Min Stock")
                self.low_stock_alerts.append(f"{name} (Stock: {stock}, Min: {min_stock})")
                for col in range(5):
                    self.table.item(i, col).setBackground(QColor("#ffdddd"))
            else:
                for col in range(5):
                    self.table.item(i, col).setBackground(QColor("#ffffff"))

        cursor.close()
        conn.close()
        self.table.blockSignals(False)

        # Show warning only on first load
        if self.low_stock_alerts and not hasattr(self, "initial_alert_shown"):
            self.initial_alert_shown = True
            QMessageBox.warning(
                self, "Low Stock Alert",
                "The following products are below minimum stock:\n\n" + "\n".join(self.low_stock_alerts)
            )

    def handle_cell_changed(self, row, column):
        if column != 2:
            return

        try:
            new_min_stock = float(self.table.item(row, column).text())
            product_name = self.table.item(row, 0).text()

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE inventory SET min_stock = %s WHERE product_id = (SELECT id FROM products WHERE name = %s)",
                (new_min_stock, product_name)
            )
            conn.commit()
            cursor.close()
            conn.close()

            self.load_inventory()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def filter_table(self, text):
        text = text.lower().strip()
        for row in range(self.table.rowCount()):
            product_name = self.table.item(row, 0).text().lower()
            self.table.setRowHidden(row, text not in product_name)