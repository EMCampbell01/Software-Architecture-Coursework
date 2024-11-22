import tkinter as tk
from tkinter import ttk
from pages.emergency_call_intake_page import create_emergency_call_intake_page

# Tkinter app setup
window = tk.Tk()
window.title("HQ UI")
window.geometry("800x600")

# Main UI
notebook = ttk.Notebook(window)

# Add the Emergency Call Intake page
create_emergency_call_intake_page(notebook)

# Add notebook to window
notebook.pack(expand=True, fill="both")

# Run the app
window.mainloop()
