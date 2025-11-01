import sqlite3
import os
from db_config import DATABASE_NAME

def get_db_connection():
    """
    Create and return a database connection.
    Ensures foreign key constraints are enabled.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db_if_not_exists():
    """
    Initialize the database with tables if they don't exist.
    """
    if not os.path.exists(DATABASE_NAME):
        create_tables()

def create_tables():
    """
    Create all necessary tables in the database.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create expenses table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            notes TEXT
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()