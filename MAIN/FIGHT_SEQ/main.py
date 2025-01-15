# FIGHT_SEQ/main.py
import json
import tkinter as tk
from tkinter import ttk, messagebox
import multiprocessing
from multiprocessing import freeze_support
import sys
import os

def create_window():
    window = tk.Tk()
    window.title("Fight Sequence")
    window.geometry("400x300")
    
    # Prevent window from being minimized or closed
    window.protocol("WM_DELETE_WINDOW", lambda: None)
    window.resizable(False, False)
    
    # Keep window always on top
    window.attributes('-topmost', True)
    
    # Load active knight
    try:
        with open('I:/KH_Py/KHGame/MAIN/__init__.json', 'r') as f:
            state = json.load(f)
            active_knight = state.get('active_knight')
    except Exception as e:
        messagebox.showerror("Error", f"Error loading knight: {e}")
        sys.exit()
        
    # Configure the window
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    
    # Create main frame
    main_frame = ttk.Frame(window, padding="20")
    main_frame.grid(row=0, column=0, sticky="nsew")
    
    # Knight info
    knight_label = ttk.Label(main_frame, text=f"Active Knight ID: {active_knight}", font=('Arial', 12))
    knight_label.pack(pady=20)
    
    # Question label
    question_label = ttk.Label(main_frame, text="Would you like to proceed with the fight?", font=('Arial', 10))
    question_label.pack(pady=20)
    
    # Buttons frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)
    
    def on_yes():
        print("User clicked Yes - proceed with game")
        # Add your game logic here
    
    def on_no():
        window.quit()
        window.destroy()
        sys.exit()
    
    # Yes/No buttons
    yes_btn = ttk.Button(button_frame, text="Yes", command=on_yes)
    yes_btn.pack(side=tk.LEFT, padx=10)
    
    no_btn = ttk.Button(button_frame, text="No", command=on_no)
    no_btn.pack(side=tk.LEFT, padx=10)
    
    # Start update loop
    def update():
        window.after(100, update)
    update()
    
    window.mainloop()

def run_window():
    # Detach from parent process
    if hasattr(os, 'setsid'):
        os.setsid()
    create_window()

if __name__ == "__main__":
    freeze_support()
    # Start in a new process
    process = multiprocessing.Process(target=run_window)
    process.daemon = False  # Make sure it's not a daemon process
    process.start()

# Update for main_window.py - proceed_to_action method
def proceed_to_action(self):
    if self.current_knight:
        knight_id = self.data_manager.get_knight_id(self.current_knight)
        state = {'active_knight': knight_id}
        with open('I:/KH_Py/KHGame/MAIN/__init__.json', 'w') as f:
            json.dump(state, f, indent=2)
        
        # Launch the FIGHT_SEQ main.py
        import subprocess
        import os
        
        # Use shell=True and start a new process group
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        subprocess.Popen(['pythonw', 'I:/KH_Py/KHGame/MAIN/FIGHT_SEQ/main.py'], 
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                        startupinfo=startupinfo,
                        shell=True)
        
        # Close the current window
        self.master.destroy()