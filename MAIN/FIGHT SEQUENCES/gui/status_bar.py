import tkinter as tk
from tkinter import ttk

class RoundStatus(ttk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Actions", **kwargs)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="ROUND").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(self, text="SET IN").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self, text="ATTACK").grid(row=0, column=2, padx=10, pady=5)
        ttk.Label(self, text="CONTACT").grid(row=0, column=3, padx=10, pady=5)

        # Add a Roll Button
        roll_button = ttk.Button(self, text="ROLL")
        roll_button.grid(row=1, column=0, columnspan=4, pady=20)
