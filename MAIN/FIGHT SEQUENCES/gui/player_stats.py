import tkinter as tk
from tkinter import ttk

class PlayerStats(ttk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Combat Values", **kwargs)
        self.master = master
        self.values = {
            "COM. DAMAGE": 43, "HP": 13, "COMBAT STRIK": 38, "Combat BLOCK": 90,
            "COM. EVADE": 14, "MOOD": 14, "COMBAT DEFEI": 99, "COMBAT ACC": 15,
            "PROT": 39, "SPEED": 9, "HARDNESS": 13, "BALANCE": 10
        }
        self.create_widgets()

    def create_widgets(self):
        for i, (key, value) in enumerate(self.values.items()):
            ttk.Label(self, text=f"{key}:").grid(row=i, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(self, text=value).grid(row=i, column=1, sticky="e", padx=5, pady=2)
