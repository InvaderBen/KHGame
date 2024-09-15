import json
import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from Knight import Knight

class TestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Test App")
        
        self.storage_data = {
            'Weapons': [],
            'Shields': [],
            'Armors': [],
        }

        self.inventory_data = {
            'Weapons': [],
            'Shields': [],
            'Armors': [],
        }

        # Initialize dictionary for treeview widgets
        self.treeview_types = {
            'Weapons_Inventory': None,
            'Shields_Inventory': None,
            'Armors_Inventory': None,
            'Weapons_Storage': None,
            'Shields_Storage': None,
            'Armors_Storage': None,
        }

        self.create_main_frame(master)
        self.create_equipment_notebook(self.main_frame)
        self.create_detail_frame(self.main_frame)

    def create_main_frame(self, parent):
        self.main_frame = ttk.Frame(parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_equipment_notebook(self, parent):
        self.notebook_frame = ttk.Frame(parent)
        self.notebook_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        for category in ['Weapons', 'Shields', 'Armors']:
            tab = ttk.Frame(self.notebook)

            Inventory = ttk.LabelFrame(tab, text='Inventory')
            Inventory.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            Storage = ttk.LabelFrame(tab, text='Storage')
            Storage.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create treeviews for Inventory and Storage
            self.create_treeview(Inventory, 'Inventory', category)
            self.create_treeview(Storage, 'Storage', category)

            self.load_equipment_data(category)

            self.notebook.add(tab, text=category)

        # Populate treeviews after all data is loaded
        self.populate_treeviews()

    def create_detail_frame(self, parent):
        self.detail_frame = ttk.LabelFrame(parent, text="Item Details")
        self.detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_treeview(self, parent, type, category):
        treeframe = ttk.Frame(parent)
        treeframe.pack(fill=tk.BOTH, expand=True)

        columns = ("Name", "Type")
        treeview = ttk.Treeview(treeframe, columns=columns, show="headings")
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor="center")

        # Create scrollbars
        vsb = ttk.Scrollbar(treeframe, orient="vertical", command=treeview.yview)
        hsb = ttk.Scrollbar(treeframe, orient="horizontal", command=treeview.xview)
        treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        treeview.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        treeframe.grid_columnconfigure(0, weight=1)
        treeframe.grid_rowconfigure(0, weight=1)

        # Bind the select event
        treeview.bind("<<TreeviewSelect>>", self.on_item_select)

        # Store treeview reference in dictionary
        self.treeview_types[f'{category}_{type}'] = treeview

    def on_item_select(self, event):
        tree = event.widget
        selected_item = tree.focus()
        item_data = tree.item(selected_item)
        
        # Clear previous details
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        if item_data['values']:  # Check if it's not a category
            name, eq_type = item_data['values']
            ttk.Label(self.detail_frame, text=f"Name: {name}", font=("", 12, "bold")).pack(anchor="w")
            ttk.Label(self.detail_frame, text=f"Type: {eq_type}").pack(anchor="w")
            
            # Fetch actual stats from our data structure
            category = self.get_category_from_treeview(tree)
            item_stats = self.get_item_stats(category, name)
            
            for stat, value in item_stats.items():
                if stat not in ['name', 'weapon_type']:  # Skip name and weapon_type as they're already displayed
                    ttk.Label(self.detail_frame, text=f"{stat.capitalize()}: {value}").pack(anchor="w")
        
        print('Selected')

    def get_category_from_treeview(self, treeview):
        for category in ['Weapons', 'Shields', 'Armors']:
            if treeview in [self.treeview_types[f'{category}_Inventory'], self.treeview_types[f'{category}_Storage']]:
                return category
        return None

    def get_item_stats(self, category, item_name):
        for item in self.storage_data[category] + self.inventory_data[category]:
            if item['name'] == item_name:  # Changed 'Name' to 'name'
                return item
        return {}

    def load_equipment_data(self, category):
        folder_path = os.path.join('equipment', category.lower())
        
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return

        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                item_data = self.load_item_data(os.path.join(folder_path, filename))
                self.storage_data[category].append(item_data)

    def load_item_data(self, file_path):
        with open(file_path, 'r') as f:
            item_data = json.load(f)
        return item_data

    def populate_treeviews(self):
        for category in ['Weapons', 'Shields', 'Armors']:
            storage_treeview = self.treeview_types[f'{category}_Storage']
            inventory_treeview = self.treeview_types[f'{category}_Inventory']

            # Populate Storage treeview
            for item in self.storage_data[category]:
                storage_treeview.insert('', 'end', values=(item['name'], item['weapon_type'] if 'weapon_type' in item else category[:-1]))

            # Populate Inventory treeview (currently empty)
            for item in self.inventory_data[category]:
                inventory_treeview.insert('', 'end', values=(item['name'], item['weapon_type'] if 'weapon_type' in item else category[:-1]))

if __name__ == "__main__":
    root = ThemedTk(theme="winxpblue")
    app = TestApp(root)
    root.mainloop()