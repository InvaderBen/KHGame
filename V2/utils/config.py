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
        
def find_base_directory(base_name='KHGame'):
    current_directory = os.getcwd()

    while True:
        # Look for the folder that contains "KHGame" and "V2"
        potential_base = os.path.join(current_directory, base_name, 'V2')
        if os.path.exists(potential_base):
            return potential_base
        else:
            parent_directory = os.path.dirname(current_directory)
            if parent_directory == current_directory:
                # Reached root directory, stop searching
                raise FileNotFoundError(f"{base_name}/V2 not found.")
            current_directory = parent_directory

# Set BASE_DIRECTORY dynamically
BASE_DIRECTORY = find_base_directory()
print("Base Directory:", BASE_DIRECTORY)

# Now build the full paths
KNIGHT_DIRECTORY = os.path.join(BASE_DIRECTORY, 'data', 'knights')
STORAGE_DIRECTORY = os.path.join(BASE_DIRECTORY, 'data', 'storage')

print("Knights Directory:", KNIGHT_DIRECTORY)
print("Storage Directory:", STORAGE_DIRECTORY)

SKILL_NAMES = ['Covering', 'Armor', 'Offense', 'Ranged', 'Riding', 'Shield', 'Unarmed', 'Weapon']
PHYSICAL_ABILITIES = ['Strength', 'Endurance', 'Massive', 'Resistance', 'Reflex', 'Dexterity', 'Perception', 'Coordination']
PERSONALITY_TRAITS = ['Intelligence', 'Willpower', 'Emotion', 'Creativity', 'Brave', 'Charisma']
EQUIPMENT_CATEGORIES = ['Weapons', 'Shields', 'Armors']