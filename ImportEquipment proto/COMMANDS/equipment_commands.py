import os
import json
from abc import ABC, abstractmethod

class Command(ABC):
    """Base command class"""
    
    @abstractmethod
    def execute(self):
        """Execute the command"""
        pass
    
    @abstractmethod
    def undo(self):
        """Undo the command"""
        pass

class CreateEquipmentCommand(Command):
    def __init__(self, equipment_manager, category, name, attributes):
        self.equipment_manager = equipment_manager
        # category is already plural when passed from equipment_manager
        self.category = category
        self.name = name
        self.attributes = attributes
        self.file_path = None

    def execute(self):
        # Create filename from name
        filename = f"{self.name.lower().replace(' ', '_')}.json"
        self.file_path = os.path.join(self.equipment_manager.base_dir, self.category, filename)
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            
            # Create the JSON data
            with open(self.file_path, 'w') as f:
                json.dump(self.attributes, f, indent=2)
            
            # Update equipment manager paths
            self.equipment_manager.refresh_storage_paths()
            return True, f"Equipment created successfully as '{filename}'"
        except Exception as e:
            return False, f"Failed to create equipment: {str(e)}"
    
    def undo(self):
        if self.file_path and os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
                self.equipment_manager.refresh_storage_paths()
                return True, f"Equipment creation of '{self.name}' undone"
            except Exception as e:
                return False, f"Failed to undo equipment creation: {str(e)}"

class ModifyEquipmentCommand(Command):
    def __init__(self, equipment_manager, file_path, new_attributes):
        self.equipment_manager = equipment_manager
        self.file_path = file_path
        self.new_attributes = new_attributes
        self.old_attributes = None
        
    def execute(self):
        try:
            # Backup current data
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    self.old_attributes = json.load(f)
            
            # Write new data
            with open(self.file_path, 'w') as f:
                json.dump(self.new_attributes, f, indent=2)
            
            return True, "Equipment modified successfully"
        except Exception as e:
            return False, f"Failed to modify equipment: {str(e)}"
    
    def undo(self):
        if self.old_attributes:
            try:
                with open(self.file_path, 'w') as f:
                    json.dump(self.old_attributes, f, indent=2)
                return True, "Equipment modification undone"
            except Exception as e:
                return False, f"Failed to undo modification: {str(e)}"
        return False, "No backup data available for undo"

class DeleteEquipmentCommand(Command):
    def __init__(self, equipment_manager, file_path):
        self.equipment_manager = equipment_manager
        self.file_path = file_path
        self.backup_data = None
        self.category = None
        
    def execute(self):
        try:
            # Get the category from the path parts correctly
            path_parts = self.file_path.split(os.sep)  # Split path using OS separator
            self.category = path_parts[-2]  # Category is the parent directory name
            
            # Backup current data if file exists
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    self.backup_data = json.load(f)
                
                # Delete file
                os.remove(self.file_path)
                
                # Update equipment manager paths
                self.equipment_manager.refresh_storage_paths()
                
                return True, "Equipment deleted successfully"
            return False, "File does not exist"
            
        except Exception as e:
            return False, f"Failed to delete equipment: {str(e)}"
 
    def undo(self):
        if self.backup_data and self.category:
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
                
                # Recreate file with backup data
                with open(self.file_path, 'w') as f:
                    json.dump(self.backup_data, f, indent=2)
                
                # Update equipment manager paths
                self.equipment_manager.refresh_storage_paths()
                
                return True, "Equipment deletion undone"
            except Exception as e:
                return False, f"Failed to undo deletion: {str(e)}"
        return False, "No backup data available for undo"