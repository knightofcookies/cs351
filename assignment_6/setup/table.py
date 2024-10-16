import pymysql

# Database connection details
HOST = 'feedback-db-3.cdgsei4a4cwp.ap-south-1.rds.amazonaws.com'
USER = 'flaskapp'
PASSWORD = 'flaksapp'
NAME = 'feedback-db-3'

# Connect to the database
connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD)
cursor = connection.cursor()

# Create database enclosing the database name in backticks
cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{NAME}`")
cursor.execute(f"USE `{NAME}`")

# Create table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    message TEXT NOT NULL
)
"""
cursor.execute(CREATE_TABLE_SQL)

cursor.close()
connection.close()
