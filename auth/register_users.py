# This File is to be only run once to create initial users
# It should not be run again after the initial setup
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db import get_connection
from utils.hash_utils import hash_password

def create_initial_users():
    users = [
        ("admin", "admin123", "admin"),
        ("operator1", "operator123", "operator"),
        ("operator2", "operator456", "operator"),
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for username, password, role in users:
        try:
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                           (username, hash_password(password), role))
        except Exception as e:
            print(f"Skipping {username}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_initial_users()