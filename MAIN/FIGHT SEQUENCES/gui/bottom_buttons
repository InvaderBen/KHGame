import tkinter as tk
from tkinter import ttk

class BottomButtons(ttk.Frame):
    def __init__(self, master, stance_callback=None, knight_callback=None, roll_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        # STANCE Button
        self.stance_button = ttk.Button(self, text="STANCE", command=stance_callback)
        self.stance_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # KNIGHT Button
        self.knight_button = ttk.Button(self, text="KNIGHT", command=knight_callback)
        self.knight_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ROLL Button
        self.roll_button = ttk.Button(self, text="ROLL", command=roll_callback)
        self.roll_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
