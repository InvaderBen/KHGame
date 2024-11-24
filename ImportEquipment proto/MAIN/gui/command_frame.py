import tkinter as tk
from tkinter import ttk
from COMMANDS.command_interpreter import CommandInterpreter

class CommandFrame(ttk.Frame):
    def __init__(self, parent, equipment_manager, main_window):
        super().__init__(parent)
        self.equipment_manager = equipment_manager
        self.main_window = main_window
        self.command_interpreter = CommandInterpreter(equipment_manager, main_window)
        self.command_history = []
        self.history_index = -1
        self.setup_command_area()
        self.pack(fill="both", expand=True)

    def setup_command_area(self):
        # Create text widget
        self.text = tk.Text(self, wrap=tk.WORD, font=('Consolas', 10))
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack widgets
        self.scrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        
        # Initialize with prompt
        self.text.insert("1.0", "Welcome to Equipment Manager Command Prompt\nType 'help' for available commands\n\n> ")
        
        # Bind events - using consistent method names
        self.text.bind("<Return>", self.on_return)
        self.text.bind("<KeyPress>", self.on_keypress)
        self.text.bind("<Up>", self.on_up)
        self.text.bind("<Down>", self.on_down)
        self.text.bind("<BackSpace>", self.on_backspace)
        self.text.bind("<Delete>", self.on_delete)
        self.text.bind("<Home>", self.on_home)
        
        # Update prompt position
        self.update_prompt_mark()
        
        # Set initial cursor position
        self.text.mark_set("insert", "end")
        self.text.see("end")

    def update_prompt_mark(self):
        """Update the current prompt position mark"""
        self.prompt_mark = self.text.index("end-1c linestart")
        self.current_prompt_pos = self.text.index(f"{self.prompt_mark}+2c")

    def on_return(self, event):
        """Handle Enter key press"""
        command = self.text.get(f"{self.prompt_mark}+2c", "end-1c").strip()
        
        if command:
            if not self.command_history or command != self.command_history[-1]:
                self.command_history.append(command)
            self.history_index = len(self.command_history)
            
            result = self.command_interpreter.execute(command)
            
            if result == "\x1bCLEAR":
                self.clear_output()
            else:
                self.text.insert("end", f"\n{result}\n\n> ")
            
            self.update_prompt_mark()
        else:
            self.text.insert("end", "\n> ")
            self.update_prompt_mark()
        
        self.text.see("end")
        return "break"

    def on_keypress(self, event):
        """Handle general key presses"""
        allowed_events = {"Control", "Shift", "Left", "Right", "Home", "End",
                         "Up", "Down", "Tab", "Delete", "BackSpace"}
        
        if event.keysym in allowed_events or event.state & 4:
            return None
            
        if self.text.compare("insert", "<", self.current_prompt_pos):
            self.text.mark_set("insert", "end")
            self.text.see("end")
            
        return None

    def on_backspace(self, event):
        """Handle Backspace key"""
        if self.text.compare("insert", "<=", self.current_prompt_pos):
            return "break"
        return None

    def on_delete(self, event):
        """Handle Delete key"""
        if self.text.compare("insert", "<", self.current_prompt_pos):
            return "break"
        return None

    def on_home(self, event):
        """Handle Home key"""
        self.text.mark_set("insert", self.current_prompt_pos)
        return "break"

    def on_up(self, event):
        """Handle Up arrow key"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.replace_current_line(self.command_history[self.history_index])
        return "break"

    def on_down(self, event):
        """Handle Down arrow key"""
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.replace_current_line(self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.replace_current_line("")
        return "break"

    def replace_current_line(self, new_text):
        """Replace the current command line with new text"""
        self.text.delete(self.current_prompt_pos, "end-1c")
        self.text.insert(self.current_prompt_pos, new_text)

    def clear_output(self):
        """Clear the output area"""
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "Command prompt ready\n\n> ")
        self.update_prompt_mark()
        self.text.see("end")

    def append_output(self, text):
        """Append text to the output area"""
        current_command = self.text.get(self.current_prompt_pos, "end-1c")
        self.text.delete(self.prompt_mark, "end-1c")
        self.text.insert("end", text + "> " + current_command)
        self.update_prompt_mark()


    def replace_current_line(self, new_text):
        """Replace the current command line with new text"""
        self.text.delete(self.current_prompt_pos, "end-1c")
        self.text.insert(self.current_prompt_pos, new_text)

    def process_command(self, event=None):
            """Process entered command and update main display"""
            command = self.cmd_entry.get().strip()
            if command:
                # Add to history
                self.command_history.append(command)
                self.history_index = len(self.command_history)
                
                # Show command in output
                output_text = f"> {command}\n"
                
                # Process command
                result = self.command_interpreter.execute(command)
                
                # Handle clear screen command
                if result == "\x1bCLEAR":
                    self.clear_output()
                    # Clear main display if available
                    main_window = self.winfo_toplevel().main_app
                    if main_window and hasattr(main_window, 'clear_cmd_display'):
                        main_window.clear_cmd_display()
                else:
                    # Add result to output
                    output_text += f"{result}\n\n"
                    self.append_output(output_text)
                    
                    # Update main view display if available
                    main_window = self.winfo_toplevel().main_app
                    if main_window and hasattr(main_window, 'update_cmd_display'):
                        main_window.update_cmd_display(output_text)
                
                # Clear entry
                self.cmd_entry.delete(0, tk.END)
            
            return "break"

    def previous_command(self, event=None):
        """Show previous command from history"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, self.command_history[self.history_index])
        return "break"

    def next_command(self, event=None):
        """Show next command from history"""
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.cmd_entry.delete(0, tk.END)
        return "break"

    def process_command_text(self, command, show_in_prompt=True):
        """Process command text (can be called externally)"""
        if command:
            if show_in_prompt:
                self.append_output(f"> {command}\n")
            
            result = self.command_interpreter.execute(command)
            
            if result == "\x1bCLEAR":
                self.clear_output()
            elif show_in_prompt:
                self.append_output(f"{result}\n\n")
            
            return result