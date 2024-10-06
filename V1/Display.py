import tkinter as tk
from tkinter import LabelFrame

# Create the main window
root = tk.Tk()
root.title("LabelFrame Arrangement")

# Create LabelFrames for each body part
head = LabelFrame(root, text="Head", width=50, height=50, labelanchor="n")
torso = LabelFrame(root, text="Torso", width=50, height=100, labelanchor="n")
hand_r = LabelFrame(root, text="Right Hand", width=50, height=50, labelanchor="n")
hand_l = LabelFrame(root, text="Left Hand", width=50, height=50, labelanchor="n")

# Position the LabelFrames using grid
head.grid(row=0, column=1, padx=10, pady=10)
torso.grid(row=1, column=1, padx=10, pady=10)
hand_r.grid(row=1, column=0, padx=10, pady=10)
hand_l.grid(row=1, column=2, padx=10, pady=10)

# Run the application
root.mainloop()
