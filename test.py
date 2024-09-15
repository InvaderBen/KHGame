import tkinter as tk
from tkinter import ttk

class ScalableEquipmentTreeview:
    def __init__(self, root):
        self.root = root
        self.root.title("Scalable Equipment Treeview")
        
        # Main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create Treeview with minimal columns
        self.tree = ttk.Treeview(main_frame, columns=("name", "type"), show="tree headings")
        self.tree.heading("#0", text="Category")
        self.tree.heading("name", text="Name")
        self.tree.heading("type", text="Type")

        self.tree.column("#0", width=150, anchor="w")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("type", width=100, anchor="w")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Frame for details
        self.detail_frame = ttk.LabelFrame(root, text="Equipment Details")
        self.detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate the tree
        self.populate_tree()

        # Bind select event
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

    def populate_tree(self):
        # Sample data structure
        equipment_data = {
            "Weapons": [
                ("Sword", "Melee", {"attack": 10, "speed": 5, "durability": 100, "weight": 3}),
                ("Bow", "Ranged", {"attack": 8, "range": 50, "accuracy": 90, "weight": 2})
            ],
            "Armor": [
                ("Plate Mail", "Heavy", {"defense": 20, "speed": -5, "durability": 150, "weight": 15}),
                ("Leather Armor", "Light", {"defense": 10, "speed": 2, "elemental_resist": 5, "weight": 5})
            ],
            "Accessories": [
                ("Ring of Power", "Jewelry", {"magic_boost": 15, "mana_regen": 5, "weight": 0.1}),
                ("Boots of Swiftness", "Footwear", {"speed": 10, "stamina": 20, "weight": 1})
            ]
        }

        for category, items in equipment_data.items():
            category_id = self.tree.insert("", "end", text=category, open=True)
            for name, eq_type, stats in items:
                self.tree.insert(category_id, "end", values=(name, eq_type))

    def on_item_select(self, event):
        selected_item = self.tree.focus()
        item_data = self.tree.item(selected_item)
        
        # Clear previous details
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        if item_data['values']:  # Check if it's not a category
            name, eq_type = item_data['values']
            ttk.Label(self.detail_frame, text=f"Name: {name}", font=("", 12, "bold")).pack(anchor="w")
            ttk.Label(self.detail_frame, text=f"Type: {eq_type}").pack(anchor="w")
            
            # In a real application, you would fetch these stats from your data structure
            # Here, we're just displaying sample stats
            sample_stats = {
                "Sword": {"attack": 10, "speed": 5, "durability": 100, "weight": 3},
                "Plate Mail": {"defense": 20, "speed": -5, "durability": 150, "weight": 15},
                "Ring of Power": {"magic_boost": 15, "mana_regen": 5, "weight": 0.1}
            }
            
            stats = sample_stats.get(name, {})
            for stat, value in stats.items():
                ttk.Label(self.detail_frame, text=f"{stat.capitalize()}: {value}").pack(anchor="w")
        
        print('Selected')

if __name__ == "__main__":
    root = tk.Tk()
    app = ScalableEquipmentTreeview(root)
    root.mainloop()