import tkinter as tk
from tkinter import ttk

class AllStatistics(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_knight = None
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Value'), show='tree headings')
        self.tree.heading('Value', text='Value')
        self.tree.column('Value', width=100, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_knight(self, knight):
        self.current_knight = knight
        self.update_display()

    def update_display(self):
        if not self.current_knight:
            return

        self.tree.delete(*self.tree.get_children())

        stats = self.current_knight.get_stats()
        
        for category, values in stats.items():
            category_id = self.tree.insert('', 'end', text=category.replace('_', ' ').title())
            for stat, value in values.items():
                self.tree.insert(category_id, 'end', text=stat, values=(value,))