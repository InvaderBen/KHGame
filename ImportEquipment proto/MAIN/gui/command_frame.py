import tkinter as tk
from tkinter import ttk
from COMMANDS.command_interpreter import CommandInterpreter

class CommandFrame(ttk.Frame):
    def __init__(self, parent, equipment_manager):
        super().__init__(parent)
        self.equipment_manager = equipment_manager
        self.command_interpreter = CommandInterpreter(equipment_manager)
        self.setup_command_area()
        
        # Make the frame expand to fill parent
        self.pack(fill="both", expand=True)

    def setup_command_area(self):
        # Output area (takes most of the space)
        self.output_text = tk.Text(self, wrap=tk.WORD)
        self.output_text.pack(side="top", fill="both", expand=True)
        
        # Scrollbar for output
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", 
                                     command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        
        # Command entry area at bottom
        self.cmd_frame = ttk.Frame(self)
        self.cmd_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        
        self.prompt_label = ttk.Label(self.cmd_frame, text=">", 
                                    font=('Courier', 10))
        self.prompt_label.pack(side="left", padx=(5,2))
        
        self.cmd_entry = ttk.Entry(self.cmd_frame)
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        
        # Bind events
        self.cmd_entry.bind('<Return>', self.process_command)
        self.cmd_entry.bind('<Up>', self.previous_command)
        self.cmd_entry.bind('<Down>', self.next_command)
        
        # Initialize command history
        self.command_history = []
        self.history_index = 0
        
        # Show welcome message
        self.append_output("Welcome to Equipment Manager Command Prompt\n" +
                         "Type 'help' for available commands\n\n")

    def append_output(self, text):
        """Append text to output area"""
        self.output_text.configure(state='normal')
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state='disabled')
        self.output_text.see(tk.END)

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

    def clear_output(self):
        """Clear the output text area"""
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Command prompt ready\n\n")
        self.output_text.configure(state='disabled')
        self.output_text.see(tk.END)
        
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