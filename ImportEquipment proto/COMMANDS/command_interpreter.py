from .error_handler import CommandError, command_error_handler
import json
import os
import re

class CommandInterpreter:
    def __init__(self, equipment_manager):
        self.equipment_manager = equipment_manager
        self.current_command = None
        # Command-specific help messages
        self.command_help = {

            'show': """
Show Command Usage:
------------------
show <option> [arguments]

Options:
  all                     - Show all equipment across all categories
  category <category>     - Show all equipment in specified category
  <name>                 - Show specific equipment details

Examples:
  show all               - Displays all equipment
  show category weapons  - Shows all weapons
  show sword            - Shows details for sword
  
Available categories: weapons, armors, shields""",

            'create': """
Create Command Usage:
-------------------
create <category> <name> <attributes>

Arguments:
  category   - Equipment category (weapons/armors/shields)
  name       - Name of the equipment
  attributes - JSON format attributes

Example:
  create weapon sword {"damage": 10, "weight": 5}""",

            'modify': """
Modify Command Usage:
-------------------
modify <name> <attributes>

Arguments:
  name       - Name of equipment to modify
  attributes - New JSON format attributes

Example:
  modify sword {"damage": 15, "weight": 5}""",

            'delete': """
Delete Command Usage:
-------------------
delete <name>

Arguments:
  name - Name of equipment to delete

Example:
  delete sword"""
        }
    
        self.valid_attributes = {
            'type': str,
            'name': str,
            'perks': list,
            'strike': int,
            'prot': int,
            'defense': int,
            'speed': int,
            'evade': int,
            'block': int,
            'damage': int,
            'critical_condition': int,
            'total_damage': int
        }

        self.commands = {
            'help': self.show_help,
            'create': self.create_equipment,
            'modify': self.modify_equipment,
            'delete': self.delete_equipment,
            'show': self.show_equipment,
            'undo': self.equipment_manager.undo_last_action,
            'redo': self.equipment_manager.redo_last_action,
            'cls': self.clear_screen,
            'refresh': self.refresh
        }

        self.equipment_types = {
            'weapon': 'weapons',
            'armor': 'armors',
            'shield': 'shields'
        }

        # Define help messages for each command
        self.command_help['create'] = """
Create Command Usage:
------------------
create <type>

Type must be one of:
  weapon  - Create a new weapon
  armor   - Create a new armor
  shield  - Create a new shield

The command will automatically assign an ID if name is not provided.
Created items will have all attributes set to null.

Examples:
  create weapon    - Creates weapon_001 (or next available ID)
  create shield    - Creates shield_001 (or next available ID)
"""
        self.command_help['modify'] = """
Modify Command Usage:
------------------
modify '<item_name>' <attribute> <value>

Examples:
  modify 'Iron Sword' name 'Flaming Sword'   # Both item name and new name need quotes
  modify 'Magic Staff' damage 50             # Numbers don't need quotes
  modify 'Battle Axe' perks append 'Fire Damage'   # String values always need quotes
  modify 'War Hammer' perks remove 'Stun Effect'
  modify 'Steel Bow' perks clear

Notes:
- String values ALWAYS need single quotes:
  * Item names: 'Iron Sword', 'Battle Axe'
  * Name attribute: modify 'weapon_001' name 'Excalibur'
  * Type attribute: modify 'weapon_001' type 'sword'
  * Perk values: modify 'weapon_001' perks append 'Fire Damage'

- Number values NEVER need quotes:
  * damage, strike, defense, speed, etc.
  * Example: modify 'Iron Sword' damage 50

Available attributes:
  * type               - string (requires quotes)
  * name               - string (requires quotes)
  * perks              - list (values require quotes)
  * strike             - integer
  * prot              - integer
  * defense           - integer
  * speed             - integer
  * evade             - integer
  * block             - integer
  * damage            - integer
  * critical_condition - integer
  * total_damage      - integer
"""
        self.command_help['create'] = """
Create Command Usage:
------------------
create <type>

Type must be one of:
  weapon  - Create a new weapon
  armor   - Create a new armor
  shield  - Create a new shield

Examples:
  create weapon    - Creates 'weapon_001' (or next available ID)
  create shield    - Creates 'shield_001' (or next available ID)

Notes:
- Creates equipment with all attributes set to null
- Use modify command to set values
- The created item will have an ID-based name that you can later modify
- To rename: modify 'weapon_001' name 'Excalibur'
"""
        self.command_help['show'] = """
Show Command Usage:
----------------
show <option> [arguments]

Options:
  all                     - Show all equipment
  category <category>     - Show all equipment in category
  <name>                 - Show specific equipment

Examples:
  show all
  show category weapons
  show 'weapon_001'
"""
        self.command_help['delete'] = """
Delete Command Usage:
------------------
delete <'item_name'>

Example:
  delete 'weapon_001'
"""
        self.command_help['cls'] = """
Clear Screen Command Usage:
------------------------
cls

Clears the command prompt output.
"""
        self.command_help['refresh'] = """
Refresh Command Usage:
-------------------
refresh [category]

Arguments:
  category - Optional. Specific category to refresh (weapons/armors/shields)
            If not provided, refreshes all categories.

Examples:
  refresh          - Refresh all categories
  refresh weapons  - Refresh only weapons
"""


    @command_error_handler
    def execute(self, command_text):
        """Parse and execute a command"""
        self.current_command = command_text  # Store current command
        
        parts = command_text.strip().split()
        if not parts:
            raise CommandError("Empty command")
        
        command = parts[0].lower()
        args = parts[1:]
        
        if command not in self.commands:
            raise CommandError(
                f"Unknown command '{command}'",
                command=command_text,
                function="execute"
            )
        
        return self.commands[command](*args)

        # Add help for cls
        self.command_help['cls'] = """
Clear Screen Command Usage:
------------------------
cls

Clears the command prompt output.
"""
    
        # Add help for cls
        self.command_help['cls'] = """
Clear Screen Command Usage:
------------------------
cls

Clears the command prompt output.
"""
    
    def clear_screen(self, *args):
        """Clear command prompt screen"""
        return "\x1bCLEAR"

    def refresh(self, *args):
        """Refresh equipment lists"""
        if args:
            category = args[0].lower()
            if category not in self.equipment_manager.categories:
                return f"Error: Invalid category '{category}'. Available categories: {', '.join(self.equipment_manager.categories)}"
            self.equipment_manager.refresh_storage_paths()
            return f"Refreshed {category} list"
        else:
            self.equipment_manager.refresh_storage_paths()
            return "Refreshed all equipment lists"


    @command_error_handler
    def modify_equipment(self, *args):
        """Modify equipment attributes"""
        self.current_command = f"modify {' '.join(args)}"
        
        if not args:
            raise CommandError(
                "Missing arguments",
                command="modify",
                function="modify_equipment"
            )
        
        # Check if item name is properly quoted
        if not (args[0].startswith("'") and args[0].endswith("'")):
            raise CommandError(
                "Item name must be enclosed in single quotes",
                command=self.current_command,
                function="modify_equipment",
                args=args
            )
        
        item_name = args[0][1:-1]  # Remove quotes
        
        if len(args) < 3:
            raise CommandError(
                "Missing attribute and value",
                command=self.current_command,
                function="modify_equipment",
                args=args
            )
        
        attr_name = args[1].lower()
        
        # Validate attribute exists
        if attr_name not in self.valid_attributes:
            raise CommandError(
                f"Invalid attribute '{attr_name}'",
                command=self.current_command,
                function="modify_equipment",
                args=args
            )
        
        # ... (rest of modify_equipment with similar error handling)

        @command_error_handler
        def create_equipment(self, *args):
            """Create new equipment with null values for all attributes"""
            self.current_command = f"create {' '.join(args)}"
            
            if not args:
                raise CommandError(
                    "Equipment type required",
                    command="create",
                    function="create_equipment"
                )
                
            if args[0] == 'help':
                return self.command_help['create']
                
            equip_type = args[0].lower()
            
            # Check if type is valid (use singular form)
            if equip_type not in self.equipment_types:
                raise CommandError(
                    f"Invalid equipment type '{equip_type}'. Must be weapon, armor, or shield",
                    command=self.current_command,
                    function="create_equipment",
                    args=args
                )
            
            # Get name if provided, otherwise generate one
            equip_name = None
            if len(args) > 1:
                equip_name = " ".join(args[1:])
            else:
                # Get next available ID using the singular form
                equip_name = self.generate_equipment_id(equip_type)
            
            # Create blank equipment with null values
            blank_equipment = {
                "type": equip_type,
                "name": None,
                "perks": None,
                "strike": None,
                "prot": None,
                "defense": None,
                "speed": None,
                "evade": None,
                "block": None,
                "damage": None,
                "critical_condition": None,
                "total_damage": None
            }
            
            # Use plural form for storage
            category = self.equipment_types[equip_type]
            success, msg = self.equipment_manager.create_equipment(category, equip_name, blank_equipment)
            
            if success:
                return f"Created blank {equip_type} with name '{equip_name}'. Use modify command to set attributes."
            return msg



    def execute(self, command_text):
        """Parse and execute a command"""
        try:
            parts = command_text.strip().split()
            if not parts:
                return "Error: Empty command"
            
            command = parts[0].lower()
            args = parts[1:]
            
            # Check for command-specific help
            if len(args) > 0 and args[-1].lower() == 'help':
                if command in self.command_help:
                    return self.command_help[command]
                return f"No specific help available for '{command}'"
            
            if command in self.commands:
                return self.commands[command](*args)
            else:
                return f"Error: Unknown command '{command}'. Type 'help' for available commands."
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def show_help(self, *args):
        if args and args[0] in self.command_help:
            return self.command_help[args[0]]
            
        return """Available commands:
help [command]   - Show this help message or command-specific help
create          - Create new equipment
modify          - Modify existing equipment
delete          - Delete equipment
show            - Show equipment details
undo            - Undo last action
redo            - Redo last action

For detailed help on a command, type:
1. <command> help    (e.g., 'show help')
2. help <command>    (e.g., 'help show')"""


    @command_error_handler
    def create_equipment(self, *args):
        """Create new equipment with null values for all attributes"""
        self.current_command = f"create {' '.join(args)}"
        
        if not args:
            raise CommandError(
                "Equipment type required",
                command="create",
                function="create_equipment"
            )
            
        if args[0] == 'help':
            return self.command_help['create']
            
        equip_type = args[0].lower()
        
        # Check if type is valid (use singular form)
        if equip_type not in self.equipment_types:
            raise CommandError(
                f"Invalid equipment type '{equip_type}'. Must be weapon, armor, or shield",
                command=self.current_command,
                function="create_equipment",
                args=args
            )
        
        # Get plural form for storage
        category = self.equipment_types[equip_type]
        
        # Get name if provided, otherwise generate one
        equip_name = None
        if len(args) > 1:
            equip_name = " ".join(args[1:])
        else:
            # Get next available ID using the singular form
            equip_name = self.generate_equipment_id(equip_type)
        
        # Create blank equipment with null values
        blank_equipment = {
            "type": equip_type,
            "name": None,
            "perks": None,
            "strike": None,
            "prot": None,
            "defense": None,
            "speed": None,
            "evade": None,
            "block": None,
            "damage": None,
            "critical_condition": None,
            "total_damage": None
        }
        
        # Pass the plural form category to create_equipment
        success, msg = self.equipment_manager.create_equipment(category, equip_name, blank_equipment)
        
        if success:
            return f"Created blank {equip_type} with name '{equip_name}'. Use modify command to set attributes."
        return msg

    def generate_equipment_id(self, equip_type):
        """Generate next available ID for equipment type"""
        # Use plural form for getting the list
        category = self.equipment_types[equip_type]
        paths = self.equipment_manager.get_equipment_list(category)
        
        current_ids = []
        id_pattern = re.compile(rf"{equip_type}_(\d+)")
        
        for path in paths:
            filename = os.path.basename(path)
            match = id_pattern.match(filename.split('.')[0])
            if match:
                current_ids.append(int(match.group(1)))
        
        # If no IDs found, start with 001
        if not current_ids:
            return f"{equip_type}_001"
        
        # Get next available ID
        next_id = max(current_ids) + 1
        return f"{equip_type}_{str(next_id).zfill(3)}"



    def modify_equipment(self, *args):
        if not args:
            return "Error: modify command requires arguments. Type 'modify help' for usage."
            
        if args[0] == 'help':
            return self.command_help['modify']
            
        # Check if item name is properly quoted
        if not (args[0].startswith("'") and args[0].endswith("'")):
            return "Error: Item name must be enclosed in single quotes"
            
        item_name = args[0][1:-1]  # Remove quotes
        
        if len(args) < 3:
            return "Error: modify command requires attribute and value"
            
        attr_name = args[1].lower()
        
        # Validate attribute exists
        if attr_name not in self.valid_attributes:
            return f"Error: Invalid attribute '{attr_name}'. Type 'modify help' to see valid attributes"
            
        # Get current equipment data
        file_path = self.find_equipment_path(item_name)
        if not file_path:
            return f"Error: Equipment '{item_name}' not found"
            
        current_data = self.equipment_manager.load_equipment_data(file_path)
        if "error" in current_data:
            return f"Error loading equipment data: {current_data['error']}"
        
        try:
            # Handle perks list operations
            if attr_name == 'perks':
                if len(args) < 3:
                    return "Error: perks modification requires an action (append, remove, clear)"
                    
                action = args[2].lower()
                
                # Initialize perks list if it doesn't exist
                if 'perks' not in current_data:
                    current_data['perks'] = []
                
                if action == 'clear':
                    current_data['perks'] = []
                elif action == 'append' and len(args) >= 4:
                    perk = " ".join(args[3:])
                    if perk not in current_data['perks']:
                        current_data['perks'].append(perk)
                elif action == 'remove' and len(args) >= 4:
                    perk = " ".join(args[3:])
                    if perk in current_data['perks']:
                        current_data['perks'].remove(perk)
                else:
                    return "Error: Invalid perks action. Use append, remove, or clear"
            else:
                # Handle regular attributes
                value = " ".join(args[2:])
                is_valid, validated_value = self.validate_value(attr_name, value)
                
                if not is_valid:
                    return validated_value  # Error message
                    
                current_data[attr_name] = validated_value
            
            # Save modifications
            success, msg = self.equipment_manager.modify_equipment(file_path, current_data)
            return msg
            
        except Exception as e:
            return f"Error executing modify command: {str(e)}"

    def validate_value(self, attr_name, value):
            """Validate value type for an attribute"""
            expected_type = self.valid_attributes[attr_name]
            
            if attr_name == 'perks':
                return True  # Perks are handled separately
            
            try:
                if expected_type == int:
                    int_value = int(value)
                    return True, int_value
                elif expected_type == str:
                    # Check if string value is properly quoted
                    if not (value.startswith("'") and value.endswith("'")):
                        return False, f"String value must be enclosed in single quotes for {attr_name}"
                    # Remove quotes and return the string
                    return True, value[1:-1]
            except ValueError:
                return False, f"Invalid value type for {attr_name}. Expected {expected_type.__name__}"
            
            return False, f"Invalid value type for {attr_name}"


    def delete_equipment(self, *args):
        if not args:
            return "Error: delete command requires equipment name"
        name = args[0]
        file_path = self.find_equipment_path(name)
        if file_path:
            success, msg = self.equipment_manager.delete_equipment(file_path)
            return msg
        return f"Error: Equipment '{name}' not found"
    
    def show_equipment(self, *args):
            if not args:
                return "Error: show command requires an option. Type 'show help' for usage."
            
            option = args[0].lower()
            
            # Show all equipment
            if option == 'all':
                return self.show_all_equipment()
                
            # Show equipment by category
            if option == 'category':
                if len(args) < 2:
                    return "Error: Please specify a category. Available categories: weapons, armors, shields"
                category = args[1].lower()
                return self.show_category_equipment(category)
                
            # Show specific equipment
            # Join all args to handle names with spaces
            name = ' '.join(args)
            file_path = self.find_equipment_path(name)
            if file_path:
                data = self.equipment_manager.load_equipment_data(file_path)
                # Use single quotes for the f-string and double quotes for the content
                name_cleaned = name.strip("'\"")  # Clean the name first
                return f'{name_cleaned}:\n{json.dumps(data, indent=2)}'
            return f"Equipment '{name.strip('\"')}' not found"
           
    def show_category_equipment(self, category):
            """Show all equipment in a specific category"""
            if category not in self.equipment_manager.categories:
                return f"Error: Invalid category '{category}'. Available categories: {', '.join(self.equipment_manager.categories)}"
                
            paths = self.equipment_manager.get_equipment_list(category)
            if not paths:
                return f"No equipment found in category '{category}'"
                
            result = [f"\n{category.upper()}:"]
            for path in paths:
                name = os.path.splitext(os.path.basename(path))[0].replace('_', ' ').title()
                data = self.equipment_manager.load_equipment_data(path)
                result.append(f"\n{name}:")
                result.append(json.dumps(data, indent=2))
                
            return "\n".join(result)
        
    def show_all_equipment(self):
        """Show all equipment in all categories"""
        result = []
        has_equipment = False
        
        for category in self.equipment_manager.categories:
            paths = self.equipment_manager.get_equipment_list(category)
            if paths:  # Only show categories with equipment
                has_equipment = True
                result.append(f"\n{category.upper()}:")
                for path in paths:
                    name = os.path.splitext(os.path.basename(path))[0].replace('_', ' ').title()
                    data = self.equipment_manager.load_equipment_data(path)
                    result.append(f"\n{name}:")
                    result.append(json.dumps(data, indent=2))
        
        if has_equipment:
            return "\n".join(result)
        return "No equipment found in any category"
 


    def find_equipment_path(self, name):
        """Find equipment file path by name"""
        # Remove any surrounding quotes if present
        name = name.strip("'\"")
        
        # Convert to filename format
        name_pattern = name.lower().replace(' ', '_')
        
        # Search through all categories
        for category, paths in self.equipment_manager.storage_paths.items():
            for path in paths:
                if name_pattern in os.path.splitext(os.path.basename(path))[0].lower():
                    return path
        return None
    
        """Find equipment file path by name"""
        name_pattern = name.lower().replace(' ', '_')
        for category, paths in self.equipment_manager.storage_paths.items():
            for path in paths:
                if name_pattern in path.lower():
                    return path
        return None