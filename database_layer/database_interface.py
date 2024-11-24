from flask import Flask, jsonify, request
import sqlite3

class DatabaseInterface:
    def __init__(self, db_file):
        self.db_file = db_file
        
    def execute_query(self, query, params=None):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        return cursor

    def insert_emergency_call_report(self, call_id, call_number, call_time, call_date, latitude, longitude, incident_type, call_details):
        query = """
        INSERT INTO EmergencyCallReports (call_id, call_number, call_time, call_date, latitude, longitude, incident_type, call_details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute_query(query, (call_id, call_number, call_time, call_date, latitude, longitude, incident_type, call_details))
        
    def get_all_emergency_call_reports(self):
        query = "SELECT * FROM EmergencyCallReports"
        cursor = self.execute_query(query)
        return cursor.fetchall()        
    
    def get_emergency_call_report(self, id):
        query = "SELECT * FROM EmergencyCallReports WHERE call_id = ?"
        cursor = self.execute_query(query, (id,))
        return cursor.fetchone()

    def insert_dispatch_request(self, dispatch_id, ambulance_id, hospital_name, call_id):
        query = """
        INSERT INTO DispatchRequests (dispatch_id, ambulance_id, hospital_name, call_id)
        VALUES (?, ?, ?, ?)
        """
        self.execute_query(query, (dispatch_id, ambulance_id, hospital_name, call_id))
        
    def get_all_dispatch_requests(self):
        query = "SELECT * FROM DispatchRequests"
        cursor = self.execute_query(query)
        return cursor.fetchall()
    
    def get_dispatch_request(self, id):
        query = "SELECT * FROM DispatchRequests WHERE dispatch_id = ?"
        cursor = self.execute_query(query, (id,))
        return cursor.fetchone()
    
    def get_ambulance_dispatch_requests(self, ambulance_id):
        query = "SELECT * FROM DispatchRequests WHERE ambulance_id = ?"
        cursor = self.execute_query(query, (ambulance_id,))
        return cursor.fetchall()
    
    def insert_ambulance(self, ambulance_id, latitude, longitude, available):
        query = """
        INSERT INTO Ambulances (ambulance_id, latitude, longitude, available)
        VALUES (?, ?, ?, ?)
        """
        self.execute_query(query, (ambulance_id, latitude, longitude, available))
        
    def get_all_ambulances(self):
        query = "SELECT * FROM Ambulances"
        cursor = self.execute_query(query)
        return cursor.fetchall()
    
    def get_ambulance(self, id):
        query = "SELECT * FROM Ambulances WHERE ambulance_id = ?"
        cursor = self.execute_query(query, (id,))
        return cursor.fetchone()
    
    def insert_hospital(self, hospital_name, latitude, longitude):
        query = """
        INSERT INTO Hospitals (hospital_name, latitude, longitude)
        VALUES (?, ?, ?)
        """
        self.execute_query(query, (hospital_name, latitude, longitude))

    def get_all_hospitals(self):
        query = "SELECT * FROM Hospitals"
        cursor = self.execute_query(query)
        return cursor.fetchall()
    
    def get_hospital(self, hospital_name):
        query = "SELECT * FROM Hospitals WHERE hospital_name = ?"
        cursor = self.execute_query(query, (hospital_name,))
        return cursor.fetchone()

app = Flask(__name__)
database_interface = DatabaseInterface('database.db')

@app.route("/emergency_call_reports", methods=['GET', 'POST'])
def emergency_call_reports():

    # Insert emergency call report
    if request.method == 'POST':
        
        data = request.get_json()
        try:
            
            print(f'data: {data}')
            
            call_id = data['call_id']
            call_number = data['call_number']
            call_time = data['call_time']
            call_date = data['call_date']
            latitude = data['latitude']
            longitude = data['longitude']
            incident_type = data['incident_type']
            call_details = data['call_details']
            
            database_interface.insert_emergency_call_report(call_id, call_number, call_time, call_date, latitude, longitude, incident_type, call_details)
            print('Emergency call report added')
            return '', 201
        
        except:
            print('Failed to add emergency call report')
            return '', 500
    
    # Return all emergency call reports
    elif request.method == 'GET':
    
        try:
            rows = database_interface.get_all_emergency_call_reports()
            columns = ["call_id", "call_number", "call_time", "call_date", "latitude", "longitude", "incident_type", "call_details"]
            emergency_call_reports = [dict(zip(columns, row)) for row in rows]

            print(f'emergency_call_reports: {emergency_call_reports}')
            return jsonify(emergency_call_reports)
        
        except:
            print('Failed to return emergency call reports')
            return '', 500

@app.route("/emergency_call_report/<id>", methods=['GET'])
def emergency_call_report(id):
    
    try:
        row = database_interface.get_emergency_call_report(id)
        if row:
            columns = ["call_id", "call_number", "call_time", "call_date", "latitude", "longitude", "incident_type", "call_details"]
            emergency_call_report = dict(zip(columns, row))
            print(f'emergency_call_report: {emergency_call_report}')
            return jsonify(emergency_call_report)
        else:
            print(f'No emergency call report found for ID: {id}')
            return '', 404
        
    except Exception as e:
        print(f'Failed to return emergency call report for ID {id}: {e}')
        return '', 500     

@app.route("/dispatch_requests", methods=['GET', 'POST'])
def dispatch_requests():

    # Insert dispatch request
    if request.method == 'POST':
        
        data = request.get_json()
        print(f'data: {data}')
        try:
            dispatch_id = data['dispatch_id']
            ambulance_id = data['ambulance_id']
            hospital = data['hospital']
            call_id = data['call_id']
            
            database_interface.insert_dispatch_request(dispatch_id, ambulance_id, hospital, call_id)
            print('Dispatch request added')
            return '', 201  
            
        except Exception as e:
            print(f'Failed to add dispatch request: {e}')
            return '', 500
    
    # Return all dispatch requests    
    elif request.method == 'GET':
        
        try:
            rows = database_interface.get_all_dispatch_requests()
            columns = ["dispatch_id", "ambulance_id", "hospital_name", "call_id"]
            dispatch_requests = [dict(zip(columns, row)) for row in rows]
            
            print(f'dispatch_requests: {dispatch_requests}')
            return jsonify(dispatch_requests)
    
        except:
            print('Failed to return dispatch requests')
            return '', 500

@app.route("/dispatch_request/<id>", methods=['GET'])
def dispatch_request(id):
    try:
        row = database_interface.get_dispatch_request(id)
        if row:
            columns = ["dispatch_id", "ambulance_id", "hospital_name", "call_id"]
            dispatch_request = dict(zip(columns, row))
            print(f'dispatch_request: {dispatch_request}')
            return jsonify(dispatch_request)
        else:
            print(f'No dispatch request found for ID: {id}')
            return '', 404

    except Exception as e:
        print(f'Failed to return dispatch request for ID {id}: {e}')
        return '', 500
    
@app.route("/ambulance_dispatch_requests/<ambulance_id>", methods=['GET'])
def ambulance_dispatch_requests(ambulance_id):
    try:
        rows = database_interface.get_ambulance_dispatch_requests(ambulance_id)
        if rows:
            columns = ["dispatch_id", "ambulance_id", "hospital_name", "call_id"]
            dispatch_requests = [dict(zip(columns, row)) for row in rows]
            print(f'dispatch_requests for ambulance_id {ambulance_id}: {dispatch_requests}')
            return jsonify(dispatch_requests)
        else:
            print(f'No dispatch requests found for ambulance_id: {ambulance_id}')
            return jsonify([])

    except Exception as e:
        print(f'Failed to fetch dispatch requests for ambulance_id {ambulance_id}: {e}')
        return '', 500
    
@app.route("/ambulances", methods=['GET', 'POST'])
def ambulances():

    # Insert ambulance
    if request.method == 'POST':
        
        data = request.get_json()
        try:
            ambulance_id = data['ambulance_id']
            latitude = data['latitude']
            longitude = data['longitude']
            available = data['available']
            
            database_interface.insert_ambulance(ambulance_id, latitude, longitude, available)
            print(f'Ambulance added')
            return '', 201
            
        except:
            print('Failed to add ambulance')
            return '', 500
    
    # Return all ambulances
    elif request.method == 'GET':
        
        try:
            rows = database_interface.get_all_ambulances()
            columns = ["ambulance_id", "latitude", "longitude", "available"]
            ambulances = [dict(zip(columns, row)) for row in rows]
            
            return jsonify(ambulances)
        
        except:
            print('Failed to add ambulance')
            return '', 500

@app.route("/hospitals", methods=['GET', 'POST'])
def hospitals():
    
    # Insert hospital
    if request.method == 'POST':
        
        data = request.get_json()
        try:
            hospital_name = data['hospital_name']
            latitude = data['latitude']
            longitude = data['longitude']
            
            database_interface.insert_hospital(hospital_name, latitude, longitude)
            print(f'Hospital added')
            return '', 201
            
        except:
            print('Failed to add hospital')
            return '', 500
    
    # Return all hospitals
    elif request.method == 'GET':
        
        try:
            rows = database_interface.get_all_hospitals()
            columns = ["hospital_name", "latitude", "longitude"]
            ambulances = [dict(zip(columns, row)) for row in rows]
            
            return jsonify(ambulances)
        
        except:
            print('Failed to add hospital')
            return '', 500

if __name__ == "__main__":
    app.run(debug=True, port=4900)

