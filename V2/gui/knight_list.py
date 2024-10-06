# gui/knight_list.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class KnightList(ttk.Frame):
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
        
        self.create_widgets()
        self.load_knights()

    def create_widgets(self):
        self.listbox = tk.Listbox(self, width=30)
        self.listbox.pack(fill=tk.BOTH, expand=1)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.bind('<Double-1>', self.on_double_click)

    def load_knights(self):
        self.listbox.delete(0, tk.END)
        for knight_id, knight in self.data_manager.knights.items():
            self.listbox.insert(tk.END, f"{knight_id}: {knight.name}")

    def on_select(self, event):
        if self.listbox.curselection():
            self.event_generate('<<KnightSelected>>')

    def on_double_click(self, event):
        self.edit_knight_name()

    def add_knight(self, knight):
        knight_id = self.data_manager.get_knight_id(knight)
        self.listbox.insert(tk.END, f"{knight_id}: {knight.name}")
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(tk.END)
        self.event_generate('<<KnightSelected>>')

    def delete_knight(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            knight_id = self.get_selected_knight_id()
            if messagebox.askyesno("Delete Knight", "Are you sure you want to delete this knight?"):
                if self.data_manager.delete_knight(knight_id):
                    self.listbox.delete(index)
                    self.event_generate('<<KnightSelected>>')

    def remove_current_knight(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)

    def edit_knight_name(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            knight_id = self.get_selected_knight_id()
            current_name = self.listbox.get(index).split(': ', 1)[1]
            new_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=current_name)
            if new_name:
                self.data_manager.update_knight_name(knight_id, new_name)
                self.listbox.delete(index)
                self.listbox.insert(index, f"{knight_id}: {new_name}")

    def get_selected_knight_id(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            item_text = self.listbox.get(index)
            return int(item_text.split(':')[0])
        return None