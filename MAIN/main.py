# MAIN/main.py
import tkinter as tk
import json
import os
import sys
from HOME.gui.main_window import MainWindow
from data.data_manager import DataManager
from FIGHT_SEQ.gui.main_window import FightWindow

def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_init_path():
    return os.path.join(get_base_dir(), '__init__.json')

def initialize_state():
    """Create or reset the state file"""
    state = {'active_knight': None}
    with open(get_init_path(), 'w') as f:
        json.dump(state, f, indent=2)
    return state

def main():
    # Set up base paths
    base_dir = get_base_dir()
    
    # Add main directory to Python path
    sys.path.insert(0, os.path.dirname(base_dir))
    
    # Set up root window
    root = tk.Tk()
    root.title("Knight Game")
    root.geometry("800x600")
    
    # Configure the grid
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    # Initialize fresh state
    initialize_state()
    
    # Always start with home screen
    print("Loading Home...")
    data_manager = DataManager()
    MainWindow(root, data_manager)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()