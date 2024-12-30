import os
import json


def find_base_directory(base_name='KHGame/MAIN'):
    current_directory = os.getcwd()

    while True:
        # Look for the folder that contains "KHGame" and "V2"
        potential_base = os.path.join(current_directory, base_name, 'FIGHT SEQUENCES')
        if os.path.exists(potential_base):
            return potential_base
        else:
            parent_directory = os.path.dirname(current_directory)
            if parent_directory == current_directory:
                # Reached root directory, stop searching
                raise FileNotFoundError(f"{base_name}/FIGHT SEQUENCES not found.")
            current_directory = parent_directory

# Set BASE_DIRECTORY dynamically
BASE_DIRECTORY = find_base_directory()