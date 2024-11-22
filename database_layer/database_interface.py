from flask import Flask, jsonify, request
import sqlite3

class DatabaseInterface:
    def __init__(self, db_file):
        self.db_file = db_file
        
    def execute_query(self, query, params=None):
        """
        Executes a query with the provided parameters.
        Returns the cursor for operations like fetching or getting the last row ID.
        """
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        return cursor

    def insert_emergency_call(self, call_id, call_number, call_time, call_date, call_location, incident_type, call_details):
        query = """
        INSERT INTO EmergencyCallReports (call_id, call_number, call_time, call_date, call_location, incident_type, call_details)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.execute_query(query, (call_id, call_number, call_time, call_date, call_location, incident_type, call_details))

    def insert_dispatch_request(self, dispatch_id, ambulance_id, hospital_id, call_id):
        query = """
        INSERT INTO DispatchRequests (dispatch_id, ambulance_id, hospital_id, call_id)
        VALUES (?, ?, ?, ?)
        """
        self.execute_query(query, (dispatch_id, ambulance_id, hospital_id, call_id))

app = Flask(__name__)
database_interface = DatabaseInterface('database')

# Emergency Call Report Routes
@app.route("/insert_emergency_call_report", methods=['POST'])
def insert_emergency_call_report():
    """
    API endpoint to add an emergency call report.
    Expects JSON input with the required fields.
    """
    data = request.get_json()  # Parse JSON from the request body
    try:
        call_id = data['call_id']
        call_number = data['call_number']
        call_time = data['call_time']
        call_date = data['call_date']
        call_location = data['call_location']
        incident_type = data['incident_type']
        call_details = data['call_details']
        
        database_interface.insert_emergency_call(call_id, call_number, call_time, call_date, call_location, incident_type, call_details)
        
        return jsonify({'success': True, 'message': 'Emergency call report added.'}), 201
    except KeyError as e:
        return jsonify({'success': False, 'message': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route("/emergency_call_reports", methods=['GET'])
def get_emergency_call_reports():
    """
    API endpoint to fetch all emergency call reports.
    Returns all records from the EmergencyCallReports table as JSON.
    """
    try:
        query = "SELECT * FROM EmergencyCallReports"
        cursor = database_interface.execute_query(query)
        rows = cursor.fetchall()
        
        columns = ["call_id", "call_number", "call_time", "call_date", "call_location", "incident_type", "call_details"]
        reports = [dict(zip(columns, row)) for row in rows]
        
        return jsonify({'success': True, 'data': reports}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# Dispatch Request Routes
@app.route("/insert_dispatch_request", methods=['POST'])
def insert_dispatch_request():
    """
    API endpoint to add a dispatch request.
    Expects JSON input with the required fields.
    """
    data = request.get_json()
    try:
        dispatch_id = data['dispatch_id']
        ambulance_id = data['ambulance_id']
        hospital_id = data['hospital_id']
        call_id = data['call_id']
        
        database_interface.insert_dispatch_request(dispatch_id, ambulance_id, hospital_id, call_id)
        
        return jsonify({'success': True, 'message': 'Dispatch request added.'}), 201
    except KeyError as e:
        return jsonify({'success': False, 'message': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route("/dispatch_requests", methods=['GET'])
def get_dispatch_requests():
    """
    API endpoint to fetch all dispatch requests.
    Returns all records from the DispatchRequests table as JSON.
    """
    try:
        query = "SELECT * FROM DispatchRequests"
        cursor = database_interface.execute_query(query)
        rows = cursor.fetchall()
        
        columns = ["dispatch_id", "ambulance_id", "hospital_id", "call_id"]
        requests = [dict(zip(columns, row)) for row in rows]
        
        return jsonify({'success': True, 'data': requests}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=4900)

