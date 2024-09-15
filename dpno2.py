#os essentials
import json
import os

#tinker modules
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox

#custom scripts
from Knight import Knight

class KnightApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Knights Information")
        
        self.SKILL_NAMES = ['Covering', 'Armor', 'Offense', 'Ranged', 'Riding', 'Shield', 'Unarmed', 'Weapon']
        self.skill_spinboxes = {}
        self.skill_progression_labels = {}
        self.phys_spinboxes = {}
        self.pers_spinboxes = {}

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        
        self.knights = {}
        self.edit_widgets = {}
        self.stat_entries = {}
        self.current_knight = None
        self.sumOfSkillCosts = 0
        self.skillpoints = 0
        
        self.remaining_skill_points = self.skillpoints - self.sumOfSkillCosts

        self.storage_data = {
            'Weapons': [],
            'Shields': [],
            'Armors': [],
        }

        self.inventory_data = {
            'Weapons': [],
            'Shields': [],
            'Armors': [],
        }

        # Initialize dictionary for treeview widgets
        self.treeview_types = {
            'Weapons_Inventory': None,
            'Shields_Inventory': None,
            'Armors_Inventory': None,
            'Weapons_Storage': None,
            'Shields_Storage': None,
            'Armors_Storage': None,
        }


        self.create_knight_list()
        self.create_notebook()
        self.create_stats_treeview()
        self.load_existing_knights()

        self.general(self.master)
        self.create_detail_frame(self.main_frame)

        # Disable spinboxes initially
        self.set_spinboxes_state('disabled')

    def set_spinboxes_state(self, state):
        for spinbox in self.phys_spinboxes.values():
            spinbox.config(state=state)
        for spinbox in self.pers_spinboxes.values():
            spinbox.config(state=state)
        for spinbox in self.skill_spinboxes.values():
            spinbox.config(state=state)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.sheet_1 = tk.Frame(self.notebook)
        self.sheet_2 = tk.Frame(self.notebook)
        self.sheet_3 = tk.Frame(self.notebook)
        self.sheet_4 = tk.Frame(self.notebook)

        self.notebook.add(self.sheet_1, text='Edit Abilities')
        self.notebook.add(self.sheet_2, text='All Statistics')
        self.notebook.add(self.sheet_3, text='Skills')
        self.notebook.add(self.sheet_4, text='Weapons')

        self.create_ability_editors(self.sheet_1)
        self.create_skill_editors(self.sheet_3)
        self.create_equipment_notebook(self.sheet_4)

    def clear_sheets(self):
        for widget in self.sheet_1.winfo_children():
            widget.destroy()
        for widget in self.sheet_2.winfo_children():
            widget.destroy()
        for widget in self.sheet_3.winfo_children():
            widget.destroy()
        for widget in self.sheet_4.winfo_children():
            widget.destroy()
        
        # Reset the stats_tree attribute
        self.stats_tree = None
        self.skill_spinboxes = {}

    def create_stats_treeview(self):
        # Create a frame for the treeview
        tree_frame = tk.Frame(self.sheet_2)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create the treeview
        self.stats_tree = ttk.Treeview(tree_frame, columns=("Value",), show="tree headings")
        self.stats_tree.heading("Value", text="Value")
        self.stats_tree.column("Value", width=100, anchor="center")
        # Create scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.stats_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.stats_tree.xview)
        self.stats_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        self.stats_tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

    def update_stats_treeview(self):
        if not self.current_knight:
            return

        if not self.stats_tree:
            self.create_stats_treeview()

        # Clear existing items
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)

        # Add Physical Abilities
        phys_id = self.stats_tree.insert("", "end", text="Physical Abilities", open=True)
        for ability, value in self.current_knight.get_stats()['abilities_physical'].items():
            if ability != 'Sum':
                self.stats_tree.insert(phys_id, "end", text=ability, values=(value,))

        # Add Personality Traits
        pers_id = self.stats_tree.insert("", "end", text="Personality Traits", open=True)
        for ability, value in self.current_knight.get_stats()['abilities_personality'].items():
            if ability != 'Sum':
                self.stats_tree.insert(pers_id, "end", text=ability, values=(value,))

        # Add Core Stats
        core_id = self.stats_tree.insert("", "end", text="Core", open=True)
        for stat, value in self.current_knight.calculate_core_stats().items():
            self.stats_tree.insert(core_id, "end", text=stat, values=(value,))

        # Add Skills
        skills_id = self.stats_tree.insert("", "end", text="Skills", open=True)
        for skill, (level, value) in self.current_knight.get_stats()['skills'].items():
            self.stats_tree.insert(skills_id, "end", text=skill, values=(f"{level} ({value})",))

    def clear_all_ui_elements(self):
        # Clear ability editors
        self.clear_and_disable_editors()
        
        # Clear skill editors
        self.clear_and_disable_skill_editors()
        
        # Clear the stats treeview
        if hasattr(self, 'stats_tree') and self.stats_tree:
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)

#Displaying the Knight Object: -
    def create_knight_list(self):
        list_frame = tk.Frame(self.main_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.knight_listbox = tk.Listbox(list_frame, width=20)
        self.knight_listbox.pack(fill=tk.BOTH, expand=1)
        self.knight_listbox.bind('<<ListboxSelect>>', self.on_knight_select)
        self.knight_listbox.bind('<Double-1>', self.edit_knight_name)

        add_button = tk.Button(list_frame, text="New Knight", command=self.add_knight)
        add_button.pack(side=tk.LEFT, pady=5)

        delete_button = tk.Button(list_frame, text="Delete Knight", command=self.delete_knight)
        delete_button.pack(side=tk.LEFT, pady=5)

    def on_knight_select(self, event=None):
        if event and hasattr(event, 'widget'):
            if not event.widget.curselection():
                return
            index = event.widget.curselection()[0]
        else:
            if self.knight_listbox.size() == 0:
                self.clear_all_ui_elements()
                return
            index = self.knight_listbox.size() - 1
        
        knight_id = list(self.knights.keys())[index]
        self.current_knight = self.knights[knight_id]
        
        # Recreate and populate UI elements
        self.recreate_ability_editors()
        self.recreate_skill_editors()
        self.update_stats_treeview()

        self.updateGeneral()
#---

#Creating and Loading the Knight Object: -
    def add_knight(self):
        new_id = self.get_next_available_id()
        name = f'knight_no{new_id + 1}'
        
        new_knight = Knight(name)
        self.knights[new_id] = new_knight
        
        self.knight_listbox.insert(tk.END, name)
        self.knight_listbox.selection_clear(0, tk.END)
        self.knight_listbox.selection_set(tk.END)
        self.save_knight_to_file(new_id, new_knight)
        
        # Recreate ability editors
        self.recreate_ability_editors()
        
        # Set the current knight and update the view
        self.on_knight_select()
        
        # Start editing the newly added knight's name
        self.edit_knight_name(index=self.knight_listbox.size() - 1)

    def load_existing_knights(self):
        if not os.path.exists('knights'):
            os.makedirs('knights')
            return

        for filename in os.listdir('knights'):
            if filename.endswith('.json'):
                knight_id = int(filename.split('_')[1].split('.')[0])
                knight = self.load_knight_from_file(knight_id)
                if knight:
                    self.knights[knight_id] = knight
                    self.knight_listbox.insert(tk.END, knight.name)

    def load_knight_from_file(self, knight_id):
        filename = f'knights/knight_{knight_id}.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                knight_data = json.load(f)
            
            knight = Knight(knight_data['name'])
            knight.age = knight_data['age']
            knight.skillPoints = knight_data['skillPoints']
            knight.persPoints = knight_data['persPoints']
            knight.physPoints = knight_data['physPoints']
            
            for ability, value in knight_data['physical_abilities'].items():
                setattr(knight, ability, value)
            
            for ability, value in knight_data['personality_abilities'].items():
                setattr(knight, ability, value)
            
            for ability, value in knight_data['core_abilities'].items():
                setattr(knight, ability, value)
            
            for skill_name, skill_data in knight_data['skills'].items():
                knight.skills[skill_name].current_level = skill_data['level']
                knight.skills[skill_name].progression = skill_data['progression']
            
            # Calculate sums after loading all abilities
            knight.update_sums()
            
            return knight
        else:
            print(f"No data file found for knight with ID {knight_id}")
            return None

    def get_next_available_id(self):
        if not self.knights:
            return 0
        return max(self.knights.keys()) + 1
    #Save the Knight's data on a .json file
    def save_knight_to_file(self, knight_id, knight):
        if not os.path.exists('knights'):
            os.makedirs('knights')
        
        # Calculate the sums
        phys_sum = sum(getattr(knight, ability) for ability in 
                    ['strength', 'endurance', 'massive', 'resistance', 
                        'reflex', 'dexterity', 'perception', 'coordination'])
        pers_sum = sum(getattr(knight, ability) for ability in 
                    ['intelligence', 'willpower', 'emotion', 'creativity', 
                        'brave', 'charisma'])
        
        knight_data = {
            'name': knight.name,
            'age': knight.age,
            'skillPoints': knight.skillPoints,
            'persPoints': 20 - pers_sum,  # Update persPoints
            'physPoints': 30 - phys_sum,  # Update physPoints
            'physical_abilities': {
                'strength': knight.strength,
                'endurance': knight.endurance,
                'massive': knight.massive,
                'resistance': knight.resistance,
                'reflex': knight.reflex,
                'dexterity': knight.dexterity,
                'perception': knight.perception,
                'coordination': knight.coordination
            },
            'personality_abilities': {
                'intelligence': knight.intelligence,
                'willpower': knight.willpower,
                'emotion': knight.emotion,
                'creativity': knight.creativity,
                'brave': knight.brave,
                'charisma': knight.charisma
            },
            'core_abilities': {
                'focus': knight.focus,
                'communication': knight.communication
            },
            'skills': {skill_name: {'level': skill.current_level, 'progression': skill.progression}
                    for skill_name, skill in knight.skills.items()},
            'equipment':{
                'weapons': knight.equipment['weapons'],
                'shields': knight.equipment['shields'],
                'armor': knight.equipment['armor']
            }
        }
        filename = f'knights/knight_{knight_id}.json'
        with open(filename, 'w') as f:
            json.dump(knight_data, f, indent=4)

        print(f"Knight data saved to {filename}")

    def delete_knight(self):
        if self.knight_listbox.curselection():
            index = self.knight_listbox.curselection()[0]
            answer = messagebox.askyesno("Delete Knight", "Are you sure you want to delete this knight?")
            if answer:
                # Remove the knight's file
                knight_id = list(self.knights.keys())[index]
                filename = f'knights/knight_{knight_id}.json'
                if os.path.exists(filename):
                    os.remove(filename)
                
                # Remove from listbox and dictionary
                self.knight_listbox.delete(index)
                del self.knights[knight_id]
                
                # Clear the current knight
                self.current_knight = None
                
                # Clear all UI elements
                self.clear_all_ui_elements()
                
                # Renumber the remaining knights in the listbox
                for i, knight in enumerate(self.knights.values()):
                    self.knight_listbox.delete(i)
                    self.knight_listbox.insert(i, knight.name)
                
                # If there are remaining knights, select the first one
                if self.knights:
                    self.knight_listbox.selection_set(0)
                    self.on_knight_select()
                else:
                    # If no knights left, clear everything
                    self.clear_sheets()
#---

#Edit the Knight's name: -
    def edit_knight_name(self, event=None, index=None):
        if index is None:
            if not self.knight_listbox.curselection():
                return
            index = self.knight_listbox.curselection()[0]
        
        # If there's an ongoing edit, finish it first
        self.finish_edit()
        
        bbox = self.knight_listbox.bbox(index)
        if not bbox:
            return
        
        x, y, width, height = bbox
        entry = tk.Entry(self.knight_listbox, width=width//7)
        entry.insert(0, self.knight_listbox.get(index))
        entry.selection_range(0, tk.END)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus_set()
        entry.bind("<Return>", lambda e: self.finish_edit(index))
        entry.bind("<FocusOut>", lambda e: self.finish_edit(index))
        
        self.edit_widgets[index] = entry

    def finish_edit(self, index=None):
        if index is None:
            indices = list(self.edit_widgets.keys())
        else:
            indices = [index]
        
        for idx in indices:
            entry = self.edit_widgets.get(idx)
            if entry:
                new_name = entry.get()
                self.knight_listbox.delete(idx)
                self.knight_listbox.insert(idx, new_name)
                
                # Update the Knight object's name
                knight_id = list(self.knights.keys())[idx]
                self.knights[knight_id].name = new_name
                
                # Update the file with the new name
                self.save_knight_to_file(knight_id, self.knights[knight_id])
                
                entry.destroy()
                del self.edit_widgets[idx]
        
        # Refresh the stats view in case the current knight's name was changed
        if self.current_knight:
            self.update_stats_treeview()
#---

#Edit abilities and generate UI for sheet_1:-
    def create_ability_editors(self, parent):
        # Physical Abilities Frame
        phys_frame = tk.LabelFrame(parent, text="Physical Abilities")
        phys_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Personality Traits Frame
        pers_frame = tk.LabelFrame(parent, text="Personality Traits")
        pers_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create spinboxes for Physical Abilities
        self.phys_spinboxes = {}
        for i, ability in enumerate(['Strength', 'Endurance', 'Massive', 'Resistance', 'Reflex', 'Dexterity', 'Perception', 'Coordination']):
            label = tk.Label(phys_frame, text=ability)
            label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            spinbox = tk.Spinbox(phys_frame, from_=1, to=6, width=5, command=lambda: self.update_points(), state='disabled')
            spinbox.grid(row=i, column=1, padx=5, pady=2)
            self.phys_spinboxes[ability.lower()] = spinbox

        # Create spinboxes for Personality Traits
        self.pers_spinboxes = {}
        for i, trait in enumerate(['Intelligence', 'Willpower', 'Emotion', 'Creativity', 'Brave', 'Charisma']):
            label = tk.Label(pers_frame, text=trait)
            label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            spinbox = tk.Spinbox(pers_frame, from_=1, to=6, width=5, command=lambda: self.update_points(), state='disabled')
            spinbox.grid(row=i, column=1, padx=5, pady=2)
            self.pers_spinboxes[trait.lower()] = spinbox

        # Create labels for points
        self.phys_points_label = tk.Label(phys_frame, text="Physical Points: --")
        self.phys_points_label.grid(row=8, column=0, columnspan=2, pady=10)

        self.pers_points_label = tk.Label(pers_frame, text="Personality Points: --")
        self.pers_points_label.grid(row=6, column=0, columnspan=2, pady=10)
        
    def recreate_ability_editors(self):
        # Clear existing widgets in sheet_1
        for widget in self.sheet_1.winfo_children():
            widget.destroy()
        
        # Recreate ability editors
        self.create_ability_editors(self.sheet_1)
        self.populate_ability_editors()

    def update_points(self):
        if not self.current_knight:
            return

        phys_sum = 0
        pers_sum = 0

        # Update physical abilities and sum
        for ability, spinbox in self.phys_spinboxes.items():
            value = int(spinbox.get())
            self.current_knight.set_physical_stat(ability, value)
            phys_sum += value

        # Update personality traits and sum
        for trait, spinbox in self.pers_spinboxes.items():
            value = int(spinbox.get())
            self.current_knight.set_personality_stat(trait, value)
            pers_sum += value

        # Update the sums in the Knight object
        self.current_knight.phySum = phys_sum
        self.current_knight.perSum = pers_sum

        phys_points = 30 - phys_sum
        pers_points = 20 - pers_sum

        self.phys_points_label.config(text=f"Physical Points: {phys_points}")
        self.pers_points_label.config(text=f"Personality Points: {pers_points}")

        # Lock/unlock spinboxes based on points
        self.lock_unlock_spinboxes(self.phys_spinboxes, phys_points)
        self.lock_unlock_spinboxes(self.pers_spinboxes, pers_points)

        # Update the knight's data in the file
        knight_id = list(self.knights.keys())[list(self.knights.values()).index(self.current_knight)]
        self.save_knight_to_file(knight_id, self.current_knight)

        # Update the stats treeview
        self.update_stats_treeview()

    def update_sums(self):
        if not self.current_knight:
            return

        self.current_knight.phySum = sum(int(spinbox.get()) for spinbox in self.phys_spinboxes.values())
        self.current_knight.perSum = sum(int(spinbox.get()) for spinbox in self.pers_spinboxes.values())

        # Update the knight's data in the file
        knight_id = list(self.knights.keys())[list(self.knights.values()).index(self.current_knight)]
        self.save_knight_to_file(knight_id, self.current_knight)

        # Update the stats treeview
        self.update_stats_treeview()

    def lock_unlock_spinboxes(self, spinboxes, points):
        for spinbox in spinboxes.values():
            current_value = int(spinbox.get())
            if points <= 0:
                spinbox.config(to=current_value)
            else:
                spinbox.config(to=6)

    def populate_ability_editors(self):
        if not self.current_knight:
            self.clear_and_disable_editors()
            return

        # Check if editors exist, if not, recreate them
        if not hasattr(self, 'phys_spinboxes') or not self.phys_spinboxes:
            self.recreate_ability_editors()

        for ability, spinbox in self.phys_spinboxes.items():
            spinbox.config(state='normal')
            spinbox.delete(0, tk.END)
            spinbox.insert(0, getattr(self.current_knight, ability))
            spinbox.config(state='readonly')

        for trait, spinbox in self.pers_spinboxes.items():
            spinbox.config(state='normal')
            spinbox.delete(0, tk.END)
            spinbox.insert(0, getattr(self.current_knight, trait))
            spinbox.config(state='readonly')

        self.update_points()

    def clear_and_disable_editors(self):
        for spinbox in self.phys_spinboxes.values():
            spinbox.config(state='normal')
            spinbox.delete(0, tk.END)
            spinbox.config(state='disabled')

        for spinbox in self.pers_spinboxes.values():
            spinbox.config(state='normal')
            spinbox.delete(0, tk.END)
            spinbox.config(state='disabled')

        self.phys_points_label.config(text="Physical Points: --")
        self.pers_points_label.config(text="Personality Points: --")

#Edit Skills:-
    def create_skill_editors(self, parent):
        self.skill_frame = tk.LabelFrame(parent, text="Combat Skills")
        self.skill_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for i, skill_name in enumerate(self.SKILL_NAMES):
            label = tk.Label(self.skill_frame, text=skill_name)
            label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            spinbox = tk.Spinbox(self.skill_frame, from_=1, to=10, width=5,
                                 command=lambda name=skill_name: self.update_skill(name),
                                 state='disabled')  # Start disabled
            spinbox.grid(row=i, column=1, padx=5, pady=2)
            self.skill_spinboxes[skill_name] = spinbox

            progression_label = tk.Label(self.skill_frame, text="")
            progression_label.grid(row=i, column=2, padx=5, pady=2)
            self.skill_progression_labels[skill_name] = progression_label

        self.skill_points_label = tk.Label(self.skill_frame, text="Remaining Skill Points: --")
        self.skill_points_label.grid(row=len(self.SKILL_NAMES), column=0, columnspan=3, pady=10)

    def update_skill(self, skill_name):
        if not self.current_knight:
            return

        new_level = int(self.skill_spinboxes[skill_name].get())
        old_level = self.current_knight.get_skill_level(skill_name)
        
        if new_level > old_level:
            cost = sum(self.current_knight.skills[skill_name].progression[old_level-1:new_level-1])
            
            if cost > self.current_knight.skillPoints:
                self.skill_spinboxes[skill_name].set(old_level)
                return
            
            self.current_knight.skillPoints -= cost
        else:
            refund = sum(self.current_knight.skills[skill_name].progression[new_level-1:old_level-1])
            self.current_knight.skillPoints += refund

        self.current_knight.set_skill_level(skill_name, new_level)
        
        knight_id = list(self.knights.keys())[list(self.knights.values()).index(self.current_knight)]
        self.save_knight_to_file(knight_id, self.current_knight)
        
        self.update_skill_points_display()
        self.update_stats_treeview()
        self.update_skill_progression_labels()
        self.update_spinbox_caps()

    def update_skill_points(self):
        if not self.current_knight:
            return

        total_used_points = 0
        for skill_name, spinbox in self.skill_spinboxes.items():
            current_level = int(spinbox.get())
            skill = self.current_knight.skills[skill_name]
            total_used_points += sum(skill.progression[:current_level - 1])

        remaining_points = self.current_knight.skillPoints - total_used_points

        self.skill_points_label.config(text=f"Remaining Skill Points: {remaining_points}")

        # Update the knight's skill levels and lock/unlock spinboxes
        for skill_name, spinbox in self.skill_spinboxes.items():
            new_level = int(spinbox.get())
            self.current_knight.set_skill_level(skill_name, new_level)

        # Save the updated knight data
        knight_id = list(self.knights.keys())[list(self.knights.values()).index(self.current_knight)]
        self.save_knight_to_file(knight_id, self.current_knight)

        # Update the stats treeview
        self.update_stats_treeview()

    def update_spinbox_caps(self):
        if not self.current_knight:
            return

        remaining_points = self.current_knight.skillPoints

        for skill_name, spinbox in self.skill_spinboxes.items():
            current_level = int(spinbox.get())
            skill = self.current_knight.skills[skill_name]
            
            max_affordable_level = current_level
            cumulative_cost = 0
            for level in range(current_level, 10):
                level_cost = skill.progression[level - 1]  # Adjust index as progression list is 0-based
                if cumulative_cost + level_cost <= remaining_points:
                    max_affordable_level = level + 1
                    cumulative_cost += level_cost
                else:
                    break
            
            spinbox.config(from_=1, to=max_affordable_level)

    def update_skill_points_display(self):
        if hasattr(self, 'skill_points_label'):
            self.skill_points_label.config(text=f"Remaining Skill Points: {self.current_knight.skillPoints}")

    def update_skill_progression_labels(self):
        if not hasattr(self, 'skill_progression_labels') or not self.current_knight:
            return
        for skill_name, label in self.skill_progression_labels.items():
            current_level = self.current_knight.get_skill_level(skill_name)
            progression_value = self.current_knight.skills[skill_name].get_value(current_level)
            next_cost = self.current_knight.skills[skill_name].progression[current_level-1] if current_level < 10 else "Max"
            label.config(text=f"Current: {progression_value}, Next Cost: {next_cost}")

    def populate_skill_editors(self):
        if not self.current_knight or not hasattr(self, 'skill_spinboxes'):
            return

        for skill_name, spinbox in self.skill_spinboxes.items():
            current_level = self.current_knight.get_skill_level(skill_name)
            spinbox.config(state='normal')
            spinbox.delete(0, tk.END)
            spinbox.insert(0, current_level)
            spinbox.config(state='readonly')
        
        self.update_skill_progression_labels()
        self.update_skill_points_display()
        self.update_spinbox_caps()
        
    def recreate_skill_editors(self):
        # Clear existing widgets in sheet_3
        for widget in self.sheet_3.winfo_children():
            widget.destroy()
        
        # Recreate skill editors
        self.create_skill_editors(self.sheet_3)
        self.populate_skill_editors()

    def clear_and_disable_skill_editors(self):
        if hasattr(self, 'skill_frame'):
            for widget in self.skill_frame.winfo_children():
                widget.destroy()
        
        self.skill_spinboxes = {}
        self.skill_progression_labels = {}
        
        if hasattr(self, 'skill_points_label'):
            self.skill_points_label.config(text="Remaining Skill Points: --")

#To load equipment:--
    def create_equipment_notebook(self, parent):
        self.notebook_frame = ttk.Frame(parent)
        self.notebook_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        for category in ['Weapons', 'Shields', 'Armors']:
            tab = ttk.Frame(self.notebook)

            Inventory = ttk.LabelFrame(tab, text='Inventory')
            Inventory.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            Storage = ttk.LabelFrame(tab, text='Storage')
            Storage.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create treeviews for Inventory and Storage
            self.create_treeview(Inventory, 'Inventory', category)
            self.create_treeview(Storage, 'Storage', category)

            self.load_equipment_data(category)

            self.notebook.add(tab, text=category)

        # Populate treeviews after all data is loaded
        self.populate_treeviews()

    def create_treeview(self, parent, type, category):
        treeframe = ttk.Frame(parent)
        treeframe.pack(fill=tk.BOTH, expand=True)

        columns = ("Name", "Type")
        treeview = ttk.Treeview(treeframe, columns=columns, show="headings")
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor="center")

        # Create scrollbars
        vsb = ttk.Scrollbar(treeframe, orient="vertical", command=treeview.yview)
        hsb = ttk.Scrollbar(treeframe, orient="horizontal", command=treeview.xview)
        treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        treeview.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        treeframe.grid_columnconfigure(0, weight=1)
        treeframe.grid_rowconfigure(0, weight=1)

        # Bind the select event
        treeview.bind("<<TreeviewSelect>>", self.on_item_select)

        # Store treeview reference in dictionary
        self.treeview_types[f'{category}_{type}'] = treeview

    def populate_treeviews(self):
        for category in ['Weapons', 'Shields', 'Armors']:
            storage_treeview = self.treeview_types[f'{category}_Storage']
            inventory_treeview = self.treeview_types[f'{category}_Inventory']

            # Populate Storage treeview
            for item in self.storage_data[category]:
                storage_treeview.insert('', 'end', values=(item['name'], item['weapon_type'] if 'weapon_type' in item else category[:-1]))

            # Populate Inventory treeview (currently empty)
            for item in self.inventory_data[category]:
                inventory_treeview.insert('', 'end', values=(item['name'], item['weapon_type'] if 'weapon_type' in item else category[:-1]))

    def create_detail_frame(self, parent):
        self.detail_frame = ttk.LabelFrame(parent, text="Item Details")
        self.detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.detail_frame.pack_forget()

    def on_item_select(self, event):
        tree = event.widget
        selected_item = tree.focus()
        item_data = tree.item(selected_item)

        # Clear previous details
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        # Show the detail frame only if an item with values is selected
        if item_data['values']:
            self.detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            name, eq_type = item_data['values']
            ttk.Label(self.detail_frame, text=f"Name: {name} - Storage", font=("", 12, "bold")).pack(anchor="w")
            ttk.Label(self.detail_frame, text=f"Type: {eq_type}").pack(anchor="w")
            
            # Fetch actual stats from our data structure
            category = self.get_category_from_treeview(tree)
            item_stats = self.get_item_stats(category, name)
            
            for stat, value in item_stats.items():
                if stat not in ['name', 'weapon_type']:  # Skip name and weapon_type as they're already displayed
                    ttk.Label(self.detail_frame, text=f"{stat.capitalize()}: {value}").pack(anchor="w")
        else:
            self.detail_frame.pack_forget()

        print('Selected')


    def get_category_from_treeview(self, treeview):
        for category in ['Weapons', 'Shields', 'Armors']:
            if treeview in [self.treeview_types[f'{category}_Inventory'], self.treeview_types[f'{category}_Storage']]:
                return category
        return None

    def get_item_stats(self, category, item_name):
        for item in self.storage_data[category] + self.inventory_data[category]:
            if item['name'] == item_name:  # Changed 'Name' to 'name'
                return item
        return {}





    def find_treeview(self, parent):
        for child in parent.winfo_children():
            if isinstance(child, ttk.Treeview):
                return child
        return None

    def update_equipment_stats_treeview(self, action='update'):
        if not self.current_knight:
            print("No knight selected.")
            return

        if action == 'update':
            self.inventory_data['weapons'] = self.current_knight.equipment['weapons']
            self.inventory_data['shields'] = self.current_knight.equipment['shields']
            self.inventory_data['armor'] = self.current_knight.equipment['armor']
            print(self.inventory_data)

        # Update equipment based on action
        if action == 'equip':
            print(action)
            # Logic for equipping item
            pass
        elif action == 'unequip':
            print(action)
            # Logic for unequipping item
            pass

        # Update the treeviews in each tab
        for tab_id in self.notebook_1.tabs():
            tab = self.notebook_1.nametowidget(tab_id)
            category = self.notebook_1.tab(tab_id, "text").lower()

            # Update inventory treeview
            inventory_frame = tab.children['!labelframe']
            inventory_tree = self.find_treeview(inventory_frame)
            if inventory_tree:
                self.populate_treeview(inventory_tree, self.inventory_data[category])

    def equip_item(self):
        if not self.current_knight:
            return
        
        category = self.notebooks.tab(self.notebooks.select(), "text").split(' - ')[0].lower()
        listbox = getattr(self, f'{category}_listbox')
        if not listbox.curselection():
            return
        index = listbox.curselection()[0]
        item = self.storage_data[category][index]
        self.current_knight.add_equipment(item, category)
        print(self.current_knight.equipment)
        self.update_knight_equipment_display()

    def unequip_item(self):
        if not self.current_knight:
            return
        category = self.notebooks.tab(self.notebooks.select(), "text").split(' - ')[0].lower()
        equipped_items = self.current_knight.get_equipment(category)
        if not equipped_items:
            return
        # For simplicity, we'll just unequip the first item
        item = equipped_items[0]
        self.current_knight.remove_equipment(item, category)
        self.update_knight_equipment_display()




    def load_equipment_data(self, category):
        folder_path = os.path.join('equipment', category.lower())
        
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return

        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                item_data = self.load_item_data(os.path.join(folder_path, filename))
                self.storage_data[category].append(item_data)

    def load_item_data(self, file_path):
        with open(file_path, 'r') as f:
            item_data = json.load(f)
        return item_data
#--
    
    def general(self, parent):
        self.generalFrame = ttk.Frame(parent)
        self.currentKnight = ttk.Label(self.generalFrame)
        self.proceedButton = tk.Button(self.generalFrame, text='Proceed to Action', command=self.forwardToAction)

        self.generalFrame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        self.currentKnight.pack(side=tk.LEFT, fill=tk.BOTH)
        self.proceedButton.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.updateGeneral()

    def updateGeneral(self):
        if self.current_knight is None:
            self.currentKnight.config(text='<No Knight Selected>')
            self.proceedButton.config(state=tk.DISABLED)  # Disable the button when no knight is selected
        else:
            self.currentKnight.config(text=self.current_knight.name)  # Use dot notation for accessing 'name'
            self.proceedButton.config(state=tk.NORMAL)  # Enable the button when a knight is selected

    def forwardToAction(self):
        print('You are now on the Action Screen')  # Removed the unused 'current' argument



if __name__ == "__main__":
    root = ThemedTk(theme="winxpblue")
    app = KnightApplication(root)
    root.mainloop() 