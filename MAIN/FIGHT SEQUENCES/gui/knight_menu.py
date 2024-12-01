import tkinter as tk
from tkinter import ttk

def show_knight_menu(parent):
    """
    Show a popup menu for knight information.
    """
    knight_window = tk.Toplevel(parent)
    knight_window.title("Knight Menu")
    knight_window.geometry("300x200")

    ttk.Label(knight_window, text="Knight Status", font=("Arial", 12)).pack(pady=10)

    ttk.Label(knight_window, text="Level: 5").pack(pady=5)
    ttk.Label(knight_window, text="Health: 80/100").pack(pady=5)
    ttk.Label(knight_window, text="Armor: 25").pack(pady=5)

    ttk.Button(knight_window, text="Close", command=knight_window.destroy).pack(pady=10)
