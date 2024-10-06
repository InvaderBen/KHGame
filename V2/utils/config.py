import os
import json

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def save_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# utils/config.py
KNIGHT_DIRECTORY = 'data/knights'
STORAGE_DIRECTORY = 'data/storage'
SKILL_NAMES = ['Covering', 'Armor', 'Offense', 'Ranged', 'Riding', 'Shield', 'Unarmed', 'Weapon']
PHYSICAL_ABILITIES = ['Strength', 'Endurance', 'Massive', 'Resistance', 'Reflex', 'Dexterity', 'Perception', 'Coordination']
PERSONALITY_TRAITS = ['Intelligence', 'Willpower', 'Emotion', 'Creativity', 'Brave', 'Charisma']
EQUIPMENT_CATEGORIES = ['Weapons', 'Shields', 'Armors']