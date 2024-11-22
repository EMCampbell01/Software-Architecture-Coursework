from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_gps_coords():
    # Return the coordinates for Edinburgh
    return (55.9533, -3.1883)

# This route listens for the 'callout_update' API call
@app.route('/callout_update', methods=['POST'])
def callout_update():
    data = request.get_json()
    data['gps'] = get_gps_coords()

    # Print the received data for callout_update
    print("ambulance_app: Received callout_update data:")
    print(data)

    # Return a success message
    return jsonify({"message": "callout_update received successfully"}), 200

# This route listens for the 'new_callout' API call and forwards it to the app on port 5000
@app.route('/new_callout', methods=['POST'])
def new_callout():
    data = request.get_json()

    # Print the received data for new_callout
    print("ambulance_app: Received new_callout data:")
    print(data)

    # Forward the new_callout to the app on port 5000 (add_address)
    try:
        response = requests.post("http://localhost:5000/add_address", json=data)
        if response.status_code == 201:
            return jsonify({"message": "new_callout forwarded to port 5000"}), 200
        else:
            print(f"Failed to forward new_callout. Status code: {response.status_code}")
            return jsonify({"error": "Failed to forward to port 5000"}), 500
    except requests.exceptions.RequestException as e:
        print(f"Error forwarding data: {e}")
        return jsonify({"error": "Error forwarding to port 5000"}), 500

# Function to start the Flask app
def run_flask_app():
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=4000)

if __name__ == "__main__":
    # Start the Flask app on port 4000
    run_flask_app()

