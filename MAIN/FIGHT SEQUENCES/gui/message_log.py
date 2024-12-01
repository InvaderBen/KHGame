import tkinter as tk
from tkinter import ttk

class MessageLog(ttk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Message Log", **kwargs)
        self.master = master

        # Create the Text widget for displaying messages
        self.log_text = tk.Text(
            self, wrap="word", height=8, state="disabled",
            bg="white", fg="black", font=("Arial", 10), relief="flat"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add a Scrollbar
        self.scrollbar = ttk.Scrollbar(self, command=self.log_text.yview)
        self.log_text["yscrollcommand"] = self.scrollbar.set
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def add_message(self, message: str):
        """
        Add a new message to the log.
        This is called externally to update the log.
        """
        self.log_text.config(state="normal")  # Enable editing temporarily
        self.log_text.insert(tk.END, message + "\n")  # Append message
        self.log_text.see(tk.END)  # Scroll to the bottom
        self.log_text.config(state="disabled")  # Disable editing
