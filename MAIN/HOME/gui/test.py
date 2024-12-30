import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Three Panel Layout")

# Configure grid weights to make the center panel expand more
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create the three LabelFrames
left_frame = ttk.LabelFrame(root, text="Left Panel")
center_frame = ttk.LabelFrame(root, text="Center Panel")
right_frame = ttk.LabelFrame(root, text="Right Panel")

# Place the frames using grid
left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
center_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
right_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

# Add some minimum width to each frame (optional)
left_frame.grid_propagate(False)
left_frame.configure(width=200, height=400)
right_frame.grid_propagate(False)
right_frame.configure(width=200, height=400)

root.mainloop()