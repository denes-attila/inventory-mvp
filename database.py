import sqlite3

def initialize_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staffs (
                    id INTEGER PRIMARY KEY, 
                    name TEXT,
                    role TEXT
                    )


                """)

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY, 
                    name TEXT,
                    type TEXT,
                    status TEXT,
                    assigned_to INTEGER
                    )

    """
    )
    conn.commit()
    conn.close()