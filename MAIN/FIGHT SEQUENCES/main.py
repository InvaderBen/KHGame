import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from gui.main_window import MainWindow
from data.data_manager import DataManager
from utils.config import ensure_directory_exists
from utils.config import KNIGHT_DIRECTORY, STORAGE_DIRECTORY

class ActionScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Knights Information")
        
        # Ensure necessary directories exist
        ensure_directory_exists(KNIGHT_DIRECTORY)
        ensure_directory_exists(STORAGE_DIRECTORY)

        self.data_manager = DataManager()
        self.main_window = MainWindow(self.master, self.data_manager)

if __name__ == "__main__":
    root = ThemedTk(theme="winxpblue")
    app = ActionScreen(root)
    root.mainloop()

