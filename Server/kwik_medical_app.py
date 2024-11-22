from flask import Flask, jsonify, request
import requests

DB_SERVER_URL = 'http://127.0.0.1:4900'

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask Server Running"

@app.route("/save_emergency_call_report", methods=['POST'])
def save_emergency_call_report():
    try:
        data = request.get_json()  # Parse JSON from the request body
        print(f'data: {data}')  # Log the received data
        response = requests.post(DB_SERVER_URL + '/insert_emergency_call_report', json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 400

@app.route("/save_dispatch_request", methods=['POST'])
def save_dispatch_request():
    """
    API route to save a dispatch request.
    Expects JSON input with required fields: dispatch_id, ambulance_id, hospital_id, call_id.
    """
    try:
        data = request.get_json()  # Parse JSON from the request body
        print(f'Dispatch request data: {data}')  # Log the received data
        
        # Forward the data to the database API's insert dispatch request route
        response = requests.post(DB_SERVER_URL + '/insert_dispatch_request', json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=4800)

