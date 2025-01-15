import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from gui.main_window import MainWindow
from MAIN.data.data_manager import DataManager
from MAIN.utils.config import ensure_directory_exists
from MAIN.utils.config import KNIGHT_DIRECTORY, STORAGE_DIRECTORY

class HomeScreen:
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
    app = HomeScreen(root)
    root.mainloop()

