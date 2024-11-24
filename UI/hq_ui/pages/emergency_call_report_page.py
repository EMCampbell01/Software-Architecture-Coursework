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

    # Latitude
    latitude_label = ttk.Label(dispatch_frame, text="Latitude:")
    latitude_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    latitude_entry = ttk.Entry(dispatch_frame, width=40)
    latitude_entry.grid(row=1, column=1, padx=10, pady=10)

    # Longitude
    longitude_label = ttk.Label(dispatch_frame, text="Longitude:")
    longitude_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    longitude_entry = ttk.Entry(dispatch_frame, width=40)
    longitude_entry.grid(row=2, column=1, padx=10, pady=10)

    # Incident Type
    incident_label = ttk.Label(dispatch_frame, text="Incident Type:")
    incident_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    incident_entry = ttk.Entry(dispatch_frame, width=40)
    incident_entry.grid(row=3, column=1, padx=10, pady=10)

    # Call Details
    details_label = ttk.Label(dispatch_frame, text="Call Details:")
    details_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    details_text = tk.Text(dispatch_frame, width=40, height=10)
    details_text.grid(row=4, column=1, padx=10, pady=10)

    # Buttons
    def submit_call_report(dispatch_ambulance):
        # Collect data from the input fields
        call_number = call_number_entry.get()
        latitude = latitude_entry.get()
        longitude = longitude_entry.get()
        incident_type = incident_entry.get()
        call_details = details_text.get("1.0", tk.END).strip()

        # Validate fields
        if not call_number or not latitude or not longitude or not incident_type or not call_details:
            print("All fields must be filled out!")
            return

        # Prepare the data payload
        data = {
            "emergency_call_report": {   
                "call_id": str(uuid.uuid4()),
                "call_time": datetime.now().strftime("%H:%M:%S"),
                "call_date": datetime.now().strftime("%Y-%m-%d"),
                "call_number": call_number,
                "latitude": float(latitude),
                "longitude": float(longitude),
                "incident_type": incident_type,
                "call_details": call_details
            },
            "dispatch_ambulance": dispatch_ambulance
        }

        # Send POST request to the API
        try:
            requests.post(SERVER_URL + '/submit_emergency_call_report', json=data)
            print("Call report submitted successfully!")
        except:
            print("Failed to submit call report")
        finally:
            # Clear all fields after submission
            call_number_entry.delete(0, tk.END)
            latitude_entry.delete(0, tk.END)
            longitude_entry.delete(0, tk.END)
            incident_entry.delete(0, tk.END)
            details_text.delete("1.0", tk.END)

    submit_button = ttk.Button(dispatch_frame, text="Submit Call Report", command=lambda: submit_call_report(False))
    submit_button.grid(row=5, column=0, padx=10, pady=20, sticky="e")

    submit_and_dispatch_button = ttk.Button(dispatch_frame, text="Submit Call Report and Dispatch Ambulance", command=lambda: submit_call_report(True))
    submit_and_dispatch_button.grid(row=5, column=1, padx=10, pady=20, sticky="w")
