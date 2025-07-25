from PySide6.QtWidgets import (
    QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem,
    QFormLayout, QHeaderView
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from db import get_connection

class GoodsReceiving(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goods Receiving")
        self.setMinimumSize(800, 600)
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
                border: 1px solid #448aff;
                background-color: #f0f8ff;
            }
            QPushButton {
                padding: 10px 16px;
                border-radius: 6px;
                background-color: #448aff;
                color: white;
            }
            QPushButton:hover {
                background-color: #3A7AFE;
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

        self.product_box = QComboBox()
        self.product_box.setPlaceholderText("Select Product")
        self.supplier_box = QComboBox()
        self.supplier_box.setPlaceholderText("Select Supplier")
        self.unit_input = QLineEdit()
        self.unit_input.setReadOnly(True)
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter Quantity")
        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText("Enter Rate Per Unit")

        self.total_label = QLabel("Total: ₹0.00")
        self.tax_label = QLabel("Tax: ₹0.00")

        self.submit_btn = QPushButton("Receive Goods")
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.clicked.connect(self.receive_goods)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignTop)
        form_layout.setHorizontalSpacing(30)
        form_layout.addRow("Product", self.product_box)
        form_layout.addRow("Supplier", self.supplier_box)
        form_layout.addRow("Quantity", self.quantity_input)
        form_layout.addRow("Unit", self.unit_input)
        form_layout.addRow("Rate Per Unit", self.rate_input)
        form_layout.addRow(self.total_label)
        form_layout.addRow(self.tax_label)
        form_layout.addRow(self.submit_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Product", "Supplier", "Qty", "Rate", "Total", "Tax"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("alternate-background-color: #f2f2f2; background-color: white;")
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addLayout(form_layout)
        layout.addSpacing(20)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_dropdowns()
        self.load_receivings()

        self.quantity_input.textChanged.connect(self.calculate_total)
        self.rate_input.textChanged.connect(self.calculate_total)

    def load_dropdowns(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM products")
        self.products = cursor.fetchall()
        self.product_box.clear()
        for pid, name in self.products:
            self.product_box.addItem(name, pid)

        conn.close()

        # Load suppliers for the first product initially
        self.load_suppliers_by_product()

        # Connect product change to update supplier list
        self.product_box.currentIndexChanged.connect(self.load_suppliers_by_product)

    def load_suppliers_by_product(self):
        product_id = self.product_box.currentData()
        if product_id is None:
            self.supplier_box.clear()
            self.unit_input.clear()
            return

        conn = get_connection()
        cursor = conn.cursor()

        # Fetch supplier
        cursor.execute("""
            SELECT s.id, s.name
            FROM suppliers s
            JOIN products p ON s.id = p.supplier_id
            WHERE p.id = %s
        """, (product_id,))
        suppliers = cursor.fetchall()
        self.supplier_box.clear()
        for sid, name in suppliers:
            self.supplier_box.addItem(name, sid)

        # Fetch unit
        cursor.execute("SELECT default_unit FROM products WHERE id=%s", (product_id,))
        result = cursor.fetchone()
        if result:
            self.unit_input.setText(result[0])
        else:
            self.unit_input.clear()

        conn.close()

    def calculate_total(self):
        try:
            qty = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            product_id = self.product_box.currentData()

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT gst_tax FROM products WHERE id=%s", (product_id,))
            gst = cursor.fetchone()[0]
            conn.close()

            total = qty * rate
            tax_amt = total * gst / 100

            self.total_label.setText(f"Total: ₹{total:.2f}")
            self.tax_label.setText(f"Tax: ₹{tax_amt:.2f}")
        except:
            self.total_label.setText("Total: ₹0.00")
            self.tax_label.setText("Tax: ₹0.00")

    def receive_goods(self):
        try:
            product_id = self.product_box.currentData()
            supplier_id = self.supplier_box.currentData()
            qty = float(self.quantity_input.text())
            unit = self.unit_input.text()
            rate = float(self.rate_input.text())

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT gst_tax FROM products WHERE id=%s", (product_id,))
            gst_tax = cursor.fetchone()[0]

            total = qty * rate
            tax_amt = total * gst_tax / 100

            cursor.execute("""
                INSERT INTO goods_receiving
                (product_id, supplier_id, quantity, unit, rate, total_rate, tax)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (product_id, supplier_id, qty, unit, rate, total, tax_amt))

            cursor.execute("SELECT quantity FROM inventory WHERE product_id=%s", (product_id,))
            row = cursor.fetchone()
            if row:
                new_qty = row[0] + qty
                cursor.execute("UPDATE inventory SET quantity=%s WHERE product_id=%s", (new_qty, product_id))
            else:
                cursor.execute("INSERT INTO inventory (product_id, quantity) VALUES (%s, %s)", (product_id, qty))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Goods received and inventory updated.")
            self.quantity_input.clear()
            self.unit_input.clear()
            self.rate_input.clear()
            self.total_label.setText("Total: ₹0.00")
            self.tax_label.setText("Tax: ₹0.00")

            self.load_receivings()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_receivings(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, s.name, g.quantity, g.rate, g.total_rate, g.tax
            FROM goods_receiving g
            JOIN products p ON g.product_id = p.id
            JOIN suppliers s ON g.supplier_id = s.id
        """)
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()