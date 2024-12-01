import tkinter as tk
from tkinter import ttk

def show_stance_menu(parent):
    """
    Show a popup menu for selecting stances.
    """
    stance_window = tk.Toplevel(parent)
    stance_window.title("Select Stance")
    stance_window.geometry("300x200")

    ttk.Label(stance_window, text="Choose your stance:", font=("Arial", 12)).pack(pady=10)

    ttk.Button(stance_window, text="Offensive Stance", command=lambda: print("Offensive Stance selected")).pack(pady=5)
    ttk.Button(stance_window, text="Defensive Stance", command=lambda: print("Defensive Stance selected")).pack(pady=5)
    ttk.Button(stance_window, text="Neutral Stance", command=lambda: print("Neutral Stance selected")).pack(pady=5)

    ttk.Button(stance_window, text="Close", command=stance_window.destroy).pack(pady=10)
