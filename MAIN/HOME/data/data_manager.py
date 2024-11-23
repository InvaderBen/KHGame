# data/data_manager.py
import os
import json
from knight import Knight
from utils.config import KNIGHT_DIRECTORY, STORAGE_DIRECTORY, EQUIPMENT_CATEGORIES
from utils.config import ensure_directory_exists, load_json_file, save_json_file

class DataManager:
    def __init__(self):
        self.knights = {}
        self.next_knight_id = 1
        self.storage = {category: [] for category in EQUIPMENT_CATEGORIES}
        self.load_knights()
        self.load_all_equipment()


    def load_knights(self):
        ensure_directory_exists(KNIGHT_DIRECTORY)
        for filename in os.listdir(KNIGHT_DIRECTORY):
            if filename.endswith('.json'):
                knight_id = int(filename.split('_')[1].split('.')[0])
                self.load_knight_from_file(knight_id)
                self.next_knight_id = max(self.next_knight_id, knight_id + 1)

    def load_knight_from_file(self, knight_id):
        filename = os.path.join(KNIGHT_DIRECTORY, f'knight_{knight_id}.json')
        knight_data = load_json_file(filename)
        if knight_data:
            knight = Knight.from_dict(knight_data)
            self.knights[knight_id] = knight
            return knight
        return None
    
    def save_knight_to_file(self, knight_id, knight):
        ensure_directory_exists(KNIGHT_DIRECTORY)
        filename = os.path.join(KNIGHT_DIRECTORY, f'knight_{knight_id}.json')
        knight_data = knight.to_dict()
        try:
            with open(filename, 'w') as f:
                json.dump(knight_data, f, indent=2)
            print(f"Knight saved successfully to {filename}")
        except Exception as e:
            print(f"Error saving knight to {filename}: {str(e)}")


    def get_knight(self, knight_id):
        return self.knights.get(knight_id)

    def get_knight_id(self, knight):
        for knight_id, k in self.knights.items():
            if k == knight:
                return knight_id
        return None


    def create_new_knight(self):
        new_knight = Knight(f'Knight_{self.next_knight_id}')
        self.knights[self.next_knight_id] = new_knight
        self.save_knight_to_file(self.next_knight_id, new_knight)
        print(f"New knight created with ID: {self.next_knight_id}")
        self.next_knight_id += 1
        return new_knight

    def delete_knight(self, knight_id):
        if knight_id in self.knights:
            del self.knights[knight_id]
            filename = os.path.join(KNIGHT_DIRECTORY, f'knight_{knight_id}.json')
            if os.path.exists(filename):
                os.remove(filename)
            return True
        return False

    def update_knight_name(self, knight_id, new_name):
        if knight_id in self.knights:
            self.knights[knight_id].name = new_name
            self.save_knight_to_file(knight_id, self.knights[knight_id])
            print(f"Knight {knight_id} name updated to {new_name}")

    def save_equipment_data(self, category):
        folder_path = os.path.join(STORAGE_DIRECTORY, category.lower())
        ensure_directory_exists(folder_path)
        
        for item in self.storage[category]:
            filename = f"{item['name'].replace(' ', '_').lower()}.json"
            file_path = os.path.join(folder_path, filename)
            save_json_file(file_path, item)


    def load_all_equipment(self):
        for category in EQUIPMENT_CATEGORIES:
            self.load_equipment_data(category)
            #print(f'Loaded for {category}')

    def load_equipment_data(self, category):
        print(f"Loading equipment data for {category}")
        folder_path = os.path.abspath(os.path.join(STORAGE_DIRECTORY, category.lower()))
        
        print(f"Absolute folder path: {folder_path}")
        ensure_directory_exists(folder_path)

        self.storage[category] = []
        
        try:
            files = os.listdir(folder_path)
            print(f"Files in directory: {files}")
            
            for filename in files:
                if filename.endswith('.json'):
                    file_path = os.path.join(folder_path, filename)
                    print(f"Attempting to load file: {file_path}")
                    
                    try:
                        with open(file_path, 'r') as f:
                            item_data = json.load(f)
                        if item_data:
                            print(f"Loaded data: {item_data}")
                            self.storage[category].append(item_data)
                        else:
                            print(f"No data loaded from file: {file_path}")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {file_path}: {str(e)}")
                    except Exception as e:
                        print(f"Error loading file {file_path}: {str(e)}")
                else:
                    print(f"Skipping non-JSON file: {filename}")
        except PermissionError:
            print(f"Permission denied when accessing directory: {folder_path}")
        except Exception as e:
            print(f"Error listing directory {folder_path}: {str(e)}")
        
        print(f"Loaded {len(self.storage[category])} items for {category}")
        print(f"Storage for {category}: {self.storage[category]}")

    def get_storage_items(self, category):
        return self.storage.get(category, [])

    def get_all_knights(self):
        return list(self.knights.values())


    def update_knight_ability(self, knight_id, ability_type, ability_name, value):
        if knight_id in self.knights:
            knight = self.knights[knight_id]
            if ability_type == 'physical':
                knight.set_physical_stat(ability_name, value)
            elif ability_type == 'personality':
                knight.set_personality_stat(ability_name, value)
            knight.update_sums()
            self.save_knight_to_file(knight_id, knight)
            print(f"Knight {knight_id} ability {ability_name} updated to {value}")

    def update_knight_skill(self, knight_id, skill_name, level):
        if knight_id in self.knights:
            knight = self.knights[knight_id]
            knight.set_skill_level(skill_name, level)
            self.save_knight_to_file(knight_id, knight)
            print(f"Knight {knight_id} skill {skill_name} updated to level {level}")