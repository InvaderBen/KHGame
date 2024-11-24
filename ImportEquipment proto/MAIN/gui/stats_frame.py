import tkinter as tk
from tkinter import ttk

class StatsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_item = None  # Track currently selected item
        self.stat_entries = {}    # Store entry widgets
        self.setup_layout()

    def setup_layout(self):
        # Create a frame for the stats grid
        self.stats_grid = ttk.Frame(self)
        self.stats_grid.pack(fill="both", expand=True, padx=10, pady=5)

        # Define stats with their types and column layout
        self.stats_layout = [
            # Column 1
            [('name', str), ('type', str), ('strike', int), ('prot', int)],
            # Column 2
            [('defense', int), ('speed', int), ('evade', int), ('block', int)],
            # Column 3
            [('damage', int), ('critical_condition', int), ('total_damage', int)]
        ]

        # Create columns
        for col, stats in enumerate(self.stats_layout):
            column_frame = ttk.Frame(self.stats_grid)
            column_frame.grid(row=0, column=col, padx=10, sticky="n")

            # Create header
            ttk.Label(
                column_frame, 
                text=f"-- Stats Group {col + 1} --", 
                font=('Arial', 10, 'bold')
            ).pack(pady=(0, 10))

            # Create stat entries
            for row, (stat, stat_type) in enumerate(stats):
                stat_frame = ttk.LabelFrame(
                    column_frame, 
                    text=stat.replace('_', ' ').title()
                )
                stat_frame.pack(fill="x", pady=5)

                entry = ttk.Entry(stat_frame, width=20)
                entry.pack(side="left", padx=5, pady=5)

                modify_btn = ttk.Button(
                    stat_frame, 
                    text="Modify",
                    command=lambda s=stat, e=entry: self.modify_stat(s, e)
                )
                modify_btn.pack(side="left", padx=5, pady=5)

                # Store references
                self.stat_entries[stat] = (entry, modify_btn)

        # Perks section at the bottom
        self.setup_perks_section()

    def setup_perks_section(self):
        self.perks_frame = ttk.LabelFrame(self, text="Perks")
        self.perks_frame.pack(fill="x", padx=10, pady=10)

        # Left side - Listbox
        left_frame = ttk.Frame(self.perks_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Create listbox with scrollbar
        self.perks_listbox = tk.Listbox(left_frame, height=6)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", 
                                command=self.perks_listbox.yview)
        self.perks_listbox.configure(yscrollcommand=scrollbar.set)

        self.perks_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right side - Buttons
        right_frame = ttk.Frame(self.perks_frame)
        right_frame.pack(side="right", fill="y", padx=5, pady=5)

        self.perk_add_button = ttk.Button(right_frame, text="Add", command=self.add_perk)
        self.perk_add_button.pack(fill="x", pady=2)
        
        self.perk_remove_button = ttk.Button(right_frame, text="Remove", command=self.remove_perk)
        self.perk_remove_button.pack(fill="x", pady=2)
        
        self.perk_clear_button = ttk.Button(right_frame, text="Clear", command=self.clear_perks)
        self.perk_clear_button.pack(fill="x", pady=2)

    def populate_stats(self, data):
        """Fill in stat fields with item data"""
        self.clear_stats()
        
        if not data:
            return

        # Fill in stats
        for stat in self.stat_entries:
            if stat in data:
                value = data[stat]
                if value is not None:
                    entry = self.stat_entries[stat][0]  # Get entry widget
                    entry.delete(0, tk.END)
                    entry.insert(0, str(value))

        # Handle perks separately
        self.perks_listbox.delete(0, tk.END)
        if data.get('perks'):
            for perk in data['perks']:
                if perk is not None:
                    self.perks_listbox.insert(tk.END, perk)

    def clear_stats(self):
        """Clear all stat fields"""
        for entry, button in self.stat_entries.values():
            entry.delete(0, tk.END)
        self.perks_listbox.delete(0, tk.END)

    def set_enabled(self, enabled=True):
        """Enable or disable all input fields"""
        state = 'normal' if enabled else 'disabled'
        for entry, button in self.stat_entries.values():
            entry.configure(state=state)
            button.configure(state=state)
        
        self.perks_listbox.configure(state=state)
        self.perk_add_button.configure(state=state)
        self.perk_remove_button.configure(state=state)
        self.perk_clear_button.configure(state=state)

    def modify_stat(self, stat_name, entry_widget):
            """Handle stat modification"""
            if not self.current_item:
                return
                
            value = entry_widget.get().strip()
            if not value:
                return
                
            # Convert item name from display format to storage format
            item_name = self.current_item.replace(' ', '_')
                
            # Handle different types of values
            if stat_name in ['name', 'type']:  # String values need quotes
                if not value.startswith("'"):
                    value = f"'{value}'"
                    
            # Create and execute command with the correct item name format
            command = f"modify '{item_name}' {stat_name} {value}"
            
            main_window = self.winfo_toplevel().main_app
            if main_window and hasattr(main_window, 'cmd_frame'):
                main_window.cmd_frame.process_command_text(command)

    def add_perk(self):
        if not self.current_item:
            return
        dialog = tk.Toplevel(self)
        dialog.title("Add Perk")
        dialog.geometry("300x100")
        dialog.transient(self)
        
        ttk.Label(dialog, text="Enter perk:").pack(pady=5)
        entry = ttk.Entry(dialog)
        entry.pack(fill="x", padx=5)
        
        main_window = self.winfo_toplevel().main_app
        
        def submit():
            perk = entry.get().strip()
            if perk and main_window and hasattr(main_window, 'cmd_frame'):
                command = f"modify '{self.current_item}' perks append '{perk}'"
                main_window.cmd_frame.process_command_text(command)
            dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=submit).pack(pady=5)
        entry.focus_set()

    def remove_perk(self):
        if not self.current_item:
            return
        selection = self.perks_listbox.curselection()
        if selection:
            perk = self.perks_listbox.get(selection)
            main_window = self.winfo_toplevel().main_app
            if main_window and hasattr(main_window, 'cmd_frame'):
                command = f"modify '{self.current_item}' perks remove '{perk}'"
                main_window.cmd_frame.process_command_text(command)

    def clear_perks(self):
        if not self.current_item:
            return
        main_window = self.winfo_toplevel().main_app
        if main_window and hasattr(main_window, 'cmd_frame'):
            command = f"modify '{self.current_item}' perks clear"
            main_window.cmd_frame.process_command_text(command)