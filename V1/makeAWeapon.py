import json
import os

class Weapon:
    def __init__(self, name="none", weapon_type="none", perk_crit_bonus="none", strike=0, protection=0, defense=0, speed=0, evade=0, block=0, damage=0):
        self.weaponID = 0
        
        self.name = name
        self.weapon_type = weapon_type
        self.perk_crit_bonus = perk_crit_bonus
        self.strike = strike
        self.protection = protection
        self.defense = defense
        self.speed = speed
        self.evade = evade
        self.block = block
        self.damage = damage

    def display_info(self):
        """Display the weapon's information."""
        print(f"Weapon Name: {self.name}")
        print(f"Weapon Type: {self.weapon_type}")
        print(f"Perk/Crit Bonus: {self.perk_crit_bonus}")
        print(f"Strike: {self.strike}")
        print(f"Protection: {self.protection}")
        print(f"Defense: {self.defense}")
        print(f"Speed: {self.speed}")
        print(f"Evade: {self.evade}")
        print(f"Block: {self.block}")
        print(f"Damage: {self.damage}")

    def to_dict(self):
        """Convert the weapon object to a dictionary."""
        return {
            "name": self.name,
            "weapon_type": self.weapon_type,
            "perk_crit_bonus": self.perk_crit_bonus,
            "strike": self.strike,
            "protection": self.protection,
            "defense": self.defense,
            "speed": self.speed,
            "evade": self.evade,
            "block": self.block,
            "damage": self.damage
        }

    def save_to_json(self, directory='equipment\weapons'):
        """Save the weapon to a JSON file in the specified directory."""
        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create the file path
        file_path = os.path.join(directory, f"Weapon_{self.weaponID}.json")
        self.weaponID =+ 1

        # Write the weapon data to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(self.to_dict(), json_file, indent=4)
        print(f"Weapon '{self.name}' saved to '{file_path}'")

# Example usage
longSword = Weapon(
    name="Gladius salutis",
    weapon_type="Longsword",
    perk_crit_bonus="Bleeder",
    strike=10,
    protection=0,
    defense=10,
    speed=(-1),
    evade=0,
    block=10,
    damage=10
)

broadSword = Weapon(
    name="Siegfrieds Breitschwert",
    weapon_type="Broadsword",
    perk_crit_bonus="Bleeder, Mover",
    strike=11,
    protection=0,
    defense=10,
    speed=(-2),
    evade=(-10),
    block=10,
    damage=20
)

warHammer = Weapon(
    name="Kriegshammer",
    weapon_type="War Hammer",
    perk_crit_bonus="Paralizer, Stunner, Piercer",
    strike=9,
    protection=0,
    defense=4,
    speed=(-1),
    evade=0,
    block=7,
    damage=12
)

battleAxe = Weapon(
    name="Kampøks",
    weapon_type="Battle Axe",
    perk_crit_bonus="Bleeder, Paralizer, Stunner, Mover",
    strike=12,
    protection=(-3),
    defense=10,
    speed=(-3),
    evade=(-5),
    block=5,
    damage=18
)

sceptre = Weapon(
    name="Sceptre",
    weapon_type="sceptre",
    perk_crit_bonus="Paralizer, Stunner",
    strike=6,
    protection=0,
    defense=3,
    speed=(-1),
    evade=0,
    block=6,
    damage=7
)



longSword.save_to_json()
broadSword.save_to_json()
warHammer.save_to_json()
battleAxe.save_to_json()
sceptre.save_to_json()
