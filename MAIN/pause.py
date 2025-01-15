# MAIN/pause.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

def handle_pause(master, init_path):
    result = messagebox.askyesno("Pause", "Return to home screen?")
    if result:
        # Reset state
        state = {'active_knight': None}
        with open(init_path, 'w') as f:
            json.dump(state, f, indent=2)
        
        # Clear fight window and reload home
        for widget in master.winfo_children():
            widget.destroy()
        
        # Import and create home window
        from HOME.gui.main_window import MainWindow
        from HOME.data.data_manager import DataManager
        
        data_manager = DataManager()
        MainWindow(master, data_manager)