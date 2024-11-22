import tkinter as tk
from tkinter import ttk
from flask import Flask, request, jsonify
import threading
import requests

# Sample data with priority as the first field
addresses = [
]

# Function to display the form for editing priority, name, address, and additional details
def show_form(priority, name, address, what, when, action_taken, time_spent, hospital):
    # Create a new window for the form
    form_window = tk.Toplevel(window)
    form_window.title(f"Edit Details for: {address}")

    # Priority label and entry
    priority_label = tk.Label(form_window, text="Priority:")
    priority_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    priority_entry = tk.Entry(form_window, width=30)
    priority_entry.grid(row=0, column=1, padx=5, pady=5)
    priority_entry.insert(0, priority)  # Populate the priority field

    # Name label and entry
    name_label = tk.Label(form_window, text="Name:")
    name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(form_window, width=30)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    name_entry.insert(0, name)  # Populate the name field

    # Address label and entry
    address_label = tk.Label(form_window, text="Address:")
    address_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    address_entry = tk.Entry(form_window, width=30)
    address_entry.grid(row=2, column=1, padx=5, pady=5)
    address_entry.insert(0, address)  # Populate the address field

    # Hospital label and entry
    hospital_label = tk.Label(form_window, text="Hospital:")
    hospital_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    hospital_entry = tk.Entry(form_window, width=30)
    hospital_entry.grid(row=3, column=1, padx=5, pady=5)
    hospital_entry.insert(0, hospital)  # Populate the hospital field

    # What label and entry
    what_label = tk.Label(form_window, text="What:")
    what_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
    what_entry = tk.Entry(form_window, width=30)
    what_entry.grid(row=4, column=1, padx=5, pady=5)
    what_entry.insert(0, what)  # Populate the "What" field

    # When label and entry
    when_label = tk.Label(form_window, text="When:")
    when_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
    when_entry = tk.Entry(form_window, width=30)
    when_entry.grid(row=5, column=1, padx=5, pady=5)
    when_entry.insert(0, when)  # Populate the "When" field

    # Action Taken label and entry
    action_label = tk.Label(form_window, text="Action Taken:")
    action_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
    action_entry = tk.Entry(form_window, width=30)
    action_entry.grid(row=6, column=1, padx=5, pady=5)
    action_entry.insert(0, action_taken)  # Populate the "Action Taken" field

    # Time Spent label and entry
    time_label = tk.Label(form_window, text="Time Spent (hours):")
    time_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
    time_entry = tk.Entry(form_window, width=30)
    time_entry.grid(row=7, column=1, padx=5, pady=5)
    time_entry.insert(0, time_spent)  # Populate the "Time Spent" field

    # Update button
    def update_data():
        updated_priority = priority_entry.get()
        updated_name = name_entry.get()
        updated_address = address_entry.get()
        updated_what = what_entry.get()
        updated_when = when_entry.get()
        updated_action_taken = action_entry.get()
        updated_time_spent = time_entry.get()
        updated_hospital = hospital_entry.get()

        updated_data = {
            "name": updated_name,
            "address": updated_address,
            "priority": updated_priority,
            "what": updated_what,
            "when": updated_when,
            "action_taken": updated_action_taken,
            "time_spent": updated_time_spent,
            "hospital": updated_hospital
        }

        # Send the updated data to the API (you can replace this with actual API calls)
        response = requests.post("http://localhost:4000/callout_update", json=updated_data)
        if response.status_code == 200:
            print("ambulance_ui: Sending update data, updated successfully.")
        else:
            print("Failed to send updated data.")

        # Close the form window
        form_window.destroy()

    update_button = tk.Button(form_window, text="Update", command=update_data)
    update_button.grid(row=8, column=0, columnspan=2, pady=10)

# Flask app to add a new name and address
app = Flask(__name__)

@app.route('/add_address', methods=['POST'])
def add_address():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    hospital = data.get('hospital', "Unknown Hospital")  # Optional, defaults to "Unknown"
    priority = data.get('priority', 3)  # Default priority is 3 if not provided

    print("ambulance_ui: Received new address.")
    addresses.append((priority, name, address, "What?", "When?", "Action Taken", "1 hour", hospital))
    update_treeview()

    return jsonify({"message": "Address added successfully"}), 201


# Function to start Flask API in a separate thread
def run_flask_app():
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000)

# Start Flask API in a separate thread
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.daemon = True
flask_thread.start()

# Function to update the treeview when addresses change
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    
    for priority, name, address, what, when, action_taken, time_spent, hospital in addresses:
        tree.insert("", "end", values=(priority, name, address, hospital))

# Create the main application window
window = tk.Tk()
window.title("Ambulance #0001")

# Create a treeview to display clickable priority, names, addresses, and hospitals
tree = ttk.Treeview(window, columns=("Priority", "Name", "Address", "Hospital"), show="headings", selectmode="browse")
tree.heading("#1", text="Priority")
tree.heading("#2", text="Name")
tree.heading("#3", text="Address")
tree.heading("#4", text="Hospital")

# Insert the priority, name, address, and hospital data into the treeview
update_treeview()

tree.pack(padx=10, pady=10)

# Add a binding to handle clicks
def on_item_click(event):
    selected_item = tree.selection()
    if selected_item:
        priority, name, address, hospital = tree.item(selected_item, "values")
        # Find the corresponding entry in the addresses list
        for addr in addresses:
            if addr[0] == int(priority) and addr[1] == name and addr[2] == address and addr[7] == hospital:
                show_form(*addr)
                break

tree.bind("<Double-1>", on_item_click)

# Run the Tkinter application
window.mainloop()

