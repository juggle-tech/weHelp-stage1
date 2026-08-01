import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling
from mysql.connector.errors import PoolError

## Database setup
load_dotenv()  # Retrieve DB variables in .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


dbconfig = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=3,
    pool_reset_session=True,
    **dbconfig
)


def get_user_by_id(user_id: int):
    """Get connection from pool, query data, then return connection to pool"""
    try:
        cnx = cnxpool.get_connection()
    except PoolError:
        # Connection pool is full
        raise RuntimeError("Connection pool is currently full, please try again later")

    try:
        # Create a cursor, results returned as dicts
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM member WHERE id = %s", (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    finally:
        cnx.close()


if __name__ == "__main__":
    print(get_user_by_id(1))

    connections = []
    for i in range(3):
        connections.append(cnxpool.get_connection())
        print(f"Successfully borrowed connection #{ i+1 }")