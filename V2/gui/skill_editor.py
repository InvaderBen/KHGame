import tkinter as tk
from tkinter import ttk

class SkillEditor(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_knight = None
        self.create_widgets()

    def create_widgets(self):
        self.skill_frame = ttk.LabelFrame(self, text="Combat Skills")
        self.skill_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.skill_spinboxes = {}
        self.skill_progression_labels = {}

        skill_names = ['Covering', 'Armor', 'Offense', 'Ranged', 'Riding', 'Shield', 'Unarmed', 'Weapon']

        for i, skill_name in enumerate(skill_names):
            label = ttk.Label(self.skill_frame, text=skill_name)
            label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            
            spinbox = ttk.Spinbox(self.skill_frame, from_=1, to=10, width=5,
                                  command=lambda name=skill_name: self.update_skill(name))
            spinbox.grid(row=i, column=1, padx=5, pady=2)
            self.skill_spinboxes[skill_name] = spinbox

            progression_label = ttk.Label(self.skill_frame, text="")
            progression_label.grid(row=i, column=2, padx=5, pady=2)
            self.skill_progression_labels[skill_name] = progression_label

        self.skill_points_label = ttk.Label(self.skill_frame, text="Remaining Skill Points: --")
        self.skill_points_label.grid(row=len(skill_names), column=0, columnspan=3, pady=10)

    def load_knight(self, knight):
        self.current_knight = knight
        self.update_display()

    def update_display(self):
        if not self.current_knight:
            return

        skills = self.current_knight.get_stats()['skills']
        
        for skill_name, spinbox in self.skill_spinboxes.items():
            spinbox.set(skills[skill_name][0])  # Set to current level

        self.update_skill_progression_labels()
        self.update_skill_points_display()

    def update_skill(self, skill_name):
        if not self.current_knight:
            return

        new_level = int(self.skill_spinboxes[skill_name].get())
        self.current_knight.set_skill_level(skill_name, new_level)
        
        self.update_skill_progression_labels()
        self.update_skill_points_display()

        # Save the updated knight data
        knight_id = self.data_manager.get_knight_id(self.current_knight)
        self.data_manager.save_knight_to_file(knight_id, self.current_knight)

    def update_skill_progression_labels(self):
        skills = self.current_knight.get_stats()['skills']
        for skill_name, label in self.skill_progression_labels.items():
            current_level, current_value = skills[skill_name]
            next_cost = self.current_knight.skills[skill_name].progression[current_level-1] if current_level < 10 else "Max"
            label.config(text=f"Current: {current_value}, Next Cost: {next_cost}")

    def update_skill_points_display(self):
        self.skill_points_label.config(text=f"Remaining Skill Points: {self.current_knight.skillPoints}")
