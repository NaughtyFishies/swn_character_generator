#!/usr/bin/env python3
"""
Example usage of the SWN Character Generator

This script demonstrates how to use the character generator
to create Stars Without Number characters.
"""

from swn.generator import CharacterGenerator
from swn.display import CharacterDisplay

# Create a generator instance
gen = CharacterGenerator()

# ============================================================================
# EXAMPLE 1: Quick Random Character
# ============================================================================
print("EXAMPLE 1: Quick Random Character")
print("=" * 70)

# Generate a completely random character at level 1
random_char = gen.generate_character()
CharacterDisplay.print_character(random_char)
print("\n\n")

# ============================================================================
# EXAMPLE 2: Specify Name and Class
# ============================================================================
print("EXAMPLE 2: Named Warrior Character")
print("=" * 70)

warrior = gen.generate_character(
    name="Kane Striker",
    class_choice="Warrior"
)
CharacterDisplay.print_character(warrior)
print("\n\n")

# ============================================================================
# EXAMPLE 3: Using Standard Array for Attributes
# ============================================================================
print("EXAMPLE 3: Expert with Standard Array")
print("=" * 70)

expert = gen.generate_character(
    name="Nova Tech",
    level=1,
    attribute_method="array",  # Use 14, 12, 11, 10, 9, 7 array
    class_choice="Expert"
)
CharacterDisplay.print_character(expert)
print("\n\n")

# ============================================================================
# EXAMPLE 4: Higher Level Character
# ============================================================================
print("EXAMPLE 4: Level 3 Psychic")
print("=" * 70)

psychic = gen.generate_character(
    name="Mind Bender",
    level=3,
    power_type="psionic",
    class_choice="Psychic"
)
CharacterDisplay.print_character(psychic)
print("\n\n")

# ============================================================================
# EXAMPLE 5: Magic Spellcaster
# ============================================================================
print("EXAMPLE 5: Level 2 Arcanist (Magic User)")
print("=" * 70)

arcanist = gen.generate_character(
    name="Lyra Arcanum",
    level=2,
    attribute_method="array",
    power_type="magic",
    class_choice="Arcanist"
)
CharacterDisplay.print_character(arcanist)
print("\n\n")

# ============================================================================
# EXAMPLE 6: Save Character to File
# ============================================================================
print("EXAMPLE 6: Saving Character to Files")
print("=" * 70)

char_to_save = gen.generate_character(
    name="Saved Character",
    level=1,
    class_choice="Adventurer"
)

# Save as text file
CharacterDisplay.save_to_file(char_to_save, "my_character.txt")
print("✓ Character sheet saved to: my_character.txt")

# Save as JSON
CharacterDisplay.export_json(char_to_save, "my_character.json")
print("✓ Character data saved to: my_character.json")

print("\n")

# ============================================================================
# EXAMPLE 7: Generate Multiple Characters
# ============================================================================
print("EXAMPLE 7: Generate Party of 4 Characters")
print("=" * 70)

party_configs = [
    {"name": "Tank", "class_choice": "Warrior"},
    {"name": "Scout", "class_choice": "Expert"},
    {"name": "Mage", "class_choice": "Arcanist", "power_type": "magic"},
    {"name": "Face", "class_choice": "Adventurer"}
]

for i, config in enumerate(party_configs, 1):
    char = gen.generate_character(**config)
    print(f"\nParty Member {i}: {char.name}")
    print(f"  Class: {char.character_class.name}")
    print(f"  HP: {char.hp}")
    print(f"  Skills: {', '.join([s.name for s in char.skills.get_all_skills()])}")
    print(f"  Foci: {', '.join([f.name for f in char.foci])}")

print("\n")

# ============================================================================
# ALL AVAILABLE OPTIONS
# ============================================================================
print("=" * 70)
print("AVAILABLE OPTIONS FOR generate_character()")
print("=" * 70)
print("""
gen.generate_character(
    name="Character Name",           # Optional, random if None
    level=1,                         # Character level (1-10)
    attribute_method="roll",         # "roll" or "array"
    power_type="normal",             # "normal", "magic", or "psionic"
    class_choice="Warrior",          # Class name or None for random
    use_quick_skills=True            # Use quick skills (default True)
)

ATTRIBUTE METHODS:
  - "roll": Roll 3d6 six times in order, pick one to set to 14
  - "array": Use standard array (14, 12, 11, 10, 9, 7) randomly assigned

POWER TYPES:
  - "normal": Regular character, no psychic powers
  - "magic": Gets psychic disciplines (for magic classes)
  - "psionic": Gets psychic disciplines (for Psychic class)

AVAILABLE CLASSES:
  Base Classes:
    - Warrior: Combat specialist
    - Expert: Skills specialist
    - Psychic: Psychic powers specialist
    - Adventurer: Jack of all trades

  Magic Classes:
    - Arcane Expert: Expert with magic abilities
    - Arcane Warrior: Warrior with magic abilities
    - Arcanist: Academic magic tradition
    - Pacter: Shadow summoner
    - Rectifier: Flesh/healing magic
    - War Mage: Military support magic

  Special Classes:
    - Free Nexus: Support class with symbiosis
    - Godhunter: Shadow hunters
    - Sunblade: Warrior-monks
    - Yama King: Wandering judges

DISPLAY & SAVE METHODS:
  - CharacterDisplay.print_character(char)        # Print to console
  - CharacterDisplay.save_to_file(char, "file.txt")  # Save as text
  - CharacterDisplay.export_json(char, "file.json")  # Save as JSON
""")
