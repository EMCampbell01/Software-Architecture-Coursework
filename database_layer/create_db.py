import sqlite3

ambulances = [
    {
        'ambulance_id': 'A1',
        'latitude': 55.921714,
        'longitude': -3.135593,
        'available': True,
    },
    {
        'ambulance_id': 'A2',
        'latitude': 55.921714,
        'longitude': -3.135593,
        'available': True,
    },
    {
        'ambulance_id': 'A3',
        'latitude': 55.921714,
        'longitude': -3.135593,
        'available': True,
    },
]

hospitals = [
    {
        'hospital_name': 'Royal Infirmary of Edinburgh',
        'latitude': 55.921714,
        'longitude': -3.135593,
    },
    {
        'hospital_name': 'Western General Hospital',
        'latitude': 55.962007,
        'longitude': -3.235019,
    },
    {
        'hospital_name': 'Royal Hospital Edinburgh',
        'latitude': 55.927011,
        'longitude': -3.216282,
    },
]

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

        # Insert ambulances into the Ambulances table
        insert_ambulances_query = """
        INSERT INTO Ambulances (ambulance_id, latitude, longitude, available)
        VALUES (?, ?, ?, ?);
        """
        for ambulance in ambulances:
            cursor.execute(
                insert_ambulances_query,
                (ambulance['ambulance_id'], ambulance['latitude'], ambulance['longitude'], ambulance['available'])
            )
        print("Ambulances added to the database.")

        # Insert hospitals into the Hospitals table
        insert_hospitals_query = """
        INSERT INTO Hospitals (hospital_name, latitude, longitude)
        VALUES (?, ?, ?);
        """
        for hospital in hospitals:
            cursor.execute(
                insert_hospitals_query,
                (hospital['hospital_name'], hospital['latitude'], hospital['longitude'])
            )
        print("Hospitals added to the database.")

        # Commit the changes
        conn.commit()

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
    db_file = 'database.db'  # Use '.db' for SQLite database files
    create_database_from_schema(sql_file_path, db_file)
