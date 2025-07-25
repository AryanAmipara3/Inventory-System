from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem,
    QGroupBox, QFormLayout, QSizePolicy, QInputDialog, QHeaderView
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from db import get_connection
from utils.hash_utils import hash_password

class ProductMaster(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Master")
        self.setMinimumSize(800, 775)
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 6px;
            }
            QTextEdit {
                padding: 2px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #3A7AFE;
                background-color: #f0f8ff;
            }
            QPushButton {
                background-color: #3A7AFE;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
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

        # Form Inputs
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Barcode")

        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText("SKU ID")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product Name")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Description")
        self.desc_input.setFixedHeight(100)
        self.desc_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.gst_input = QLineEdit()
        self.gst_input.setPlaceholderText("GST %")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")

        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText("Default Unit (e.g., kg)")

        self.conv_factor_input = QLineEdit()
        self.conv_factor_input.setPlaceholderText("Conversion Factor")

        self.category_box = QComboBox()
        self.category_box.setPlaceholderText("Select Category")
        self.subcategory_box = QComboBox()
        self.subcategory_box.setPlaceholderText("Select Subcategory")
        self.supplier_box = QComboBox()
        self.supplier_box.setPlaceholderText("Select Supplier")

        self.image_path = ""
        self.image_btn = QPushButton("Upload Image")
        self.image_btn.setCursor(Qt.PointingHandCursor)
        self.image_btn.clicked.connect(self.select_image)

        self.add_btn = QPushButton("Add Product")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_product)

        # Form Layout
        form_group = QGroupBox("Product Details")
        form_layout = QFormLayout()
        form_layout.addRow("Barcode:", self.barcode_input)
        form_layout.addRow("SKU ID:", self.sku_input)
        form_layout.addRow("Product Name:", self.name_input)
        form_layout.addRow("Description:", self.desc_input)
        form_layout.addRow("GST %:", self.gst_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Default Unit:", self.unit_input)
        form_layout.addRow("Conversion Factor:", self.conv_factor_input)

        # Category Row
        category_layout = QHBoxLayout()
        category_layout.addWidget(self.category_box)
        add_category_btn = QPushButton("+")
        add_category_btn.setCursor(Qt.PointingHandCursor)
        add_category_btn.setFixedWidth(40)
        add_category_btn.clicked.connect(self.add_category)
        category_layout.addWidget(add_category_btn)
        form_layout.addRow("Category:", category_layout)

        # Subcategory Row
        subcategory_layout = QHBoxLayout()
        subcategory_layout.addWidget(self.subcategory_box)
        add_subcategory_btn = QPushButton("+")
        add_subcategory_btn.setCursor(Qt.PointingHandCursor)
        add_subcategory_btn.setFixedWidth(40)
        add_subcategory_btn.clicked.connect(self.add_subcategory)
        subcategory_layout.addWidget(add_subcategory_btn)
        form_layout.addRow("Subcategory:", subcategory_layout)

        # Supplier Row
        supplier_layout = QHBoxLayout()
        supplier_layout.addWidget(self.supplier_box)
        add_supplier_btn = QPushButton("+")
        add_supplier_btn.setCursor(Qt.PointingHandCursor)
        add_supplier_btn.setFixedWidth(40)
        add_supplier_btn.clicked.connect(self.add_supplier)
        supplier_layout.addWidget(add_supplier_btn)
        form_layout.addRow("Supplier:", supplier_layout)

        form_layout.addRow(self.image_btn)
        form_layout.addRow(self.add_btn)
        form_group.setLayout(form_layout)

        # Table Setup
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "Supplier"])
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(form_group)
        main_layout.addWidget(QLabel("Existing Products:"))
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        self.load_dropdowns()
        self.load_products()

        self.category_box.currentIndexChanged.connect(self.update_subcategories)

    def load_dropdowns(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM categories")
        self.categories = cursor.fetchall()
        self.category_box.clear()
        for cat in self.categories:
            self.category_box.addItem(cat[1], cat[0])

        self.update_subcategories()

        cursor.execute("SELECT id, name FROM suppliers")
        self.suppliers = cursor.fetchall()
        self.supplier_box.clear()
        for sup in self.suppliers:
            self.supplier_box.addItem(sup[1], sup[0])

        conn.close()

    def update_subcategories(self):
        cat_id = self.category_box.currentData()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM subcategories WHERE category_id=%s", (cat_id,))
        self.subcategories = cursor.fetchall()
        self.subcategory_box.clear()
        for sub in self.subcategories:
            self.subcategory_box.addItem(sub[1], sub[0])
        conn.close()

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Product Image")
        if file_path:
            self.image_path = file_path
            QMessageBox.information(self, "Selected", f"Image selected:\n{file_path}")

    def add_product(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO products
                (barcode, sku_id, category_id, subcategory_id, name, description, gst_tax, price,
                 default_unit, conversion_factor, image_path, supplier_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.barcode_input.text(),
                self.sku_input.text(),
                self.category_box.currentData(),
                self.subcategory_box.currentData(),
                self.name_input.text(),
                self.desc_input.toPlainText(),
                float(self.gst_input.text()),
                float(self.price_input.text()),
                self.unit_input.text(),
                float(self.conv_factor_input.text()),
                self.image_path,
                self.supplier_box.currentData()
            ))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Product added successfully.")
            self.clear_inputs()
            self.load_products()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_inputs(self):
        self.barcode_input.clear()
        self.sku_input.clear()
        self.name_input.clear()
        self.desc_input.clear()
        self.gst_input.clear()
        self.price_input.clear()
        self.unit_input.clear()
        self.conv_factor_input.clear()
        self.image_path = ""

    def load_products(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.name, c.name, p.price, s.name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            JOIN suppliers s ON p.supplier_id = s.id
        """)
        products = cursor.fetchall()
        self.table.setRowCount(len(products))
        for i, row in enumerate(products):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()
        
    def add_category(self):
        name, ok = QInputDialog.getText(self, "Add Category", "Enter new category name:")
        if ok and name:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Added", "New category added.")
                self.load_dropdowns()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def add_subcategory(self):
        if self.category_box.currentIndex() == -1:
            QMessageBox.warning(self, "Warning", "Please select a category first.")
            return
        name, ok = QInputDialog.getText(self, "Add Subcategory", "Enter new subcategory name:")
        if ok and name:
            try:
                category_id = self.category_box.currentData()
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO subcategories (name, category_id) VALUES (%s, %s)", (name, category_id))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Added", "New subcategory added.")
                self.update_subcategories()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def add_supplier(self):
        name, ok = QInputDialog.getText(self, "Add Supplier", "Enter new supplier name:")
        if ok and name:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO suppliers (name) VALUES (%s)", (name,))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Added", "New supplier added.")
                self.load_dropdowns()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))