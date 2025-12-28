"""
Code examples for Jupyter Notebooks / Google Colab
Copy and paste these cells into your notebook
"""

# ============================================================================
# CELL 1: Setup and Import
# ============================================================================
from swn.generator import CharacterGenerator
from swn.display import CharacterDisplay

# Create generator instance
gen = CharacterGenerator()

print("✓ Character generator loaded!")
print("✓ Ready to generate characters")


# ============================================================================
# CELL 2: Generate All Base Classes
# ============================================================================
print("=" * 70)
print("GENERATING ALL BASE CLASSES")
print("=" * 70)
print()

base_classes = ["Warrior", "Expert", "Psychic", "Adventurer"]

for class_name in base_classes:
    power_type = "psionic" if class_name == "Psychic" else "normal"

    char = gen.generate_character(
        name=f"Sample {class_name}",
        level=1,
        attribute_method="array",
        power_type=power_type,
        class_choice=class_name
    )

    CharacterDisplay.print_character(char)
    print("\n" * 2)


# ============================================================================
# CELL 3: Generate All Magic Classes
# ============================================================================
print("=" * 70)
print("GENERATING ALL MAGIC CLASSES")
print("=" * 70)
print()

magic_classes = [
    "Arcanist",
    "Pacter",
    "Rectifier",
    "War Mage",
    "Arcane Expert",
    "Arcane Warrior"
]

for class_name in magic_classes:
    char = gen.generate_character(
        name=f"Sample {class_name}",
        level=1,
        attribute_method="array",
        power_type="magic",  # Important for magic classes!
        class_choice=class_name
    )

    CharacterDisplay.print_character(char)
    print("\n" * 2)


# ============================================================================
# CELL 4: Generate All Special Classes
# ============================================================================
print("=" * 70)
print("GENERATING ALL SPECIAL CLASSES")
print("=" * 70)
print()

special_classes = [
    "Free Nexus",
    "Godhunter",
    "Sunblade",
    "Yama King"
]

for class_name in special_classes:
    char = gen.generate_character(
        name=f"Sample {class_name}",
        level=1,
        attribute_method="array",
        class_choice=class_name
    )

    CharacterDisplay.print_character(char)
    print("\n" * 2)


# ============================================================================
# CELL 5: Generate One of Each Class (Compact View)
# ============================================================================
print("=" * 70)
print("ALL 14 CLASSES - COMPACT SUMMARY")
print("=" * 70)
print()

all_classes = {
    "Base": ["Warrior", "Expert", "Psychic", "Adventurer"],
    "Magic": ["Arcanist", "Pacter", "Rectifier", "War Mage", "Arcane Expert", "Arcane Warrior"],
    "Special": ["Free Nexus", "Godhunter", "Sunblade", "Yama King"]
}

for category, classes in all_classes.items():
    print(f"\n{category} Classes:")
    print("-" * 70)

    for class_name in classes:
        # Determine power type
        power_type = "normal"
        if class_name == "Psychic":
            power_type = "psionic"
        elif class_name in ["Arcanist", "Pacter", "Rectifier", "War Mage",
                           "Arcane Expert", "Arcane Warrior"]:
            power_type = "magic"

        char = gen.generate_character(
            level=1,
            attribute_method="array",
            power_type=power_type,
            class_choice=class_name
        )

        # Compact summary
        skills_count = len(char.skills.get_all_skills())
        foci_names = ", ".join([f.name for f in char.foci])

        print(f"  {class_name:20} | HP: {char.hp:2} | Skills: {skills_count} | Foci: {foci_names}")

        # Show spell count for spellcasters
        if char.spells:
            spell_count = len(char.spells.known_spells)
            print(f"  {'':20} | Spells: {spell_count} ({char.spells.tradition} tradition)")


# ============================================================================
# CELL 6: Generate High-Level Characters (Levels 1-5)
# ============================================================================
print("=" * 70)
print("LEVEL PROGRESSION EXAMPLES")
print("=" * 70)
print()

# Show how a Warrior progresses
print("Warrior Progression (Levels 1-5):")
print("-" * 70)
for level in range(1, 6):
    warrior = gen.generate_character(
        name=f"Warrior L{level}",
        level=level,
        attribute_method="array",
        class_choice="Warrior"
    )

    skills = len(warrior.skills.get_all_skills())
    print(f"Level {level}: HP={warrior.hp:2}, Skills={skills}, Attack Bonus=+{warrior.attack_bonus}")

print()

# Show how a spellcaster progresses
print("Arcanist Progression (Levels 1-5) - Spell Growth:")
print("-" * 70)
for level in range(1, 6):
    arcanist = gen.generate_character(
        name=f"Arcanist L{level}",
        level=level,
        attribute_method="array",
        power_type="magic",
        class_choice="Arcanist"
    )

    # Count spells by level
    spell_counts = {}
    for spell in arcanist.spells.known_spells:
        spell_counts[spell.level] = spell_counts.get(spell.level, 0) + 1

    spell_summary = ", ".join([f"L{lvl}:{cnt}" for lvl, cnt in sorted(spell_counts.items())])
    print(f"Level {level}: {len(arcanist.spells.known_spells)} total spells ({spell_summary})")


# ============================================================================
# CELL 7: Generate a Complete Party
# ============================================================================
print("=" * 70)
print("SAMPLE ADVENTURING PARTY")
print("=" * 70)
print()

party_configs = [
    {"name": "Brutus", "class_choice": "Warrior", "level": 2},
    {"name": "Cipher", "class_choice": "Expert", "level": 2},
    {"name": "Mystic", "class_choice": "Arcanist", "level": 2, "power_type": "magic"},
    {"name": "Shadow", "class_choice": "Pacter", "level": 2, "power_type": "magic"},
]

for config in party_configs:
    char = gen.generate_character(**config)
    CharacterDisplay.print_character(char)
    print("\n" * 2)


# ============================================================================
# CELL 8: Compare Attribute Methods (Roll vs Array)
# ============================================================================
print("=" * 70)
print("COMPARING ATTRIBUTE METHODS")
print("=" * 70)
print()

print("Method 1: ARRAY (14, 12, 11, 10, 9, 7)")
print("-" * 70)
array_char = gen.generate_character(
    name="Array Method",
    attribute_method="array",
    class_choice="Warrior"
)

print(f"STR: {array_char.attributes.STR} | DEX: {array_char.attributes.DEX} | CON: {array_char.attributes.CON}")
print(f"INT: {array_char.attributes.INT} | WIS: {array_char.attributes.WIS} | CHA: {array_char.attributes.CHA}")
print()

print("Method 2: ROLL (3d6 six times, pick one to set to 14)")
print("-" * 70)
roll_char = gen.generate_character(
    name="Roll Method",
    attribute_method="roll",
    class_choice="Warrior"
)

print(f"STR: {roll_char.attributes.STR} | DEX: {roll_char.attributes.DEX} | CON: {roll_char.attributes.CON}")
print(f"INT: {roll_char.attributes.INT} | WIS: {roll_char.attributes.WIS} | CHA: {roll_char.attributes.CHA}")


# ============================================================================
# CELL 9: Save Characters to Files
# ============================================================================
print("=" * 70)
print("SAVING CHARACTERS TO FILES")
print("=" * 70)
print()

# Generate a character
my_character = gen.generate_character(
    name="My Hero",
    level=3,
    class_choice="Arcane Warrior",
    power_type="magic"
)

# Save as text
CharacterDisplay.save_to_file(my_character, "my_hero.txt")
print("✓ Saved character sheet to: my_hero.txt")

# Save as JSON
CharacterDisplay.export_json(my_character, "my_hero.json")
print("✓ Saved character data to: my_hero.json")

# Display the character
print()
CharacterDisplay.print_character(my_character)


# ============================================================================
# CELL 10: Generate Random Characters (Quick Tests)
# ============================================================================
print("=" * 70)
print("10 RANDOM CHARACTERS")
print("=" * 70)
print()

for i in range(10):
    char = gen.generate_character()

    skills = len(char.skills.get_all_skills())
    foci = ", ".join([f.name for f in char.foci[:2]])  # Show first 2 foci
    if len(char.foci) > 2:
        foci += "..."

    spell_info = ""
    if char.spells:
        spell_info = f" | Spells: {len(char.spells.known_spells)}"

    print(f"{i+1:2}. {char.name:20} | {char.character_class.name:15} | "
          f"HP:{char.hp:2} | Skills:{skills}{spell_info}")


# ============================================================================
# CELL 11: Test All Spell Traditions
# ============================================================================
print("=" * 70)
print("ALL SPELL TRADITIONS AT LEVEL 3")
print("=" * 70)
print()

spell_classes = {
    "Arcanist": "Academic magic with versatile spells",
    "Pacter": "Shadow summoning and control",
    "Rectifier": "Healing and flesh transformation",
    "War Mage": "Military tactical support magic"
}

for class_name, description in spell_classes.items():
    print(f"\n{class_name}")
    print(f"Description: {description}")
    print("-" * 70)

    char = gen.generate_character(
        name=f"Test {class_name}",
        level=3,
        power_type="magic",
        class_choice=class_name
    )

    # Show spell breakdown
    spell_counts = {}
    for spell in char.spells.known_spells:
        spell_counts[spell.level] = spell_counts.get(spell.level, 0) + 1

    print(f"Total Spells: {len(char.spells.known_spells)}")
    for spell_level in sorted(spell_counts.keys()):
        count = spell_counts[spell_level]
        print(f"  Level-{spell_level} spells: {count}")

    # Show a few example spells
    print("\nExample spells:")
    for spell in char.spells.known_spells[:4]:
        print(f"  • {spell.name} (Level {spell.level})")
        print(f"    {spell.description[:80]}...")


# ============================================================================
# CELL 12: Class Comparison Matrix
# ============================================================================
print("=" * 70)
print("CLASS COMPARISON MATRIX")
print("=" * 70)
print()

all_class_names = [
    "Warrior", "Expert", "Psychic", "Adventurer",
    "Arcanist", "Pacter", "Rectifier", "War Mage",
    "Arcane Expert", "Arcane Warrior",
    "Free Nexus", "Godhunter", "Sunblade", "Yama King"
]

print(f"{'Class':20} | {'HP':3} | {'Skills':6} | {'Foci':4} | {'AB':2} | Features")
print("-" * 90)

for class_name in all_class_names:
    # Determine power type
    power_type = "normal"
    if class_name == "Psychic":
        power_type = "psionic"
    elif class_name in ["Arcanist", "Pacter", "Rectifier", "War Mage",
                       "Arcane Expert", "Arcane Warrior"]:
        power_type = "magic"

    char = gen.generate_character(
        level=1,
        attribute_method="array",
        power_type=power_type,
        class_choice=class_name
    )

    skills = len(char.skills.get_all_skills())
    foci = len(char.foci)

    features = []
    if char.spells:
        features.append(f"{len(char.spells.known_spells)} spells")
    if char.psychic_powers:
        features.append("Psychic")
    if char.attack_bonus > 0:
        features.append("Combat")

    features_str = ", ".join(features) if features else "—"

    print(f"{class_name:20} | {char.hp:3} | {skills:6} | {foci:4} | +{char.attack_bonus:1} | {features_str}")
