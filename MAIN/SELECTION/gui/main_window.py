# gui/main_window.py
import sys
sys.path.append(r"I:\KH_Py\KHGame")
import os
import json
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from MAIN.SELECTION.gui.knight_list import KnightList
from MAIN.SELECTION.gui.all_statistics import AllStatistics
from MAIN.SELECTION.gui.weapons_manager import WeaponsManager

class MainWindow:
    def __init__(self, master, data_manager):
        self.master = master
        self.data_manager = data_manager
        
    
        # Create main container for LEFT|CENTER|RIGHT panels
        self.top_frame = ttk.Frame(self.master)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Create panels in order
        self.create_left_panel()
        self.create_center_panel()  # New method for notebook
        self.create_right_panel()
        self.create_status_bar()    # RIGHT
        

        self.current_knight = None

    def create_center_panel(self):
        # Center panel with notebook
        self.notebook = ttk.Notebook(self.top_frame)
        self.notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.all_statistics = AllStatistics(self.notebook, self.data_manager)
        self.weapons_manager = WeaponsManager(self.notebook, self.data_manager)

        self.notebook.add(self.all_statistics, text='All Statistics')
        self.notebook.add(self.weapons_manager, text='Weapons')


    def create_right_panel(self):
        self.right_panel = ttk.LabelFrame(self.top_frame, text="Knight")
        self.right_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Create label for artwork image
        self.artwork_label = ttk.Label(self.right_panel)
        self.artwork_label.pack(side=tk.TOP, padx=10, pady=5)
        
        # Create label for artwork filename
        self.artwork_path_label = ttk.Label(self.right_panel, text="No artwork selected")
        self.artwork_path_label.pack(side=tk.TOP, padx=10, pady=5)
        
        # Store the current PhotoImage reference
        self.current_artwork = None

    def create_left_panel(self):
        self.left_panel = ttk.Frame(self.top_frame)  # Note: parent is top_frame
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        self.create_knight_list()
        self.create_knight_buttons()


    def create_knight_list(self):
        self.knight_list = KnightList(self.left_panel, self.data_manager)
        self.knight_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.knight_list.bind('<<KnightSelected>>', self.on_knight_select)

    def create_knight_buttons(self):
        button_frame = ttk.Frame(self.left_panel)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.new_knight_button = ttk.Button(button_frame, text="New Knight", command=self.new_knight)
        self.new_knight_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.delete_knight_button = ttk.Button(button_frame, text="Delete Knight", command=self.delete_knight)
        self.delete_knight_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)


    def new_knight(self):
        new_knight = self.data_manager.create_new_knight()
        self.knight_list.add_knight(new_knight)
        self.on_knight_select(None)

    def delete_knight(self):
        if self.current_knight:
            knight_id = self.data_manager.get_knight_id(self.current_knight)
            if knight_id is not None and self.data_manager.delete_knight(knight_id):
                self.knight_list.remove_current_knight()
                self.current_knight = None
                self.update_general_frame()


    def create_status_bar(self):
        # Status bar will be the BOTTOM panel
        self.status_bar = ttk.Frame(self.master)  # Note: parent is master
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.current_knight_label = ttk.Label(self.status_bar, text="<No Knight Selected>")
        self.current_knight_label.pack(side=tk.LEFT, padx=10)

        self.proceed_button = ttk.Button(self.status_bar, text="Proceed to Action", 
                                    command=self.proceed_to_action, state=tk.DISABLED)
        self.proceed_button.pack(side=tk.RIGHT, padx=10)

    def update_status_bar(self):
        if self.current_knight:
            self.current_knight_label.config(text=self.current_knight.name)
            self.proceed_button.config(state=tk.NORMAL)
        else:
            self.current_knight_label.config(text="<No Knight Selected>")
            self.proceed_button.config(state=tk.DISABLED)


    def on_knight_select(self, event):
        knight_id = self.knight_list.get_selected_knight_id()
        self.current_knight = self.data_manager.get_knight(knight_id)
        
        # Update artwork display
        if self.current_knight and hasattr(self.current_knight, 'artwork'):
            self.load_artwork(self.current_knight.artwork)
        else:
            self.artwork_label.config(image='')
            self.artwork_path_label.config(text="No artwork selected")
        
        self.ability_editor.load_knight(self.current_knight)
        self.all_statistics.load_knight(self.current_knight)
        self.skill_editor.load_knight(self.current_knight)
        self.weapons_manager.load_knight(self.current_knight)
        self.update_status_bar()

    def load_artwork(self, artwork_path):
        try:
            full_path = os.path.normpath(f"I:/{artwork_path}")
            
            # Load and process image with PIL
            pil_image = Image.open(full_path)
            pil_image = pil_image.rotate(-90, expand=True)  # Rotate 90° clockwise
            width = pil_image.width // 2
            height = pil_image.height // 2
            pil_image = pil_image.resize((width, height))
            
            # Convert to PhotoImage
            self.current_artwork = ImageTk.PhotoImage(pil_image)
            self.artwork_label.config(image=self.current_artwork)
            self.artwork_path_label.config(text=os.path.basename(artwork_path))
            
        except Exception as e:
            print(f"Error loading artwork: {e}")
            self.artwork_label.config(image='')
            self.artwork_path_label.config(text="Error loading artwork")

    def proceed_to_action(self):
        if self.current_knight:
            knight_id = self.data_manager.get_knight_id(self.current_knight)
            state = {'active_knight': knight_id}
            
            # Get base directory and init.json path
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            init_path = os.path.join(base_dir, '__init__.json')
            
            # Save state
            with open(init_path, 'w') as f:
                json.dump(state, f, indent=2)
                
            # Clear all widgets from current window
            for widget in self.master.winfo_children():
                widget.destroy()
                
            # Import and create fight window
            from FIGHT_SEQ.gui.main_window import FightWindow
            FightWindow(self.master)