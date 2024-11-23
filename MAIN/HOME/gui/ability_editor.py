import tkinter as tk
from tkinter import ttk
from utils.config import PHYSICAL_ABILITIES, PERSONALITY_TRAITS

class AbilityEditor(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_knight = None
        self.create_widgets()

    def create_widgets(self):
        self.create_ability_editors()
        self.create_apply_button()

    def create_ability_editors(self):
        # Physical Abilities Frame
        phys_frame = ttk.LabelFrame(self, text="Physical Abilities")
        phys_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Personality Traits Frame
        pers_frame = ttk.LabelFrame(self, text="Personality Traits")
        pers_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create spinboxes for Physical Abilities
        self.phys_spinboxes = {}
        for i, ability in enumerate(PHYSICAL_ABILITIES):
            label = ttk.Label(phys_frame, text=ability)
            label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            spinbox = ttk.Spinbox(phys_frame, from_=1, to=6, width=5, command=self.update_points, state='disabled')
            spinbox.grid(row=i, column=1, padx=5, pady=2)
            self.phys_spinboxes[ability.lower()] = spinbox

        # Create spinboxes for Personality Traits
        self.pers_spinboxes = {}
        for i, trait in enumerate(PERSONALITY_TRAITS):
            label = ttk.Label(pers_frame, text=trait)
            label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            spinbox = ttk.Spinbox(pers_frame, from_=1, to=6, width=5, command=self.update_points, state='disabled')
            spinbox.grid(row=i, column=1, padx=5, pady=2)
            self.pers_spinboxes[trait.lower()] = spinbox

        # Create labels for points
        self.phys_points_label = ttk.Label(phys_frame, text="Physical Points: --")
        self.phys_points_label.grid(row=len(PHYSICAL_ABILITIES), column=0, columnspan=2, pady=10)

        self.pers_points_label = ttk.Label(pers_frame, text="Personality Points: --")
        self.pers_points_label.grid(row=len(PERSONALITY_TRAITS), column=0, columnspan=2, pady=10)

    def create_apply_button(self):
        self.apply_button = ttk.Button(self, text="Apply Changes", command=self.apply_changes)
        self.apply_button.pack(pady=10)

    def load_knight(self, knight):
        self.current_knight = knight
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
        self.current_knight.update_sums()

        phys_points = 30 - phys_sum
        pers_points = 20 - pers_sum

        self.phys_points_label.config(text=f"Physical Points: {phys_points}")
        self.pers_points_label.config(text=f"Personality Points: {pers_points}")

        # Lock/unlock spinboxes based on points
        self.lock_unlock_spinboxes(self.phys_spinboxes, phys_points)
        self.lock_unlock_spinboxes(self.pers_spinboxes, pers_points)

        # Update the knight's data in the file
        knight_id = self.data_manager.get_knight_id(self.current_knight)
        self.data_manager.save_knight_to_file(knight_id, self.current_knight)

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

    def apply_changes(self):
        if not self.current_knight:
            return

        for ability, spinbox in self.phys_spinboxes.items():
            self.current_knight.set_physical_stat(ability, int(spinbox.get()))

        for trait, spinbox in self.pers_spinboxes.items():
            self.current_knight.set_personality_stat(trait, int(spinbox.get()))

        self.current_knight.update_sums()

        # Update the knight's data in the file
        knight_id = self.data_manager.get_knight_id(self.current_knight)
        self.data_manager.save_knight_to_file(knight_id, self.current_knight)

        # Notify AllStatistics to update
        self.event_generate("<<StatsUpdated>>")