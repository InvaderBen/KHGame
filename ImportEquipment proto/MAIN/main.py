import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path to allow imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# Import our modules
from MAIN.equipment_logic import EquipmentManager
from gui.main_window import MainWindow
from gui.constants import *

class Application:
    def __init__(self):
        # Create and configure root window
        self.root = tk.Tk()
        self.root.title("Equipment Manager")
        self.root.geometry("1200x800")  # Set default window size
        
        # Configure style
        self.setup_styles()
        
        # Initialize equipment manager
        self.equipment_manager = EquipmentManager()
        
        # Create main window
        self.main_window = MainWindow(self.root, self.equipment_manager)
        
        # Store reference to main window in root
        self.root.main_app = self.main_window
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.configure('TFrame', background=BACKGROUND_COLOR)
        style.configure('TLabel', background=BACKGROUND_COLOR, font=NORMAL_FONT)
        style.configure('TButton', font=NORMAL_FONT)
        style.configure('Header.TLabel', font=HEADER_FONT)
        style.configure('Cmd.TLabel', font=MONO_FONT)
        
        # Configure Notebook styles
        style.configure('TNotebook', background=BACKGROUND_COLOR)
        style.configure('TNotebook.Tab', padding=[10, 5])
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    try:
        # Create and start application
        app = Application()
        app.run()
    except Exception as e:
        # Basic error handling
        import traceback
        print("Error starting application:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()