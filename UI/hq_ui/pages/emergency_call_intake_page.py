from datetime import datetime
import requests
from tkinter import ttk
import tkinter as tk
import uuid

SERVER_URL = "http://127.0.0.1:4800"

def create_emergency_call_intake_page(notebook):
    """
    Create the Emergency Call Intake page and add it to the notebook.
    """
    # Page frame
    dispatch_frame = ttk.Frame(notebook)
    notebook.add(dispatch_frame, text="Emergency Call Intake")

    # Labels and Input Fields
    # Call Number
    call_number_label = ttk.Label(dispatch_frame, text="Call Number:")
    call_number_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    call_number_entry = ttk.Entry(dispatch_frame, width=40)
    call_number_entry.grid(row=0, column=1, padx=10, pady=10)

    # Call Location
    location_label = ttk.Label(dispatch_frame, text="Call Location:")
    location_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    location_entry = ttk.Entry(dispatch_frame, width=40)
    location_entry.grid(row=1, column=1, padx=10, pady=10)

    # Incident Type
    incident_label = ttk.Label(dispatch_frame, text="Incident Type:")
    incident_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    incident_entry = ttk.Entry(dispatch_frame, width=40)
    incident_entry.grid(row=2, column=1, padx=10, pady=10)

    # Call Details
    details_label = ttk.Label(dispatch_frame, text="Call Details:")
    details_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    details_text = tk.Text(dispatch_frame, width=40, height=10)
    details_text.grid(row=3, column=1, padx=10, pady=10)

    # Buttons
    def save_call_report():
        # Collect data from the input fields
        call_number = call_number_entry.get()
        location = location_entry.get()
        incident_type = incident_entry.get()
        call_details = details_text.get("1.0", tk.END).strip()

        # Validate fields
        if not call_number or not location or not incident_type or not call_details:
            print("All fields must be filled out!")
            return

        # Prepare the data payload
        data = {
            "call_id": str(uuid.uuid4()),
            "call_time": datetime.now().strftime("%H:%M:%S"),
            "call_date": datetime.now().strftime("%Y-%m-%d"),
            "call_number": call_number,
            "call_location": location,
            "incident_type": incident_type,
            "call_details": call_details
        }

        # Send POST request to the API
        try:
            response = requests.post(SERVER_URL + '/save_emergency_call_report', json=data)
            if response.status_code == 201:
                print("Call report saved successfully!")
                print(response.json())  # Print the API response
            else:
                print(f"Failed to save call report: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to the API: {e}")

    def save_and_dispatch():
        save_call_report()
        print("Dispatching ambulance...")

    save_button = ttk.Button(dispatch_frame, text="Save Call Report", command=save_call_report)
    save_button.grid(row=4, column=0, padx=10, pady=20, sticky="e")

    dispatch_button = ttk.Button(dispatch_frame, text="Save and Dispatch Ambulance", command=save_and_dispatch)
    dispatch_button.grid(row=4, column=1, padx=10, pady=20, sticky="w")
