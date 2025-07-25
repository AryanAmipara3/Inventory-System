from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QFormLayout, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt
from db import get_connection

class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Form")
        self.setMinimumWidth(400)

        # Title Label
        self.title_label = QLabel("New Sale Entry")
        self.title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        self.customer_input = QLineEdit()
        self.customer_input.setPlaceholderText("Enter Customer Name")

        self.product_dropdown = QComboBox()
        self.product_dropdown.setPlaceholderText("Select Product")
        self.product_dropdown.setStyleSheet("padding: 5px;")

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter Quantity")

        self.unit_input = QLineEdit()
        self.unit_input.setReadOnly(True)
        self.unit_input.setStyleSheet("background-color: #f0f0f0;")

        self.price_input = QLineEdit()
        self.price_input.setReadOnly(True)
        self.price_input.setStyleSheet("background-color: #f0f0f0;")

        self.tax_input = QLineEdit()
        self.tax_input.setReadOnly(True)
        self.tax_input.setStyleSheet("background-color: #f0f0f0;")

        self.submit_btn = QPushButton("Submit Sale")
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.submit_btn.clicked.connect(self.submit_sale)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.addRow("Customer Name", self.customer_input)
        form_layout.addRow("Product", self.product_dropdown)
        form_layout.addRow("Quantity", self.quantity_input)
        form_layout.addRow("Unit", self.unit_input)
        form_layout.addRow("Price", self.price_input)
        form_layout.addRow("GST (%)", self.tax_input)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(form_layout)
        main_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(self.submit_btn)

        self.setLayout(main_layout)
        self.load_products()

    def load_products(self):
        self.product_data = {}
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, default_unit, price, gst_tax
            FROM products
        """)
        for pid, name, unit, price, gst in cursor.fetchall():
            self.product_data[name] = {
                "id": pid,
                "unit": unit,
                "price": price,
                "gst": gst
            }
            self.product_dropdown.addItem(name)

        self.product_dropdown.currentTextChanged.connect(self.update_fields)
        self.update_fields()
        cursor.close()
        conn.close()

    def update_fields(self):
        pname = self.product_dropdown.currentText()
        if not pname:
            return
        data = self.product_data[pname]
        self.unit_input.setText(data["unit"])
        self.price_input.setText(str(data["price"]))
        self.tax_input.setText(str(data["gst"]))

    def submit_sale(self):
        customer = self.customer_input.text().strip()
        pname = self.product_dropdown.currentText()
        quantity_str = self.quantity_input.text().strip()

        if not customer or not quantity_str:
            QMessageBox.warning(self, "Missing Data", "Please fill all fields.")
            return

        try:
            quantity = float(quantity_str)
        except ValueError:
            QMessageBox.warning(self, "Invalid Quantity", "Quantity must be a number.")
            return

        product = self.product_data[pname]
        pid = product["id"]
        price = float(product["price"])
        gst = float(product["gst"])

        # Inventory check
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM inventory WHERE product_id = %s", (pid,))
        result = cursor.fetchone()

        if not result:
            QMessageBox.critical(self, "Error", "Product not in stock.")
            return

        current_stock = result[0]

        if quantity > current_stock:
            QMessageBox.warning(self, "Stock Error", f"Only {current_stock} units in stock.")
            return

        total = price * quantity
        total_with_gst = total + (total * gst / 100)

        try:
            cursor.execute("""
                INSERT INTO sales (product_id, customer_name, quantity, price, gst, total_price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (pid, customer, quantity, price, gst, total_with_gst))

            cursor.execute("""
                UPDATE inventory SET quantity = quantity - %s WHERE product_id = %s
            """, (quantity, pid))

            conn.commit()
            QMessageBox.information(self, "Success", f"Sale completed.\nTotal: ₹{total_with_gst:.2f}")
            self.customer_input.clear()
            self.quantity_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            cursor.close()
            conn.close()