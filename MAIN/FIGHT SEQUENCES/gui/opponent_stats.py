import tkinter as tk
from tkinter import ttk

class OpponentStats(ttk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Combat Values", **kwargs)
        self.master = master
        self.values = {
            "COM. DAMAGE": 38, "HP": 7, "COMBAT STRIK": 46, "Combat BLOCK": 31,
            "COM. EVADE": 18, "MOOD": 8, "COMBAT DEFEI": 97, "COMBAT ACC": 25,
            "PROT": 32, "SPEED": 12, "HARDNESS": 7, "BALANCE": 14
        }
        self.create_widgets()

    def create_widgets(self):
        for i, (key, value) in enumerate(self.values.items()):
            ttk.Label(self, text=f"{key}:").grid(row=i, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(self, text=value).grid(row=i, column=1, sticky="e", padx=5, pady=2)
