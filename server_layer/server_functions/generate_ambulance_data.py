from flask import jsonify
import requests

DB_SERVER_URL = 'http://127.0.0.1:4900'

def generate_ambulance_data(ambulance_id):
    
    response = requests.get(DB_SERVER_URL + '/ambulance_dispatch_requests/' + ambulance_id)
    ambulance_dispatch_requests = response.json()
    
    ambulance_data = []
    for dispatch_request in ambulance_dispatch_requests:
        
        call_id = dispatch_request['call_id']
        response = requests.get(DB_SERVER_URL + '/emergency_call_report/' + call_id)
        emergency_call_report = response.json()
        
        location = (emergency_call_report.get('latitude'), emergency_call_report.get('longitude'))
        destination = dispatch_request.get('hospital_name')
        incident_type = emergency_call_report.get('incident_type')
        call_details = emergency_call_report.get('call_details')
        
        ambulance_data.append(
            {
                'location': location,
                'destination': destination,
                'incident_type': incident_type,
                'call details': call_details
            }
        )
    
    return jsonify(ambulance_data)
        
