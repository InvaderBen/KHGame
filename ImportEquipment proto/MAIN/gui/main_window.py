from tkinter import ttk
import tkinter as tk
from .stats_frame import StatsFrame
from .command_frame import CommandFrame
from .constants import *

class CategoryTab(ttk.Frame):
    def __init__(self, parent, category, equipment_manager):
        super().__init__(parent)
        self.category = category
        self.equipment_manager = equipment_manager
        
        # Create and configure treeview
        self.tree = ttk.Treeview(self, selectmode='browse')
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack treeview and scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Store file paths
        self.file_paths = {}
        
        # Load initial items
        self.load_items()
    
    def load_items(self):
        """Load items into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get equipment list
        equipment_list = self.equipment_manager.get_equipment_list(self.category)
        
        # Add items to treeview
        for path in equipment_list:
            name = self.equipment_manager.get_equipment_name(path)
            item_id = self.tree.insert("", "end", text=name)
            self.file_paths[item_id] = path

class MainWindow:
    def __init__(self, root, equipment_manager):
        self.root = root
        self.equipment_manager = equipment_manager
        self.setup_main_window()
        
    def setup_main_window(self):
        # Create main horizontal split
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill="both", expand=True)
        
        # Setup panels
        self.left_frame = self.setup_left_panel()
        self.right_frame = self.setup_right_panel()
        
        self.main_paned.add(self.left_frame, weight=1)
        self.main_paned.add(self.right_frame, weight=3)
        
    def setup_left_panel(self):
        frame = ttk.Frame()
        
        # Refresh button
        self.refresh_btn = ttk.Button(
            frame, 
            text="↻ REFRESH",
            command=self.refresh_all
        )
        self.refresh_btn.pack(fill="x", padx=5, pady=5)
        
        # Create notebook for category tabs
        self.category_notebook = ttk.Notebook(frame)
        self.category_notebook.pack(fill="both", expand=True, padx=5)
        
        # Create category tabs
        self.category_tabs = {}
        for category in self.equipment_manager.get_categories():
            tab = CategoryTab(self.category_notebook, category, self.equipment_manager)
            self.category_tabs[category] = tab
            self.category_notebook.add(tab, text=category.title())
            
            # Bind selection event
            tab.tree.bind('<<TreeviewSelect>>', 
                         lambda e, t=tab: self.on_item_selected(e, t))
        
        return frame
    
    def setup_right_panel(self):
            frame = ttk.Frame()
            
            # Create vertical paned window
            self.view_paned = ttk.PanedWindow(frame, orient=tk.VERTICAL)
            self.view_paned.pack(fill="both", expand=True)
            
            # Create view tabs
            self.view_notebook = ttk.Notebook(self.view_paned)
            
            # Main view (stats and command display)
            self.main_view = ttk.Frame(self.view_notebook)
            self.view_notebook.add(self.main_view, text="MAIN")
            
            # Stats view takes most of the space
            self.stats_view = StatsFrame(self.main_view)
            self.stats_view.pack(fill="both", expand=True)
            
            # Read-only command display at bottom of main view
            self.cmd_display = self.create_cmd_display(self.main_view)
            self.cmd_display.pack(fill="x", padx=5, pady=5)
            
            # CMD view (full command prompt)
            self.cmd_view = ttk.Frame(self.view_notebook)
            self.view_notebook.add(self.cmd_view, text="CMD")
            
            # Add notebook to paned window
            self.view_paned.add(self.view_notebook)
            
            # Command frame (only in CMD view)
            self.cmd_frame = CommandFrame(self.cmd_view, self.equipment_manager)
            self.cmd_frame.pack(fill="both", expand=True)
            
            return frame

    
    def create_cmd_display(self, parent):
        """Create a read-only command display"""
        frame = ttk.LabelFrame(parent, text="Command Output")
        
        # Create text widget for output display
        self.output_display = tk.Text(frame, height=4, wrap=tk.WORD)
        self.output_display.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", 
                                command=self.output_display.yview)
        scrollbar.pack(side="right", fill="y")
        self.output_display.configure(yscrollcommand=scrollbar.set)
        
        # Make it read-only
        self.output_display.configure(state='disabled')
        
        return frame

    def update_cmd_display(self, text):
        """Update the command display in main view"""
        self.output_display.configure(state='normal')
        self.output_display.delete(1.0, tk.END)
        self.output_display.insert(tk.END, text)
        self.output_display.configure(state='disabled')
        self.output_display.see(tk.END)

    def refresh_all(self):
        """Refresh all category tabs"""
        for tab in self.category_tabs.values():
            tab.load_items()
        # Execute refresh command
        self.cmd_frame.process_command_text("refresh", show_in_prompt=True)
    
    def on_item_selected(self, event, tab):
        """Handle item selection in treeview"""
        selection = tab.tree.selection()
        if selection:
            item_id = selection[0]
            item_name = tab.tree.item(item_id)['text']
            file_path = tab.file_paths[item_id]
            
            # Store current item name
            self.current_item = item_name
            
            # Get item data
            data = self.equipment_manager.load_equipment_data(file_path)
            
            # Update stats view
            self.stats_view.current_item = item_name
            self.stats_view.populate_stats(data)
            self.stats_view.set_enabled(True)
            
            # Show in command prompt
            self.cmd_frame.process_command_text(f"show '{item_name}'")
        else:
            # Clear selection
            self.current_item = None
            self.stats_view.current_item = None
            self.stats_view.clear_stats()
            self.stats_view.set_enabled(False)