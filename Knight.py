class Skill:
    def __init__(self, name, progression):
        self.name = name
        self.progression = progression
        self.current_level = 1  # Initialize with level 1

    def get_value(self, level):
        if 1 <= level <= len(self.progression):
            return self.progression[level - 1]
        else:
            raise ValueError("Level out of range")

    def __str__(self):
        return f"{self.name} Skill: Progression = {self.progression}, Current Level = {self.current_level}"
    
class Knight:
    def __init__(self, name):
        self.name = name
        self.age = 18
        self.skillPoints = (self.age - 20) * 36 + 192
        self.persPoints = 20  # Changed from perPoints to persPoints
        self.physPoints = 30  # Changed from phyPoints to physPoints

        # Physical abilities
        self.strength = 1    # STR
        self.endurance = 1   # END
        self.massive = 1     # MAS
        self.resistance = 1  # RES
        self.reflex = 1      # REF
        self.dexterity = 1   # DEX
        self.perception = 1  # PER
        self.coordination = 1  # COO
        self.phySum = self.strength + self.endurance + self.massive + self.resistance + self.reflex + self.dexterity + self.perception + self.coordination
        # Personality abilities
        self.intelligence = 1  # INT
        self.willpower = 1   # WIL
        self.emotion = 1     # EMO
        self.creativity = 1  # CRE
        self.brave = 1       # BRA
        self.charisma = 1    # CHA
        self.perSum = self.intelligence + self.willpower + self.emotion + self.creativity + self.brave + self.charisma

        # Core abilities
        self.focus = 1       # FOC
        self.communication = 1  # COM
        
        self.update_sums()

        # Skills
        self.skills = {
            'Covering': Skill('Covering', [5, 10, 15, 20, 25, 30, 35, 40, 50, 125]),
            'Armor': Skill('Armor', [1, 2, 3, 4, 6, 8, 10, 11, 12, 20]),
            'Offense': Skill('Offense', [2, 5, 10, 10, 20, 20, 30, 30, 40, 75]),
            'Ranged': Skill('Ranged', [2, 5, 12, 15, 20, 25, 30, 35, 40, 55]),
            'Riding': Skill('Riding', [1, 2, 2, 3, 3, 4, 4, 4, 4, 5]),
            'Shield': Skill('Shield', [10, 15, 20, 25, 30, 35, 40, 45, 50, 75]),
            'Unarmed': Skill('Unarmed', [2, 5, 10, 10, 20, 20, 30, 30, 40, 50]),
            'Weapon': Skill('Weapon', [1, 3, 6, 8, 10, 12, 15, 18, 24, 36])
        }

        self.equipment = {
            'weapons': [],
            'shields': [],
            'armor': []
        }

    def update_sums(self):
        self.physSum = (self.strength + self.endurance + self.massive + self.resistance + 
                        self.reflex + self.dexterity + self.perception + self.coordination)
        self.persSum = (self.intelligence + self.willpower + self.emotion + self.creativity + 
                        self.brave + self.charisma)

    def get_stats(self):
        return {
            'abilities_physical': {
                'Strength': self.strength,
                'Endurance': self.endurance,
                'Massive': self.massive,
                'Resistance': self.resistance,
                'Reflex': self.reflex,
                'Dexterity': self.dexterity,
                'Perception': self.perception,
                'Coordination': self.coordination,
                'Sum': self.physSum
            },
            'abilities_personality': {
                'Intelligence': self.intelligence,
                'Willpower': self.willpower,
                'Emotion': self.emotion,
                'Creativity': self.creativity,
                'Brave': self.brave,
                'Charisma': self.charisma,
                'Sum': self.persSum
            },
            'skills':{
                'Covering': self.skills["Covering"],
                'Armor': self.skills["Armor"],
                'Offense': self.skills["Offense"],
                'Ranged': self.skills["Ranged"],
                'Riding': self.skills["Riding"],
                'Shield': self.skills["Shield"],
                'Unarmed': self.skills["Unarmed"],
                'Weapon': self.skills["Weapon"]
            },
            'core_stats': self.calculate_core_stats(),
            'skills': {skill_name: (skill.current_level, skill.get_value(skill.current_level)) 
                   for skill_name, skill in self.skills.items()},
            
        }

    def set_physical_stat(self, stat_name, value):
        if hasattr(self, stat_name):
            setattr(self, stat_name, value)

    def set_personality_stat(self, stat_name, value):
        if hasattr(self, stat_name):
            setattr(self, stat_name, value)

    def calculate_core_stats(self):
        return {
            'Speed': self.reflex + self.dexterity + self.coordination,
            'Hp': self.endurance + self.resistance + self.willpower,
            'Strike': self.strength + self.coordination + self.endurance,
            'Damage': self.strength + self.massive + self.brave,
            'Mood': self.emotion + self.brave + self.communication,
            'Hardness': self.resistance + self.willpower + self.endurance,
            'Evade': self.reflex + self.creativity + self.perception,
            'Balance': self.dexterity + self.coordination + self.reflex,
            'Block': self.strength + self.communication + self.perception,
            'Defense': self.strength + self.coordination + self.intelligence,
            'Accuracy': self.dexterity + self.perception + self.focus,
            'Protection': self.resistance + self.massive + self.focus,
            'Gallantry': self.brave + self.willpower + self.emotion,
            'Charming': self.charisma + self.intelligence + self.emotion,
            'Motivation': self.creativity + self.charisma + self.focus,
            'Command': self.intelligence + self.focus + self.reflex,
            'Fortitude': self.communication + self.willpower + self.resistance,
            'Insight': self.perception + self.intelligence + self.creativity
        }

    def get_skill_level(self, skill_name):
        if skill_name in self.skills:
            return self.skills[skill_name].current_level
        else:
            raise ValueError(f"Skill '{skill_name}' does not exist.")

    def set_skill_level(self, skill_name, level):

        if skill_name in self.skills:
            if 1 <= level <= 10:
                self.skills[skill_name].current_level = level
                return self.skills[skill_name].get_value(level)
            else:
                raise ValueError("Skill level must be between 1 and 10.")
        else:
            raise ValueError(f"Skill '{skill_name}' does not exist.")
        
    def set_physical_stat(self, stat_name, value):
        if hasattr(self, stat_name):
            setattr(self, stat_name, value)
            self.update_sums()

    def set_personality_stat(self, stat_name, value):
        if hasattr(self, stat_name):
            setattr(self, stat_name, value)
            self.update_sums()

    def add_equipment(self, item, category):
        if category in self.equipment:
            self.equipment[category].append(item)

    def remove_equipment(self, item, category):
        if category in self.equipment and item in self.equipment[category]:
            self.equipment[category].remove(item)

    def get_equipment(self, category):
        return self.equipment.get(category, [])