import tkinter as tk
from tkinter import ttk

class WeaponsManager(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_knight = None
        self.treeview_types = {}
        self.create_widgets()



    def create_widgets(self):
        self.create_equipment_notebook()
        self.create_detail_frame()

    def create_equipment_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        for category in ['Weapons', 'Shields', 'Armors']:
            tab = ttk.Frame(self.notebook)

            inventory_frame = ttk.LabelFrame(tab, text='Inventory')
            inventory_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            storage_frame = ttk.LabelFrame(tab, text='Storage')
            storage_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.create_treeview(inventory_frame, 'Inventory', category)
            self.create_treeview(storage_frame, 'Storage', category)

            #self.equip_button(inventory_frame)

            self.notebook.add(tab, text=category)

        self.create_action_buttons()

    def create_treeview(self, parent, type, category):
        columns = ("Name",)
        treeview = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=200, anchor="w")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)

        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        treeview.bind("<<TreeviewSelect>>", self.on_item_select)
        self.treeview_types[f'{category}_{type}'] = treeview

    def create_action_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=10)

        self.move_to_inventory_button = ttk.Button(button_frame, text='Move to Inventory', command=self.move_to_inventory)
        self.move_to_inventory_button.pack(side=tk.LEFT, padx=5)

        self.remove_from_inventory_button = ttk.Button(button_frame, text='Remove from Inventory', command=self.remove_from_inventory)
        self.remove_from_inventory_button.pack(side=tk.LEFT, padx=5)

    def create_detail_frame(self):
        self.detail_frame = ttk.LabelFrame(self, text="Item Details")
        self.detail_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    def load_knight(self, knight):
        self.current_knight = knight
        self.refresh_equipment_display()

    def refresh_equipment_display(self):
        for category in ['Weapons', 'Shields', 'Armors']:
            if self.current_knight:
                self.populate_treeview(f'{category}_Inventory', self.current_knight.get_equipment(category.lower()))
            self.load_storage_items(category)

    def load_storage_items(self, category):
        storage_items = self.data_manager.get_storage_items(category)
        self.populate_treeview(f'{category}_Storage', storage_items)



    def populate_treeview(self, treeview_name, items):
        treeview = self.treeview_types[treeview_name]
        treeview.delete(*treeview.get_children())
        for item in items:
            treeview.insert('', 'end', values=(item['name'],))



    def on_item_select(self, event):
        tree = event.widget
        selected_item = tree.focus()
        item_data = tree.item(selected_item)

        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        if item_data['values']:
            name = item_data['values'][0]  # Only get the name
            category = self.get_category_from_treeview(tree)
            item_stats = self.get_item_stats(category, name)
            
            if item_stats:
                ttk.Label(self.detail_frame, text=f"Name: {item_stats['name']}", font=("", 12, "bold")).pack(anchor="w")
                ttk.Label(self.detail_frame, text=f"Type: {item_stats['type']}").pack(anchor="w")
                
                for stat, value in item_stats.items():
                    if stat not in ['name', 'type']:
                        if isinstance(value, list):
                            # Handle array values (like 'perk')
                            ttk.Label(self.detail_frame, text=f"{stat.capitalize()}:").pack(anchor="w")
                            for item in value:
                                ttk.Label(self.detail_frame, text=f"  • {item}").pack(anchor="w", padx=(20, 0))
                        else:
                            ttk.Label(self.detail_frame, text=f"{stat.capitalize()}: {value}").pack(anchor="w")
            else:
                ttk.Label(self.detail_frame, text="Item details not found").pack(anchor="w")



    def get_category_from_treeview(self, treeview):
        for category in ['Weapons', 'Shields', 'Armors']:
            if treeview in [self.treeview_types[f'{category}_Inventory'], self.treeview_types[f'{category}_Storage']]:
                return category
        return None

    def get_item_stats(self, category, item_name):
        items = self.current_knight.get_equipment(category.lower()) + self.data_manager.get_storage_items(category)
        for item in items:
            if item['name'] == item_name:
                return item
        return {}



    def move_to_inventory(self):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        storage_tree = self.treeview_types[f'{selected_tab}_Storage']
        selected_item = storage_tree.focus()
        print(selected_item)
        
        if selected_item:
            item_data = storage_tree.item(selected_item)
            item_name = item_data['values'][0]
            item = self.get_item_stats(selected_tab, item_name)
        
            self.current_knight.add_equipment(item, selected_tab.lower())
            self.data_manager.save_knight_to_file(self.data_manager.get_knight_id(self.current_knight), self.current_knight)
            print(selected_item)

            self.refresh_equipment_display()

    def remove_from_inventory(self):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        inventory_tree = self.treeview_types[f'{selected_tab}_Inventory']
        selected_item = inventory_tree.focus()
        if selected_item:
            item_data = inventory_tree.item(selected_item)
            item_name = item_data['values'][0]
            item = self.get_item_stats(selected_tab, item_name)
            
            self.current_knight.remove_equipment(item, selected_tab.lower())
            self.data_manager.save_knight_to_file(self.data_manager.get_knight_id(self.current_knight), self.current_knight)
            self.refresh_equipment_display()