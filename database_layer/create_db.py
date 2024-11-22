import sqlite3
import os

def create_database_from_schema(sql_file, db_file):

    try:
        # Read the schema from the SQL file
        with open(sql_file, 'r') as file:
            schema = file.read()

        # Connect to SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Execute the schema
        cursor.executescript(schema)
        print(f"Database created successfully at '{db_file}'")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    sql_file_path = 'schema.sql'
    db_file = 'database'
    create_database_from_schema(sql_file_path, db_file)
