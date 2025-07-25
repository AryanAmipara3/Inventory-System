import pymysql

def get_connection():
    try:
        return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="inventory_system",
        charset='utf8mb4'
    )
    except Exception as e:
        with open("db_error.txt", "w") as f:
            f.write(str(e))
        raise