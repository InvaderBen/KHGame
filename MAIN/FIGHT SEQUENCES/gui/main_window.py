from tkinter import Tk
from bottom_buttons import BottomButtons
from stances_menu import show_stance_menu
from knight_menu import show_knight_menu
from message_log import MessageLog


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Combat UI")
        self.root.geometry("1000x600")

        # Bottom Buttons Panel
        self.bottom_buttons = BottomButtons(
            self.root,
            stance_callback=lambda: show_stance_menu(self.root),
            knight_callback=lambda: show_knight_menu(self.root),
            roll_callback=self.handle_roll
        )
        self.bottom_buttons.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Message Log (Bottom Center)
        self.message_log = MessageLog(self.root)
        self.message_log.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Grid configuration
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def handle_roll(self):
        """
        Handle the ROLL button click.
        """
        import random
        roll_result = random.randint(1, 20)
        self.message_log.add_message(f"You rolled a {roll_result}!")

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()