# Jupyter Notebook / Google Colab Guide

Copy and paste these code cells into your Jupyter notebook or Google Colab.

---

## CELL 1: Setup

```python
from swn.generator import CharacterGenerator
from swn.display import CharacterDisplay

# Create generator instance
gen = CharacterGenerator()

print("✓ Character generator loaded!")
```

---

## CELL 2: Generate All Base Classes (4 classes)

```python
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
```

---

## CELL 3: Generate All Magic Classes (6 classes)

```python
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
        power_type="magic",  # Important!
        class_choice=class_name
    )

    CharacterDisplay.print_character(char)
    print("\n" * 2)
```

---

## CELL 4: Generate All Special Classes (4 classes)

```python
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
```

---

## CELL 5: Quick Summary of All 14 Classes

```python
print("=" * 70)
print("ALL 14 CLASSES - COMPACT SUMMARY")
print("=" * 70)

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
```

---

## CELL 6: Level Progression Example

```python
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

print("\n")
print("Arcanist Spell Progression (Levels 1-5):")
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
```

---

## CELL 7: Generate a Complete Party

```python
party = [
    gen.generate_character(name="Brutus", class_choice="Warrior", level=2),
    gen.generate_character(name="Cipher", class_choice="Expert", level=2),
    gen.generate_character(name="Mystic", class_choice="Arcanist", level=2, power_type="magic"),
    gen.generate_character(name="Shadow", class_choice="Pacter", level=2, power_type="magic"),
]

for char in party:
    CharacterDisplay.print_character(char)
    print("\n" * 2)
```

---

## CELL 8: Compare Attribute Methods

```python
print("ARRAY Method (14, 12, 11, 10, 9, 7):")
print("-" * 70)
array_char = gen.generate_character(
    name="Array Warrior",
    attribute_method="array",
    class_choice="Warrior"
)
print(f"STR: {array_char.attributes.STR} | DEX: {array_char.attributes.DEX} | CON: {array_char.attributes.CON}")
print(f"INT: {array_char.attributes.INT} | WIS: {array_char.attributes.WIS} | CHA: {array_char.attributes.CHA}")

print("\n")
print("ROLL Method (3d6 six times, pick one to set to 14):")
print("-" * 70)
roll_char = gen.generate_character(
    name="Rolled Warrior",
    attribute_method="roll",
    class_choice="Warrior"
)
print(f"STR: {roll_char.attributes.STR} | DEX: {roll_char.attributes.DEX} | CON: {roll_char.attributes.CON}")
print(f"INT: {roll_char.attributes.INT} | WIS: {roll_char.attributes.WIS} | CHA: {roll_char.attributes.CHA}")
```

---

## CELL 9: Test All Spell Traditions

```python
spell_classes = {
    "Arcanist": "Academic magic with versatile spells",
    "Pacter": "Shadow summoning and control",
    "Rectifier": "Healing and flesh transformation",
    "War Mage": "Military tactical support magic"
}

for class_name, description in spell_classes.items():
    print(f"\n{'='*70}")
    print(f"{class_name} - {description}")
    print('='*70)

    char = gen.generate_character(
        name=f"Test {class_name}",
        level=3,
        power_type="magic",
        class_choice=class_name
    )

    CharacterDisplay.print_character(char)
    print("\n")
```

---

## CELL 10: Save Characters

```python
# Generate a character
my_char = gen.generate_character(
    name="My Hero",
    level=3,
    class_choice="Arcane Warrior",
    power_type="magic"
)

# Save as text file
CharacterDisplay.save_to_file(my_char, "my_hero.txt")
print("✓ Saved to my_hero.txt")

# Save as JSON
CharacterDisplay.export_json(my_char, "my_hero.json")
print("✓ Saved to my_hero.json")

# Display
CharacterDisplay.print_character(my_char)
```

---

## CELL 11: Class Comparison Matrix

```python
all_classes = [
    "Warrior", "Expert", "Psychic", "Adventurer",
    "Arcanist", "Pacter", "Rectifier", "War Mage",
    "Arcane Expert", "Arcane Warrior",
    "Free Nexus", "Godhunter", "Sunblade", "Yama King"
]

print(f"{'Class':20} | {'HP':3} | {'Skills':6} | {'Foci':4} | {'AB':2} | Features")
print("-" * 90)

for class_name in all_classes:
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
```

---

## Tips for Google Colab

1. **Upload the character_generator folder** to your Colab session
2. **Add to Python path** (if needed):
   ```python
   import sys
   sys.path.append('/content/character_generator')
   ```
3. **Then run CELL 1** to import and set up the generator

---

## Quick Reference

### Generate Specific Class
```python
char = gen.generate_character(class_choice="Warrior")
```

### Magic Classes (MUST set power_type="magic")
```python
mage = gen.generate_character(class_choice="Arcanist", power_type="magic")
```

### Higher Level
```python
veteran = gen.generate_character(class_choice="Warrior", level=5)
```

### Custom Name
```python
hero = gen.generate_character(name="Kane Striker", class_choice="Expert")
```

### Save to File
```python
CharacterDisplay.save_to_file(hero, "character.txt")
CharacterDisplay.export_json(hero, "character.json")
```
