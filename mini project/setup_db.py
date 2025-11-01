from db_connect import create_tables

def setup_database():
    """
    Set up the database with all required tables.
    """
    print("Setting up database...")
    create_tables()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()