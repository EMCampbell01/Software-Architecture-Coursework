from flask import jsonify
import requests
import math
import uuid

DB_SERVER_URL = 'http://127.0.0.1:4900'

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def get_ambulances():

    response = requests.get(DB_SERVER_URL + '/ambulances')
    ambulances = response.json()
    print(f'ambulances: {ambulances}')
    return ambulances

def get_hospitals():
    
    response = requests.get(DB_SERVER_URL + '/hospitals')
    hospitals = response.json()
    print(f'hospitals: {hospitals}')
    return hospitals

def generate_ambulance_request(emergency_call_report):
    print('generate ambulance request')
    print(f'emergency call report: {emergency_call_report}')
    
    call_id = emergency_call_report["call_id"]
    call_lat = emergency_call_report['latitude']
    call_lon = emergency_call_report['longitude']
    
    ambulances = get_ambulances()
    available_ambulances = [ambulance for ambulance in ambulances if ambulance['available'] == True]
    nearest_ambulance = min(
        available_ambulances,
        key=lambda amb: calculate_distance(call_lat, call_lon, amb['latitude'], amb['longitude'])
    )
    print(f'nearest ambulance: {nearest_ambulance}')
    
    hospitals = get_hospitals()
    nearest_hospital = min(
        hospitals,
        key=lambda hospital: calculate_distance(call_lat, call_lon, hospital['latitude'], hospital['longitude'])
    )
    print(f'hospital: {nearest_hospital}')

    hospital = nearest_hospital["hospital_name"]
    ambulance_id = nearest_ambulance["ambulance_id"]
    
    dispatch_request = {
        'dispatch_id': str(uuid.uuid4()),
        'ambulance_id': ambulance_id,
        'hospital': hospital,
        'call_id': call_id
    }
    
    print(f'dispatch request {dispatch_request}')
    return dispatch_request

def process_emergency_call_report(emergency_call_report):
    
    emergency_call_report_data = emergency_call_report.get('emergency_call_report')
    dispatch_ambulance = emergency_call_report.get('dispatch_ambulance')
    
    requests.post(DB_SERVER_URL + '/emergency_call_reports', json=emergency_call_report_data)
    print('posted emergency call report to db')
    
    if dispatch_ambulance:
        ambulance_request = generate_ambulance_request(emergency_call_report_data)
        requests.post(DB_SERVER_URL + '/dispatch_requests', json=ambulance_request)
        print('dispatch request to db')