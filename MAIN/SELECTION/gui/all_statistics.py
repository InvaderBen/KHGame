import tkinter as tk
from tkinter import ttk

class AllStatistics(ttk.Frame):
    """
    A tkinter Frame that displays all statistics for a knight, including abilities,
    skills, combat stats, and available stances based on skill level.
    """
    def __init__(self, parent, data_manager):
        """Initialize the statistics display frame"""
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_knight = None
        self.create_widgets()

    def create_widgets(self):
        """Create and configure all display widgets"""
        # Create notebook for multiple tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create and configure Stats tab
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text='Stats')
        
        # Create treeview for displaying stats
        self.tree = ttk.Treeview(self.stats_frame, columns=('Value'), show='tree headings')
        self.tree.heading('Value', text='Value')
        self.tree.column('Value', width=100, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Create and configure Stances tab
        self.stances_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stances_frame, text='Stances')
        
        # Create treeview for displaying stances with all relevant columns
        self.stances_tree = ttk.Treeview(self.stances_frame, 
                                       columns=('Name', 'Level', 'Category', 'AP Cost', 
                                              'Defense', 'Strike', 'Block', 'Evade', 
                                              'Balance', 'Damage', 'Combined'),
                                       show='headings')
        
        # Configure all columns for the stances display
        columns = [
            ('Name', 'Name', 150),
            ('Level', 'Level', 80),
            ('Category', 'Category', 150),
            ('AP Cost', 'AP', 50),
            ('Defense', 'Def', 50),
            ('Strike', 'Str', 50),
            ('Block', 'Blk', 50),
            ('Evade', 'Eva', 50),
            ('Balance', 'Bal', 50),
            ('Damage', 'Dmg', 50),
            ('Combined', 'Total', 70)
        ]
        
        # Apply column configurations
        for col_id, heading, width in columns:
            self.stances_tree.heading(col_id, text=heading)
            self.stances_tree.column(col_id, width=width, anchor='center')
        
        # Add scrollbar to stances tree
        scrollbar = ttk.Scrollbar(self.stances_frame, orient="vertical", 
                                command=self.stances_tree.yview)
        self.stances_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack stance widgets
        self.stances_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_stances(self):
        """Load and display stances based on knight's stance skill level"""
        # Clear existing items
        for item in self.stances_tree.get_children():
            self.stances_tree.delete(item)
        
        if not self.current_knight:
            return
            
        # Get stances and filter based on knight's skill level
        stances = self.data_manager.get_stances()
        stance_skill = self.current_knight.stance_skill
        
        # Map stance skill levels to available stance types
        available_levels = {
            1: ["Basic"],
            2: ["Basic", "Advanced"],
            3: ["Basic", "Advanced", "Expert"]
        }
        
        allowed_levels = available_levels.get(stance_skill, [])
        available_stances = [s for s in stances if s['stance_level'] in allowed_levels]
        
        # Sort stances by level, category, and name
        available_stances.sort(key=lambda x: (x['stance_level'], x['category'], x['name']))
        
        # Insert stances into tree with proper formatting
        for stance in available_stances:
            attrs = stance['attributes']
            values = (
                stance['name'],
                stance['stance_level'],
                stance['category'],
                stance['action_point_cost'],
                attrs['defense'],
                attrs['strike'],
                attrs['block'],
                attrs['evade'],
                attrs['balance'],
                attrs['damage'],
                stance['combined_value']
            )
            
            # Apply color coding based on stance category
            if stance['category'] == 'Defensive Stances':
                tags = ['defensive']  # Light blue
            elif stance['category'] == 'Offensive Stances':
                tags = ['offensive']  # Light red
            elif stance['category'] == 'Balanced Stances':
                tags = ['balanced']   # Light green
            elif stance['category'] == 'Evasive Stances':
                tags = ['evasive']    # Light magenta/pink
            elif stance['category'] == 'Execution Stances':
                tags = ['execution']  # Light yellow
            else:
                tags = []
                
            self.stances_tree.insert('', 'end', values=values, text=stance['name'], tags=tags)
        
        # Configure color tags
        self.stances_tree.tag_configure('defensive', background='#e8f0ff')  # Light blue
        self.stances_tree.tag_configure('offensive', background='#ffd6d6')  # Light red
        self.stances_tree.tag_configure('balanced', background='#e8ffe8')   # Light green
        self.stances_tree.tag_configure('evasive', background='#ffe8ff')    # Light magenta
        self.stances_tree.tag_configure('execution', background='#fff7e6')  # Light yellow

    def load_knight(self, knight):
        """Load a knight's data and update all displays"""
        self.current_knight = knight
        self.update_display()
        self.load_stances()

    def update_display(self):
        """Update the stats display with current knight's information"""
        if not self.current_knight:
            return

        self.tree.delete(*self.tree.get_children())

        # Get all stats from the knight
        stats = self.current_knight.get_stats()
        combat_stats = self.current_knight.calculate_combat_stats()
        
        # Display regular abilities and skills
        for category, values in stats.items():
            category_id = self.tree.insert('', 'end', text=category.replace('_', ' ').title())
            for stat, value in values.items():
                self.tree.insert(category_id, 'end', text=stat, values=(value,))

        # Add combat stats category
        combat_id = self.tree.insert('', 'end', text='Combat Statistics')
        for stat, value in combat_stats.items():
            # Clean up the stat name
            clean_stat = stat.replace('.', '').replace('Combat ', '')
            self.tree.insert(combat_id, 'end', text=clean_stat, values=(value,))