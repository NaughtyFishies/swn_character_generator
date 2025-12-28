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


# ============================================================================
# CELL 13: Equipment and Tech Levels
# ============================================================================
print("=" * 70)
print("EQUIPMENT SYSTEM - TECH LEVEL EXAMPLES")
print("=" * 70)
print()

tech_examples = [
    {
        "name": "Barbarian",
        "tech_level": 0,
        "class_choice": "Warrior",
        "description": "Stone age primitive (TL0)"
    },
    {
        "name": "Modern Soldier",
        "tech_level": 4,
        "class_choice": "Warrior",
        "description": "Standard spacefaring (TL4)"
    },
    {
        "name": "Pretech Scout",
        "tech_level": 5,
        "class_choice": "Expert",
        "description": "Advanced Mandate-era (TL5)"
    }
]

for config in tech_examples:
    print(f"\n{config['name']} - {config['description']}")
    print("-" * 70)

    char = gen.generate_character(
        name=config["name"],
        level=1,
        class_choice=config["class_choice"],
        tech_level=config["tech_level"]
    )

    # Show equipment summary
    print(f"Starting Credits: {char.credits + char.equipment.total_cost()} cr")
    print(f"Spent: {char.equipment.total_cost()} cr | Remaining: {char.credits} cr")
    print(f"Total Encumbrance: {char.equipment.total_encumbrance()}")
    print()

    # Show armor
    if char.equipment.armor:
        armor = char.equipment.armor
        ac = armor.properties.get("ac", "10")
        print(f"Armor: {armor.name} (AC {ac}, TL{armor.tech_level})")

    # Show weapons
    if char.equipment.weapons:
        print("Weapons:")
        for weapon in char.equipment.weapons:
            damage = weapon.properties.get("damage", "—")
            range_val = weapon.properties.get("range", "")
            if range_val:
                print(f"  • {weapon.name}: {damage} damage, {range_val}m (TL{weapon.tech_level})")
            else:
                shock = weapon.properties.get("shock", "")
                print(f"  • {weapon.name}: {damage} damage, Shock {shock} (TL{weapon.tech_level})")

    # Show gear
    if char.equipment.gear:
        print(f"Gear ({len(char.equipment.gear)} items):")
        for item in char.equipment.gear[:5]:  # Show first 5 items
            print(f"  • {item.name} (TL{item.tech_level})")
        if len(char.equipment.gear) > 5:
            print(f"  ... and {len(char.equipment.gear) - 5} more items")


# ============================================================================
# CELL 14: Psychic Disciplines and Techniques
# ============================================================================
print("\n\n")
print("=" * 70)
print("PSYCHIC DISCIPLINES AND TECHNIQUES")
print("=" * 70)
print()

print("Full Psychic (2 disciplines)")
print("-" * 70)
psychic = gen.generate_character(
    name="Mind Walker",
    level=3,
    power_type="psionic",
    class_choice="Psychic",
    attribute_method="array"
)

# Show discipline skills
psychic_disciplines = ["Biopsionics", "Metapsionics", "Precognition",
                      "Telekinesis", "Telepathy", "Teleportation"]

print(f"Effort Pool: {psychic.psychic_powers.effort_pool}")
print()

for disc_name in psychic_disciplines:
    if psychic.skills.has_skill(disc_name):
        skill_level = psychic.skills.get_level(disc_name)
        print(f"{disc_name}-{skill_level}:")

        # Show techniques for this discipline
        techniques = psychic.psychic_powers.get_techniques(disc_name)
        for tech in techniques:
            effort_str = f"({tech.effort_cost} Effort)" if tech.effort_cost > 0 else "(Core)"
            print(f"  • {tech.name} {effort_str}")
            # Truncate description
            desc = tech.description[:70] + "..." if len(tech.description) > 70 else tech.description
            print(f"    {desc}")
        print()

print("\n" + "=" * 70)
print("Partial Psychic (Arcanist with 1 discipline)")
print("-" * 70)
arcanist_psychic = gen.generate_character(
    name="Mystic Scholar",
    level=2,
    power_type="magic",
    class_choice="Arcanist",
    attribute_method="array"
)

# Show that they have both spells AND psychic powers
if arcanist_psychic.spells:
    print(f"Spells: {len(arcanist_psychic.spells.known_spells)} known ({arcanist_psychic.spells.tradition})")

if arcanist_psychic.psychic_powers:
    print(f"Effort Pool: {arcanist_psychic.psychic_powers.effort_pool}")
    print()

    for disc_name in psychic_disciplines:
        if arcanist_psychic.skills.has_skill(disc_name):
            skill_level = arcanist_psychic.skills.get_level(disc_name)
            print(f"{disc_name}-{skill_level}:")

            techniques = arcanist_psychic.psychic_powers.get_techniques(disc_name)
            for tech in techniques:
                effort_str = f"({tech.effort_cost} Effort)" if tech.effort_cost > 0 else "(Core)"
                print(f"  • {tech.name} {effort_str}")


# ============================================================================
# CELL 15: High-Level Character Showcase (Levels 5-10)
# ============================================================================
print("\n\n")
print("=" * 70)
print("HIGH-LEVEL CHARACTER PROGRESSION (Level 5 & 10)")
print("=" * 70)
print()

print("Level 5 Warrior")
print("-" * 70)
warrior_5 = gen.generate_character(
    name="Veteran Soldier",
    level=5,
    class_choice="Warrior",
    tech_level=4,
    attribute_method="array"
)

print(f"HP: {warrior_5.hp}")
print(f"Attack Bonus: +{warrior_5.attack_bonus}")
print(f"Skills: {len(warrior_5.skills.get_all_skills())}")
print("Sample Skills:")
for skill in warrior_5.skills.get_all_skills()[:8]:
    print(f"  • {skill}")
print(f"Starting Credits: {warrior_5.credits + warrior_5.equipment.total_cost()} cr")
print(f"Equipment Value: {warrior_5.equipment.total_cost()} cr")
print()

print("Level 10 Arcanist (Maximum Power)")
print("-" * 70)
arcanist_10 = gen.generate_character(
    name="Archmage Supreme",
    level=10,
    class_choice="Arcanist",
    power_type="magic",
    tech_level=5,
    attribute_method="array"
)

print(f"HP: {arcanist_10.hp}")
print(f"Attack Bonus: +{arcanist_10.attack_bonus}")
print(f"Skills: {len(arcanist_10.skills.get_all_skills())}")

# Show spell progression
if arcanist_10.spells:
    print(f"\nSpell Tradition: {arcanist_10.spells.tradition}")
    print(f"Total Known Spells: {len(arcanist_10.spells.known_spells)}")
    print("\nSpell Slots per Day:")
    for level in range(1, 6):
        slots = arcanist_10.spells.get_spell_slots(level)
        if slots > 0:
            level_spells = arcanist_10.spells.get_spells_by_level(level)
            print(f"  Level {level}: {len(level_spells)} known / {slots} slots")

# Show high-level skill examples
print("\nSample Skills (with high levels):")
all_skills = warrior_5.skills.get_all_skills()
for skill in arcanist_10.skills.get_all_skills()[:10]:
    print(f"  • {skill}")

print(f"\nStarting Credits: {arcanist_10.credits + arcanist_10.equipment.total_cost()} cr")
print(f"Equipment Value: {arcanist_10.equipment.total_cost()} cr")


# ============================================================================
# CELL 16: Tech Level Comparison (All TL0-5)
# ============================================================================
print("\n\n")
print("=" * 70)
print("COMPLETE TECH LEVEL COMPARISON (TL0 through TL5)")
print("=" * 70)
print()

print(f"{'TL':3} | {'Description':25} | {'Credits':8} | {'Armor':30} | {'Primary Weapon':25}")
print("-" * 100)

tech_levels = [
    (0, "Stone Age"),
    (1, "Medieval"),
    (2, "Renaissance"),
    (3, "Industrial"),
    (4, "Spacefaring"),
    (5, "Pretech/Mandate")
]

for tl, desc in tech_levels:
    char = gen.generate_character(
        name=f"TL{tl} Character",
        level=1,
        class_choice="Warrior",
        tech_level=tl,
        attribute_method="array"
    )

    armor_name = char.equipment.armor.name if char.equipment.armor else "None"
    weapon_name = char.equipment.weapons[0].name if char.equipment.weapons else "None"

    total_credits = char.credits + char.equipment.total_cost()

    print(f"{tl:3} | {desc:25} | {total_credits:8} | {armor_name:30} | {weapon_name:25}")
