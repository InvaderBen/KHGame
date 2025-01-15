import tkinter as tk
from tkinter import ttk

class BattleGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battle Grid")

        # Define the grid layout based on the diagram
        self.create_grid()
        self.add_knight_controls()

    def create_grid(self):
        zones = ["SAFE", "2ND", "KNIGHT_NO1", "KNIGHT_NO2", "2ND", "SAFE"]

        for row in range(4):
            for col in range(6):
                cell = tk.Frame(
                    self.root, 
                    width=100, 
                    height=100, 
                    bg="gray" if row == 3 or col in [0, 5] else "white",
                    relief=tk.RIDGE, 
                    borderwidth=2
                )
                cell.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

                # Add labels for specific zones
                if row == 3:
                    tk.Label(cell, text=zones[col], bg="gray", fg="white").pack(expand=True)

                # Add stick figures in the middle row
                if row == 1 and col in [2, 3]:
                    stick_figure = tk.Label(cell, text="\u263A", font=("Arial", 24), bg="white")
                    stick_figure.pack(expand=True)

    def add_knight_controls(self):
        # Add controls below "KNIGHT_NO1"
        control_frame = tk.Frame(self.root, bg="lightgray", relief=tk.RIDGE, borderwidth=2)
        control_frame.grid(row=4, column=2, rowspan=1, columnspan=2, sticky="nsew")

        # Add control buttons
        tk.Button(control_frame, text="PASS", width=10).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="ACT", width=10).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="COUNTER", width=10).grid(row=2, column=0, padx=5, pady=5)

        # Add dropdown menu for stances
        stance_label = tk.Label(control_frame, text="STANCES:", bg="lightgray")
        stance_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        stances = ttk.Combobox(control_frame, values=["Attack", "Defend", "Neutral"])
        stances.set("Select Stance")
        stances.grid(row=1, column=1, padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleGridApp(root)
    root.mainloop()
