import tkinter as tk
from tkinter import ttk
import requests

# Variable to store the logged-in ambulance ID
current_ambulance_id = None

# Function to fetch dispatch requests
def fetch_dispatch_requests():
    global current_ambulance_id
    if not current_ambulance_id:
        return  # If ambulance ID is not set, do not proceed
    print('Fetching dispatch requests for:', current_ambulance_id)
    try:
        # Use the current ambulance ID in the API endpoint
        response = requests.get(f"http://127.0.0.1:5000/dispatch_requests/{current_ambulance_id}")
        if response.status_code == 200:
            print(response.json())
            update_dispatch_table(response.json())
        else:
            print(f"Failed to fetch dispatch requests: {response.status_code}")
    except Exception as e:
        print(f"Error fetching dispatch requests: {e}")

# Function to update the dispatch table
def update_dispatch_table(data):
    for row in dispatch_table.get_children():
        dispatch_table.delete(row)  # Clear existing rows
    for request in data:
        dispatch_table.insert("", tk.END, values=(
            request["Priority"], 
            request["Incident Type"], 
            request["Location"], 
            request["Destination"]
        ))

# Function to periodically fetch updates
def periodic_update():
    fetch_dispatch_requests()
    window.after(5000, periodic_update)  # Schedule the function to run every 5 seconds

# Function to handle login and show main UI
def handle_login():
    global current_ambulance_id
    ambulance_id = ambulance_id_entry.get().strip()
    if ambulance_id:
        current_ambulance_id = ambulance_id  # Save the ambulance ID globally
        print(f"Ambulance ID: {ambulance_id}")  # Debug output
        login_frame.pack_forget()  # Hide login frame
        notebook.pack(expand=True, fill=tk.BOTH)  # Show main UI
        window.after(0, periodic_update)  # Start periodic updates
    else:
        error_label.config(text="Ambulance ID cannot be empty")

# Tkinter app setup
window = tk.Tk()
window.title("Ambulance UI")
window.geometry("800x600")

# Login Frame
login_frame = tk.Frame(window)
login_frame.pack(expand=True, fill=tk.BOTH)

tk.Label(login_frame, text="Enter Ambulance ID", font=("Arial", 14)).pack(pady=20)

ambulance_id_entry = tk.Entry(login_frame, font=("Arial", 12))
ambulance_id_entry.pack(pady=10)

login_button = tk.Button(login_frame, text="Login", font=("Arial", 12), command=handle_login)
login_button.pack(pady=10)

error_label = tk.Label(login_frame, text="", font=("Arial", 10), fg="red")
error_label.pack()

# Main UI
notebook = ttk.Notebook(window)

# Dispatch Requests page
dispatch_frame = ttk.Frame(notebook)
notebook.add(dispatch_frame, text="Dispatch Requests")

# Create Treeview table
dispatch_table = ttk.Treeview(dispatch_frame, columns=("Priority", "Incident Type", "Location", "Destination"), show="headings")
dispatch_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Configure headings
dispatch_table.heading("Priority", text="Priority")
dispatch_table.heading("Incident Type", text="Incident Type")
dispatch_table.heading("Location", text="Location")
dispatch_table.heading("Destination", text="Destination")

# Medical Records page
records_frame = ttk.Frame(notebook)
notebook.add(records_frame, text="Medical Records")

# Start with login frame visible
notebook.pack_forget()  # Hide the main UI initially

# Run the Tkinter event loop
window.mainloop()
