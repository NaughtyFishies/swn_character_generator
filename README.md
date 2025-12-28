# Stars Without Number Character Generator

A comprehensive Python-based character generator for the Stars Without Number tabletop RPG, supporting both the core rulebook and Codex of the Black Sun magic system.

## Features

✨ **Official SWN Character Creation**
- Follow the exact character creation steps from the core rulebook
- Roll attributes (3d6, pick one to set to 14) or use standard array (14, 12, 11, 10, 9, 7)
- 21 backgrounds with skill tables
- Level-based character generation (levels 1-10) with proper scaling
- Accurate skill point costs: (new level + 1) per SWN rules
- Level-based skill caps: +1 at levels 1-2, +2 at 3-5, +3 at 6-8, +4 at 9-10

⚔️ **14 Character Classes**
- **Base Classes**: Warrior, Expert, Psychic, Adventurer
- **Magic Classes**: Arcanist, Pacter, Rectifier, War Mage, Arcane Expert, Arcane Warrior
- **Special Classes**: Free Nexus, Godhunter, Sunblade, Yama King

🔮 **Magic & Psychic Systems**
- **Spell Traditions**: 4 complete spell lists (Arcanist, Pacter, Rectifier, War Mage) with 30+ spells each
- **Psychic Disciplines**: 6 disciplines as individual skills (Biopsionics, Metapsionics, Precognition, Telekinesis, Telepathy, Teleportation)
- Each discipline has a core technique (level-0) and 8-12 advanced techniques (levels 1-4)
- Technique selection: 1 technique learned per skill level increase
- Effort pool: 1 + highest discipline skill + WIS/INT modifier
- **Arcane Foci**: 27 arcane foci for magic-using characters
- Spell progression from levels 1-5 with known spells and spell slots tracked separately

🎯 **Advanced Features**
- 52 total foci (25 general + 27 arcane)
- Class-exclusive foci (Experts get non-combat, Warriors get combat bonus)
- Automatic skill point allocation with class priorities
- Export to JSON or formatted text files

⚙️ **Equipment System**
- **Tech Level Selection**: TL 0-5 (primitive to pretech)
- **18 Armor Types**: From shields to powered armor with AC 10-20
- **33 Weapons**: 25 ranged (bows to distortion cannons) + 8 melee weapons
- **27 Gear Items**: Communications, medical, tools, field equipment
- **Starting Credits**: Class/level-based (1000-2000 + 500/level)
- **Smart Selection**: Class-appropriate equipment (Warriors get combat gear, Experts get tools)
- Automatic encumbrance and cost tracking

## Installation

**Requirements**: Python 3.7+ (no external dependencies!)

```bash
# Clone or download the repository
git clone <your-repo-url>
cd character_generator

# Verify installation
python3 -c "from swn.generator import CharacterGenerator; print('✓ Installation successful!')"
```

## Quick Start

### Generate Your First Character

```python
from swn.generator import CharacterGenerator
from swn.display import CharacterDisplay

# Create generator
gen = CharacterGenerator()

# Generate a random character
char = gen.generate_character()

# Display it
CharacterDisplay.print_character(char)
```

### Command Line Quick Test

```bash
python3 -c "
from swn.generator import CharacterGenerator
from swn.display import CharacterDisplay

gen = CharacterGenerator()
char = gen.generate_character(name='Test Character', class_choice='Warrior')
CharacterDisplay.print_character(char)
"
```

## Usage Examples

### Basic Character Generation

```python
from swn.generator import CharacterGenerator
from swn.display import CharacterDisplay

gen = CharacterGenerator()

# Random character
char = gen.generate_character()

# Specific class
warrior = gen.generate_character(class_choice="Warrior")

# Named character with custom options
expert = gen.generate_character(
    name="Nova Tech",
    level=1,
    attribute_method="array",  # Use standard array instead of rolling
    class_choice="Expert"
)

CharacterDisplay.print_character(expert)
```

### Magic Characters

```python
# Arcanist (Academic magic tradition)
arcanist = gen.generate_character(
    name="Lyra Arcanum",
    level=2,
    power_type="magic",
    class_choice="Arcanist"
)

# Pacter (Shadow summoner)
pacter = gen.generate_character(
    name="Shadow Master",
    level=1,
    power_type="magic",
    class_choice="Pacter"
)

CharacterDisplay.print_character(arcanist)
```

### Psychic Characters

```python
# Full Psychic (2 disciplines)
psychic = gen.generate_character(
    name="Mind Walker",
    level=3,
    power_type="psionic",
    class_choice="Psychic"
)
# Will have 2 discipline skills (e.g., Telepathy-1, Precognition-0)
# Each discipline grants core technique + 1 technique per skill level

# Partial Psychic (1 discipline, non-Psychic class)
# Note: Only power_type="psionic" grants psychic abilities
warrior_psychic = gen.generate_character(
    name="Mind Warrior",
    level=2,
    power_type="psionic",
    class_choice="Warrior"
)
# Will have 1 discipline skill (e.g., Telekinesis-0) + warrior abilities

CharacterDisplay.print_character(psychic)
```

### Equipment & Tech Levels

```python
# Standard TL4 character (modern spacefaring tech)
modern = gen.generate_character(
    name="Spacer",
    level=1,
    class_choice="Warrior",
    tech_level=4  # Default
)
# Gets: Combat armor, energy weapons, compad, medkit

# Primitive TL0 character (stone age)
primitive = gen.generate_character(
    name="Barbarian",
    level=1,
    class_choice="Warrior",
    tech_level=0
)
# Gets: Hide armor, primitive weapons, basic supplies

# Advanced TL5 character (pretech/Mandate-era)
pretech = gen.generate_character(
    name="Ancient Tech User",
    level=5,
    class_choice="Expert",
    tech_level=5
)
# Gets: Powered armor, advanced energy weapons, pretech tools
# High starting credits: 2000 + (5 × 500) = 4500 cr

CharacterDisplay.print_character(modern)
```

### Save Characters to Files

```python
char = gen.generate_character(name="My Hero")

# Save as formatted text file
CharacterDisplay.save_to_file(char, "my_hero.txt")

# Save as JSON (for data processing/storage)
CharacterDisplay.export_json(char, "my_hero.json")
```

### Generate a Party

```python
party = [
    gen.generate_character(name="Tank", class_choice="Warrior"),
    gen.generate_character(name="Scout", class_choice="Expert"),
    gen.generate_character(name="Wizard", class_choice="Arcanist", power_type="magic"),
    gen.generate_character(name="Face", class_choice="Adventurer")
]

for char in party:
    CharacterDisplay.print_character(char)
    print("\n")
```

## API Reference

### CharacterGenerator

```python
character = gen.generate_character(
    name=None,                   # Character name (random if None)
    level=1,                     # Character level (1-10)
    attribute_method="roll",     # "roll" or "array"
    power_type="normal",         # "normal", "magic", or "psionic"
    class_choice=None,           # Class name or None for random
    use_quick_skills=True,       # Use quick skills from background
    tech_level=4                 # Equipment tech level (0-5)
)
```

**Parameters:**

- **name** (str, optional): Character name. Auto-generated if None.
- **level** (int): Character level (1-10), default 1.
  - HP, skill points, spell slots, and technique selection scale with level
  - Skill caps: +1 (levels 1-2), +2 (3-5), +3 (6-8), +4 (9-10)
- **attribute_method** (str):
  - `"roll"`: Roll 3d6 six times in order, pick one to set to 14
  - `"array"`: Use standard array (14, 12, 11, 10, 9, 7) randomly assigned
- **power_type** (str):
  - `"normal"`: Regular character, no psychic/magic powers
  - `"magic"`: Character with magical abilities (for magic classes)
  - `"psionic"`: Character with psychic powers (for Psychic class)
- **class_choice** (str, optional): Class name or None for random
- **tech_level** (int): Equipment technology level (0-5), default 4
  - TL0: Stone age (hide armor, clubs, bows)
  - TL1-2: Medieval to Renaissance (plate armor, firearms)
  - TL3: Industrial (combat rifles, woven armor)
  - TL4: Standard spacefaring (energy weapons, vacc suits)
  - TL5: Pretech/Mandate-era (powered armor, advanced energy weapons)

### CharacterDisplay Methods

```python
CharacterDisplay.print_character(character)              # Print to console
CharacterDisplay.save_to_file(character, "output.txt")   # Save as text
CharacterDisplay.export_json(character, "output.json")   # Export as JSON
```

## Available Classes

### Base Classes

| Class | Description | HP Die | Skills | Foci |
|-------|-------------|--------|--------|------|
| Warrior | Combat specialist | 1d6+2 | 3+INT | 1 + combat bonus |
| Expert | Skills specialist | 1d6 | 6+INT | 1 + non-combat bonus |
| Psychic | Psychic powers | 1d6 | 4+INT | 1 |
| Adventurer | Jack of all trades | 1d6+1 | 4+INT | 2 |

### Magic Classes

| Class | Spell Tradition | HP Die | Skills | Foci |
|-------|-----------------|--------|--------|------|
| Arcanist | Arcanist | 1d6 | 3+INT | 1 |
| Pacter | Pacter | 1d6 | 3+INT | 1 |
| Rectifier | Rectifier | 1d6 | 3+INT | 1 |
| War Mage | War Mage | 1d6 | 3+INT | 1 |
| Arcane Expert | — | 1d6 | 6+INT | 1 + non-combat |
| Arcane Warrior | — | 1d6+2 | 3+INT | 1 + combat |

### Special Classes

| Class | Description | HP Die | Skills |
|-------|-------------|--------|--------|
| Free Nexus | Support with symbiosis | 1d6 | 4+INT |
| Godhunter | Shadow hunters | 1d6+2 | 3+INT |
| Sunblade | Warrior-monks | 1d6 | 3+INT |
| Yama King | Wandering judges | 1d6 | 3+INT |

## Project Structure

```
character_generator/
├── README.md                    # This file
├── QUICK_START.md              # Quick reference guide
├── example_usage.py            # Usage examples
├── notebook_examples.py        # Jupyter-friendly examples
├── swn/                        # Main package
│   ├── __init__.py
│   ├── character.py            # Character model
│   ├── generator.py            # Character generation logic
│   ├── display.py              # Display/export functions
│   ├── dice.py                 # Dice rolling utilities
│   ├── data/                   # Game data (JSON)
│   │   ├── backgrounds.json
│   │   ├── classes.json
│   │   ├── foci.json
│   │   ├── skills.json
│   │   ├── psychic_disciplines.json    # 6 disciplines with techniques
│   │   ├── arcanist_spells.json
│   │   ├── pacter_spells.json
│   │   ├── rectifier_spells.json
│   │   ├── war_mage_spells.json
│   │   ├── armor.json                   # NEW: 18 armor types
│   │   ├── weapons.json                 # NEW: 33 weapons
│   │   └── gear.json                    # NEW: 27 gear items
│   └── models/                 # Data models
│       ├── __init__.py
│       ├── attributes.py
│       ├── backgrounds.py
│       ├── classes.py
│       ├── foci.py
│       ├── psychic.py          # Disciplines as skills system
│       ├── skills.py           # Correct skill costs
│       ├── spells.py
│       └── equipment.py        # NEW: Equipment selection
```

## Spell Progression

| Level | Level-1 Spells | Level-2 Spells | Level-3 Spells |
|-------|----------------|----------------|----------------|
| 1 | 4 | — | — |
| 2 | 5 | — | — |
| 3 | 6 | 2 | — |
| 4 | 7 | 3 | — |
| 5+ | 8 | 4 | 2 |

## Tips & Best Practices

### For Balanced Characters
```python
# Use standard array for predictable stats
char = gen.generate_character(attribute_method="array")
```

### For Magic Users
```python
# Always set power_type="magic" for spellcasters
mage = gen.generate_character(
    class_choice="Arcanist",
    power_type="magic"  # Important!
)
```

### Generate Multiple Options
```python
# Generate several characters and pick your favorite
options = [gen.generate_character(class_choice="Warrior") for _ in range(5)]
for i, char in enumerate(options, 1):
    print(f"Option {i}: HP={char.hp}, Skills={len(char.skills.get_all_skills())}")
```

## Troubleshooting

**ImportError: No module named 'swn'**
- Make sure you're running Python from the `character_generator` directory
- The `swn/` folder should be in the same directory

**Characters have no spells**
- For magic classes, set `power_type="magic"`
- Example: `gen.generate_character(class_choice="Arcanist", power_type="magic")`

**Low HP rolls**
- HP is rolled randomly (1d6 + modifiers)
- This is normal! Some characters will have low HP at level 1

## Customization

All game data is stored in JSON files in `swn/data/`. You can:
- Add new backgrounds
- Create custom foci
- Add new psychic disciplines
- Create custom spell lists
- Modify class attributes

Just edit the JSON files to customize your campaign!

## License

This is an unofficial fan project for Stars Without Number.

Stars Without Number is © Kevin Crawford and Sine Nomine Publishing.

This generator is provided for personal, non-commercial use.

## Credits

- **Stars Without Number**: Kevin Crawford (Sine Nomine Publishing)
- **Codex of the Black Sun**: Magic system for SWN
- Character Generator: Built with Python standard library only

## Version

Current Version: 1.0.0

---

**Enjoy creating characters for your Stars Without Number adventures!** 🚀✨
