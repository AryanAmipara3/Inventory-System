Inventory Management System
===========================

A powerful and user-friendly desktop application built with PySide6 and MySQL to manage users, products, inventory, goods receiving, and sales efficiently. Designed for small to medium-sized businesses with role-based access (admin/operator).

Features
--------
- Secure login authentication with hashed passwords
- User and role management (Admin, Operator)
- Product master and inventory management
- Low-stock alerts and minimum stock setup
- Goods receiving with stock updates
- Sales module with real-time inventory deduction
- Fully responsive UI with optimized usability
- Modern, minimal, and intuitive design

Technologies Used
-----------------
- Python 3.11+
- PySide6 (for the GUI)
- PyMySQL (for MySQL connectivity)
- MySQL (as the database backend)

Getting Started
---------------

Prerequisites:
- Python 3.11+
- MySQL Server installed and running
- A database named 'inventory_system' with required tables (schema should be created beforehand)

Installation:
1. Clone the repository:
   git clone https://github.com/AryanAmipara3/Inventory-System.git
   cd inventory-system

2. Create a virtual environment:
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   python main.py

OR use the pre-built .exe file from the 'dist/' folder to run without needing Python.

File Structure
--------------

main.py
db.py
config.py
dashboard.py
app_style.py
requirements.txt

modules/
- product_master.py
- goods_receiving.py
- inventory.py
- sales.py
- user_master.py

auth/
- login_window.py
- register_users.py

utils/
- hash_utils.py

Demo
----
Check out the screenshots and demo here:
Live Demo Page: https://aryanallprojects.prolbox.com/projects/Inventory_Management_System.html

Author
------
Developed by Aryan Amipara
Portfolio: https://aryanamipara.prolbox.com