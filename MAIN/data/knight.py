import random

class Skill:
    def __init__(self, name, progression, current_level=1):
        self.name = name
        self.progression = progression
        self.current_level = current_level

    def get_value(self, level):
        if 1 <= level <= len(self.progression):
            return self.progression[level - 1]
        else:
            raise ValueError("Level out of range")

    def to_dict(self):
        return {
            'name': self.name,
            'progression': self.progression,
            'current_level': self.current_level
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['progression'], data['current_level'])

class Knight:
    def __init__(self, name, age=18, stance_skill=1):
        self.name = name
        self.age = age
        self.stance_skill = stance_skill
        self.preferred_hand = 'right' if random.random() < 0.85 else 'left'
        self.artwork = self._select_random_artwork()

        self.skillPoints = (self.age - 20) * 36 + 192
        self.persPoints = 20
        self.physPoints = 30

        # Physical abilities
        self.strength = 1
        self.endurance = 1
        self.massive = 1
        self.resistance = 1
        self.reflex = 1
        self.dexterity = 1
        self.perception = 1
        self.coordination = 1

        # Personality abilities
        self.intelligence = 1
        self.willpower = 1
        self.emotion = 1
        self.creativity = 1
        self.brave = 1
        self.charisma = 1

        # Core abilities
        self.focus = 1
        self.communication = 1
        
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

        self.equipped = {
            'head': None,
            'torso': None,
            'hand_left': None,
            'hand_right': None
        }


    def _select_random_artwork(self):
        artworks = [
            "KH_Py\\KHGame\\ART\\crusader_A.sprite.attack_scroll.png",
            "KH_Py\\KHGame\\ART\\crusader_B.sprite.attack_scroll.png",
            "KH_Py\\KHGame\\ART\\crusader_C.sprite.attack_scroll.png",
            "KH_Py\\KHGame\\ART\\crusader_D.sprite.attack_scroll.png"
        ]
        return random.choice(artworks)

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
            'skills': {skill_name: (skill.current_level, skill.get_value(skill.current_level)) 
                       for skill_name, skill in self.skills.items()},
            'core_stats': self.calculate_core_stats(),
        }

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

    def calculate_combat_stats(self):
        weapon_skill = self.get_skill_level('Weapon')
        armor_skill = self.get_skill_level('Armor')
        covering_skill = self.get_skill_level('Covering')
        offense_skill = self.get_skill_level('Offense')
        unarmed_skill = self.get_skill_level('Unarmed')
        ranged_skill = self.get_skill_level('Ranged')
        riding_skill = self.get_skill_level('Riding')

        return {
            'Combat Damage.': self.calculate_core_stats()['Damage'] + weapon_skill,
            'Combat HP': self.calculate_core_stats()['Hp'],
            'Combat Strike.': self.calculate_core_stats()['Strike'] + offense_skill,
            'Combat Block': self.calculate_core_stats()['Block'] + covering_skill,
            'Combat Evade': self.calculate_core_stats()['Evade'] + unarmed_skill,
            'Combat Mood': self.calculate_core_stats()['Mood'],
            'Combat Defense': 75 + self.calculate_core_stats()['Defense'] + covering_skill,
            'Combat ACC.': self.calculate_core_stats()['Accuracy'] + ranged_skill,
            'Combat Protection': self.calculate_core_stats()['Protection'] + armor_skill,
            'Combat Speed': self.calculate_core_stats()['Speed'] + riding_skill,
            'Combat Hardness': self.calculate_core_stats()['Hardness'],
            'Combat Balance': self.calculate_core_stats()['Balance']
        }
    

        """"COM.DAM.: CORE DAM + WEP SKILL + WEP DAM
            HP: END + RES + WILL
            COM STR.: CORE STR + OFF SKILL + WEP STRIKE
            COM BLOCK: CORE BLOCK + WEP BLOCK + COVER SKILL
            COM EVADE: CORE EVADE + UNARMED SKILL
            COM MOOD: EMOTION + BRAVE + COMPOSURE
            COM DEF.: 75 + CORE DEF + COVERING SKILL + WEAPON DEF
            COM ACC.: CORE ACC + RANGED SKILL
            COM PROT.: CORE PROT + ARMOR SKILL + WEP PROT
            COM SPEED: CORE SPEED + RIDING SKILL + WEAPON SKILL
            COM HARDNESS: CORE HARDNESS
            COM BALANCE: CORE BALANCE"""


    def get_available_stances(self, stances):
        return [stance for stance in stances if stance['level'] <= self.stance_skill]

    def get_skill_level(self, skill_name):
        if skill_name in self.skills:
            return self.skills[skill_name].current_level
        else:
            raise ValueError(f"Skill '{skill_name}' does not exist.")

    def set_skill_level(self, skill_name, level):
        if skill_name in self.skills:
            if 1 <= level <= 10:
                old_level = self.skills[skill_name].current_level
                self.skills[skill_name].current_level = level
                cost = sum(self.skills[skill_name].progression[old_level-1:level-1])
                self.skillPoints -= cost
                return self.skills[skill_name].get_value(level)
            else:
                raise ValueError("Skill level must be between 1 and 10.")
        else:
            raise ValueError(f"Skill '{skill_name}' does not exist.")
        
    def set_physical_stat(self, stat_name, value):
        if hasattr(self, stat_name):
            old_value = getattr(self, stat_name)
            setattr(self, stat_name, value)
            self.physPoints -= (value - old_value)
            self.update_sums()

    def set_personality_stat(self, stat_name, value):
        if hasattr(self, stat_name):
            old_value = getattr(self, stat_name)
            setattr(self, stat_name, value)
            self.persPoints -= (value - old_value)
            self.update_sums()

    def add_equipment(self, item, category):
        if category in self.equipment:
            self.equipment[category].append(item)

    def remove_equipment(self, item, category):
        if category in self.equipment and item in self.equipment[category]:
            self.equipment[category].remove(item)

    def get_equipment(self, category):
        return self.equipment.get(category, [])

    def equip_item(self, item, slot):
        if slot in self.equipped:
            self.equipped[slot] = item

    def unequip_item(self, slot):
        if slot in self.equipped:
            item = self.equipped[slot]
            self.equipped[slot] = None
            return item
        return None

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'stance_skill': self.stance_skill,
            'artwork': self.artwork,
            'preferred_hand': self.preferred_hand,  # Include preferred_hand in the save data
            'skillPoints': self.skillPoints,
            'persPoints': self.persPoints,
            'physPoints': self.physPoints,
            'physical_abilities': {
                'strength': self.strength,
                'endurance': self.endurance,
                'massive': self.massive,
                'resistance': self.resistance,
                'reflex': self.reflex,
                'dexterity': self.dexterity,
                'perception': self.perception,
                'coordination': self.coordination
            },
            'personality_abilities': {
                'intelligence': self.intelligence,
                'willpower': self.willpower,
                'emotion': self.emotion,
                'creativity': self.creativity,
                'brave': self.brave,
                'charisma': self.charisma
            },
            'core_abilities': {
                'focus': self.focus,
                'communication': self.communication
            },
            'skills': {name: skill.to_dict() for name, skill in self.skills.items()},
            'equipment': self.equipment,
            'equipped': self.equipped
        }

    @classmethod
    def from_dict(cls, data):
        knight = cls(data['name'], data['age'], data.get('stance_skill', 1))
        
        # Load artwork if present
        if 'artwork' in data:
            knight.artwork = data['artwork']
            
        # Load preferred_hand or generate new one if not present
        if 'preferred_hand' in data:
            knight.preferred_hand = data['preferred_hand']
        else:
            # 85% chance of being right-handed for backward compatibility
            knight.preferred_hand = 'right' if random.random() < 0.85 else 'left'

        knight.skillPoints = data['skillPoints']
        knight.persPoints = data['persPoints']
        knight.physPoints = data['physPoints']
        
        for ability, value in data['physical_abilities'].items():
            setattr(knight, ability, value)
        
        for ability, value in data['personality_abilities'].items():
            setattr(knight, ability, value)
        
        for ability, value in data['core_abilities'].items():
            setattr(knight, ability, value)
        
        knight.skills = {name: Skill.from_dict(skill_data) for name, skill_data in data['skills'].items()}
        knight.equipment = data['equipment']
        knight.equipped = data['equipped']
        
        knight.update_sums()
        return knight