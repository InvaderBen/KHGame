# gui/main_window.py
import tkinter as tk
from tkinter import ttk
from gui.knight_list import KnightList
from gui.ability_editor import AbilityEditor
from gui.skill_editor import SkillEditor
from gui.all_statistics import AllStatistics
from gui.weapons_manager import WeaponsManager

class MainWindow:
    def __init__(self, master, data_manager):
        self.master = master
        self.data_manager = data_manager
        
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        
        self.create_left_panel()
        self.create_notebook()
        
        self.create_status_bar()
        
        self.current_knight = None

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        self.ability_editor = AbilityEditor(self.notebook, self.data_manager)
        self.all_statistics = AllStatistics(self.notebook, self.data_manager)
        self.skill_editor = SkillEditor(self.notebook, self.data_manager)
        self.weapons_manager = WeaponsManager(self.notebook, self.data_manager)

        self.notebook.add(self.ability_editor, text='Edit Abilities')
        self.notebook.add(self.all_statistics, text='All Statistics')
        self.notebook.add(self.skill_editor, text='Skills')
        self.notebook.add(self.weapons_manager, text='Weapons')

        self.ability_editor.bind("<<StatsUpdated>>", lambda e: self.all_statistics.update_display())

    def create_left_panel(self):
        self.left_panel = ttk.Frame(self.main_frame)
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
        self.status_bar = ttk.Frame(self.master)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.current_knight_label = ttk.Label(self.status_bar, text="<No Knight Selected>")
        self.current_knight_label.pack(side=tk.LEFT, padx=10)

        self.proceed_button = ttk.Button(self.status_bar, text="Proceed to Action", command=self.proceed_to_action, state=tk.DISABLED)
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
        self.ability_editor.load_knight(self.current_knight)
        self.all_statistics.load_knight(self.current_knight)
        self.skill_editor.load_knight(self.current_knight)
        self.weapons_manager.load_knight(self.current_knight)
        self.update_status_bar()

    def proceed_to_action(self):
        print('You are now on the Action Screen')