from server_functions.process_emergency_call_report import process_emergency_call_report
from server_functions.generate_ambulance_data import generate_ambulance_data
from flask import Blueprint, request

bp = Blueprint('server_routes', __name__)

@bp.route("/submit_emergency_call_report", methods=['POST'])
def save_emergency_call_report():
    
    try:
        data = request.get_json()
        process_emergency_call_report(data)
        return '', 201
        
    except:
        print('Failed to submit emergency call report')
        return '', 500

@bp.route("/dispatch_requests/<ambulance_id>", methods=['GET'])
def dispatch_requests(ambulance_id):
    
    try:
        ambulance_data = generate_ambulance_data(ambulance_id)
        return ambulance_data, 200
         
    except:
        print(f'Failed to generate ambulance data for ambulance {ambulance_id}')
        return '', 500