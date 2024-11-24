import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from COMMANDS.command_manager import CommandManager
from COMMANDS.equipment_commands import CreateEquipmentCommand, ModifyEquipmentCommand, DeleteEquipmentCommand

class EquipmentManager:
    def __init__(self):
        # Get the directory where the script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        
        # Define base directory and categories
        self.base_dir = os.path.join(parent_dir, 'equipment', 'storage')
        self.categories = ['weapons', 'armors', 'shields']
        
        # Initialize storage paths
        self.storage_paths = {
            'weapons': self.get_equipment_list('weapons'),
            'armors': self.get_equipment_list('armors'),
            'shields': self.get_equipment_list('shields')
        }
        
        self.command_manager = CommandManager()

    def get_equipment_list(self, category):
            """Get list of equipment files for a category"""
            if category in self.categories:
                category_path = os.path.join(self.base_dir, category)
                if os.path.exists(category_path):
                    # Get actual files from directory
                    files = [f for f in os.listdir(category_path) if f.endswith('.json')]
                    return [os.path.join(self.base_dir, category, f) for f in files]
            return []

    def get_equipment_name(self, file_path):
        """Convert file path to display name"""
        return os.path.splitext(os.path.basename(file_path))[0].replace('_', ' ').title()

    def get_equipment_name(self, file_path):
        """Convert file path to display name"""
        return os.path.splitext(os.path.basename(file_path))[0].replace('_', ' ').title()

    def load_equipment_data(self, file_path):
            """Load and parse JSON data from file"""
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    # Ensure all expected fields exist with at least None value
                    expected_fields = [
                        'type', 'name', 'perks', 'strike', 'prot', 
                        'defense', 'speed', 'evade', 'block', 
                        'damage', 'critical_condition', 'total_damage'
                    ]
                    for field in expected_fields:
                        if field not in data:
                            data[field] = None
                    return data
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading {file_path}: {str(e)}")  # Debug print
                return {
                    "error": f"Could not load file: {str(e)}",
                    "type": None, "name": None, "perks": None,
                    "strike": None, "prot": None, "defense": None,
                    "speed": None, "evade": None, "block": None,
                    "damage": None, "critical_condition": None,
                    "total_damage": None
                }

    def get_categories(self):
        """Get list of available equipment categories"""
        return self.categories

    def create_equipment(self, category, name, attributes):
        """Create new equipment using command pattern"""
        if category not in self.categories:
            return False, f"Invalid category. Available categories: {', '.join(self.categories)}"
        
        command = CreateEquipmentCommand(self, category, name, attributes)
        return self.command_manager.execute_command(command)

    def modify_equipment(self, file_path, new_attributes):
        """Modify existing equipment using command pattern"""
        command = ModifyEquipmentCommand(self, file_path, new_attributes)
        return self.command_manager.execute_command(command)

    def delete_equipment(self, file_path):
        """Delete equipment using command pattern"""
        command = DeleteEquipmentCommand(self, file_path)
        return self.command_manager.execute_command(command)

    def undo_last_action(self):
        """Undo last command"""
        return self.command_manager.undo_last_command()

    def redo_last_action(self):
        """Redo last undone command"""
        return self.command_manager.redo_last_command()

    def refresh_storage_paths(self):
            """Refresh all storage paths"""
            for category in self.categories:
                category_path = os.path.join(self.base_dir, category)
                if os.path.exists(category_path):
                    files = [f for f in os.listdir(category_path) if f.endswith('.json')]
                    self.storage_paths[category] = [os.path.join(self.base_dir, category, f) for f in files]
                else:
                    self.storage_paths[category] = []

    def debug_paths(self):
        """Print debug information about paths"""
        print(f"Base Directory: {self.base_dir}")
        print("\nStorage Paths:")
        for category, paths in self.storage_paths.items():
            print(f"\n{category.upper()}:")
            if paths:
                for path in paths:
                    print(f"  {path}")
                    if os.path.exists(path):
                        print("    (File exists)")
                    else:
                        print("    (File not found)")
            else:
                print("  No files found")