# Stars Without Number Character Generator

A comprehensive Python-based character generator for the Stars Without Number tabletop RPG, supporting both the core rulebook and Codex of the Black Sun magic system.

## Features

✨ **Official SWN Character Creation**
- Follow the exact character creation steps from the core rulebook
- Roll attributes (3d6, pick one to set to 14) or use standard array (14, 12, 11, 10, 9, 7)
- **44 backgrounds**: 20 general + 24 class-specific backgrounds (3 each for 8 specialized classes)
- Special skill resolution: "Any Combat" (Shoot/Stab/Punch), "Any Skill" (random non-psychic skill)
- Level-based character generation (levels 1-10) with proper scaling
- Accurate skill point costs: (new level + 1) per SWN rules
- Level-based skill caps: +1 at levels 1-2, +2 at 3-5, +3 at 6-8, +4 at 9-10

⚔️ **14 Character Classes**
- **Base Classes**: Warrior, Expert, Psychic, Adventurer (power type: normal)
- **Magic Classes**: Arcanist, Pacter, Rectifier, War Mage, Arcane Expert, Arcane Warrior (power type: magic)
- **Special Classes**: Free Nexus ✨*NEW*, Godhunter, Sunblade, Yama King (power type varies)
- Power type automatically set based on class choice
- Free Nexus: Symbiotic support class with 14 Nexus gifts
- Godhunter: Shadow hunters with bonuses vs Shadows
- Sunblade: Warrior-monks with sacred weapons
- Yama King: Wandering judges with social manipulation abilities

🔮 **Magic & Psychic Systems**
- **Spell Traditions**: 4 complete spell lists (Arcanist, Pacter, Rectifier, War Mage) with 30+ spells each
- **Arcanist Tradition** ⚡*UPDATED*: Unlimited spells known, limited prepared per day (differs from other traditions)
  - Levels 1-5: 2-4 spells per level, Levels 6+: 5-8 spells per level
  - Correct spell slots: 1/2/2/3/3/3/4/4/5/5 at levels 1-10 (less than other traditions)
- **Other Traditions**: Limited known spells with more spell slots (standard Magister progression)
- **Psychic Disciplines**: 6 disciplines as individual skills (Biopsionics, Metapsionics, Precognition, Telekinesis, Telepathy, Teleportation)
- Each discipline has a core technique (level-0) and 8-12 advanced techniques (levels 1-4)
- Technique selection: 1 technique learned per skill level increase
- Psychic class gets 2 bonus psychic skill picks (can pick same discipline twice for level-1)
- Effort pool: 1 + highest discipline skill + better of WIS/CON modifier (minimum 1)
- **Arcane Foci**: 27 arcane foci for magic-using characters

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

### Option 1: Interactive Jupyter Notebook ⭐ **Recommended for Beginners**

We provide a comprehensive Jupyter notebook with all options documented and easy variable configuration.

#### Local Jupyter

```bash
# Install Jupyter if needed
pip install jupyter

# Launch the notebook
jupyter notebook character_generator_notebook.ipynb
```

#### Google Colab (No Installation Required!)

You can run this notebook in Google Colab without installing anything:

**Method 1: Upload Files to Colab**
1. Go to [Google Colab](https://colab.research.google.com/)
2. Upload the entire project folder to your Colab session:
   ```python
   from google.colab import files
   import zipfile
   import os

   # Upload the project as a zip file
   uploaded = files.upload()

   # Extract it
   for filename in uploaded.keys():
       with zipfile.ZipFile(filename, 'r') as zip_ref:
           zip_ref.extractall('.')

   # Change to the project directory
   os.chdir('swn_character_generator')
   ```

3. Then run the notebook cells normally!

**Method 2: Clone from GitHub** (if you have it in a repo)
```python
!git clone <your-repo-url>
%cd swn_character_generator
```

**Method 3: Direct Notebook Upload**
1. Go to [Google Colab](https://colab.research.google.com/)
2. File → Upload notebook
3. Upload `character_generator_notebook.ipynb`
4. Add a setup cell at the top to upload the `swn` folder:
   ```python
   from google.colab import files
   import zipfile

   # Upload swn folder as zip
   print("Upload the swn folder as a zip file")
   uploaded = files.upload()

   # Extract swn folder
   with zipfile.ZipFile(list(uploaded.keys())[0], 'r') as zip_ref:
       zip_ref.extractall('.')
   ```

**The notebook includes:**
- **Complete documentation** of all 14 classes, 44 backgrounds, and options
- **Easy configuration section** - just change variables and run
- **Pre-configured examples** for common character types
- **Multiple character generation** examples
- Perfect for learning the system!

### Option 2: Python Script

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

### Option 3: Command Line Quick Test

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
    class_choice="Expert",
    background_choice="Technician"  # Optional: choose specific background
)

CharacterDisplay.print_character(expert)
```

### Magic Characters

```python
# Arcanist (Academic magic tradition)
arcanist = gen.generate_character(
    name="Lyra Arcanum",
    level=2,
    class_choice="Arcanist",
    background_choice="Arcanist Scholar"  # Class-specific background
)

# Pacter (Shadow summoner)
pacter = gen.generate_character(
    name="Shadow Master",
    level=1,
    class_choice="Pacter",
    background_choice="Pacter Dragoman"  # Class-specific background
)

# Power type is automatically set to "magic" for these classes
CharacterDisplay.print_character(arcanist)
```

### Psychic Characters

```python
# Psychic class (gets 2 bonus psychic skill picks)
psychic = gen.generate_character(
    name="Mind Walker",
    level=3,
    class_choice="Psychic"
)
# Psychic class gets 2 bonus psychic skill picks as starting skills
# Can pick same discipline twice for level-1 + free level-1 technique
# Or pick two different disciplines for level-0 each
# Power type automatically set to "psionic"

# Each discipline grants core technique + 1 technique per skill level
# Effort pool: 1 + highest discipline skill + better of WIS/CON mod

CharacterDisplay.print_character(psychic)
```

### Special Class Characters

```python
# Free Nexus (symbiotic support class)
free_nexus = gen.generate_character(
    name="Symbiote",
    level=6,
    class_choice="Free Nexus",
    background_choice="Escaped Familiar"  # Class-specific background
)
# Level 1: Gains Symbiosis and Free Nexus Effort abilities
# Levels 2, 4, 6: Gains 1 Nexus gift each (3 gifts at level 6)
# Effort pool: 3 gifts + max(WIS, CHA modifier)
# Can establish symbiosis with allies to share abilities

# Sunblade (warrior-monk with sacred weapon)
sunblade = gen.generate_character(
    name="Blade Master",
    level=4,
    class_choice="Sunblade",
    background_choice="Sunblade Warrior"  # Class-specific background
)
# Level 1: Gets Sacred Weapon, Sunblade Effort, Radiance
# Levels 2, 4: Gains 1 selectable ability each (5 total at level 4)
# Sacred weapon gets +½ level to hit bonus

# Godhunter (Shadow hunter)
godhunter = gen.generate_character(
    name="Shadow Slayer",
    level=5,
    class_choice="Godhunter",
    background_choice="Godhunter Templar"  # Class-specific background
)
# Gains abilities every level (8 total at level 5)
# Grim Determination: +3 HP at level 5 (odd levels only)
# True Hand: +3 to hit vs Shadows/cultists
# Armor of Contempt: +3 AC vs Shadows/cultists

CharacterDisplay.print_character(free_nexus)
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

# Save as formatted text file (overwrites)
CharacterDisplay.save_to_file(char, "my_hero.txt")

# Save as JSON (overwrites)
CharacterDisplay.export_json(char, "my_hero.json")
```

### Generate Multiple Characters to Review

**NEW in v1.1.0**: Use `append_to_file()` to generate multiple characters to one file, then review and pick your favorites!

```python
# Example 1: Generate 5 warriors and pick the best one
print("Generating 5 Warrior options...")
for i in range(5):
    char = gen.generate_character(level=1, class_choice="Warrior")
    CharacterDisplay.append_to_file(char, "warriors.txt")
    print(f"  {i+1}. {char.name} - HP: {char.hp}, AC: {char.calculate_ac()}")

print("\nAll warriors saved to 'warriors.txt' - open it and pick your favorite!")

# Example 2: Generate party options (3 options per role)
party_roles = ["Warrior", "Expert", "Arcanist", "Psychic"]

for role in party_roles:
    print(f"\nGenerating {role} options:")
    for i in range(3):
        char = gen.generate_character(level=1, class_choice=role)

        # Append to text file (human-readable)
        CharacterDisplay.append_to_file(char, "party_options.txt")

        # Append to JSON file (creates array)
        CharacterDisplay.append_json_to_file(char, "party_options.json")

        print(f"  {i+1}. {char.name} (HP: {char.hp})")

print("\n✅ 12 characters saved!")
print("   Text: party_options.txt (review all options)")
print("   JSON: party_options.json (array for processing)")

# Example 3: Generate and compare characters at different levels
for level in [1, 3, 5, 7, 10]:
    char = gen.generate_character(
        name=f"Level {level} Warrior",
        level=level,
        class_choice="Warrior"
    )
    CharacterDisplay.append_to_file(char, "level_comparison.txt")
    print(f"Level {level}: HP={char.hp}, Attack=+{char.attack_bonus}")
```

**Key Features:**
- `append_to_file()`: Adds character to text file with spacing between characters
- `append_json_to_file()`: Maintains JSON array of characters `[{char1}, {char2}, ...]`
- Perfect for generating multiple options and reviewing them all at once
- Files can be opened in any text editor

### Generate a Party

```python
party = [
    gen.generate_character(name="Tank", class_choice="Warrior", background_choice="Soldier"),
    gen.generate_character(name="Scout", class_choice="Expert", background_choice="Criminal"),
    gen.generate_character(name="Wizard", class_choice="Arcanist", background_choice="Arcanist Scholar"),
    gen.generate_character(name="Face", class_choice="Adventurer", background_choice="Dilettante")
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
    class_choice=None,           # Class name or None for random
    background_choice=None,      # Background name or None for random
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
- **class_choice** (str, optional): Class name or None for random
  - Power type automatically set based on class (normal/magic/psionic)
- **background_choice** (str, optional): Background name or None for random
  - 20 general backgrounds available to all classes
  - 24 class-specific backgrounds (3 each for Arcanist, Free Nexus, Godhunter, Pacter, Rectifier, Sunblade, War Mage, Yama King)
  - Class-specific backgrounds can be used by any class but are thematically designed for specific classes
- **tech_level** (int): Equipment technology level (0-5), default 4
  - TL0: Stone age (hide armor, clubs, bows)
  - TL1-2: Medieval to Renaissance (plate armor, firearms)
  - TL3: Industrial (combat rifles, woven armor)
  - TL4: Standard spacefaring (energy weapons, vacc suits)
  - TL5: Pretech/Mandate-era (powered armor, advanced energy weapons)

### CharacterDisplay Methods

```python
# Display to console
CharacterDisplay.print_character(character)

# Save single character (overwrites file)
CharacterDisplay.save_to_file(character, "output.txt")
CharacterDisplay.export_json(character, "output.json")

# Append multiple characters (NEW in v1.1.0)
CharacterDisplay.append_to_file(character, "output.txt")          # Append to text file
CharacterDisplay.append_json_to_file(character, "output.json")    # Append to JSON array
```

**Method Details:**

- **`print_character(character)`**: Prints formatted character sheet to console
- **`save_to_file(character, filename)`**: Saves single character to text file (overwrites)
- **`export_json(character, filename)`**: Exports single character as JSON (overwrites)
- **`append_to_file(character, filename)`** ✨*NEW*: Appends character to text file with spacing
  - First call creates file, subsequent calls append
  - Automatically adds separators between characters
  - Perfect for generating multiple options to review
- **`append_json_to_file(character, filename)`** ✨*NEW*: Appends character to JSON array
  - Maintains array structure: `[{char1}, {char2}, ...]`
  - First call creates array, subsequent calls add to it
  - Great for batch processing or data analysis

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

| Class | Description | HP Die | Skills | Special Abilities |
|-------|-------------|--------|--------|-------------------|
| Free Nexus | Support with symbiosis | 1d6 | 4+INT | Gains Nexus gifts at even levels (2, 4, 6, 8, 10) |
| Godhunter | Shadow hunters | 1d6+2 | 3+INT | Gains abilities every level, bonuses vs Shadows |
| Sunblade | Warrior-monks | 1d6 | 3+INT | Sacred weapon, gains abilities at even levels |
| Yama King | Wandering judges | 1d6 | 3+INT | Gains abilities every level, social manipulation |

#### Free Nexus Details
- **Level 1**: 2 base abilities (Symbiosis, Free Nexus Effort)
- **Levels 2, 4, 6, 8, 10**: Gain 1 Nexus gift each (5 total at level 10)
- **Effort Pool**: Number of gifts + max(WIS, CHA modifier)
- **Symbiotic Healing**: Scales with level (1d6 per 2 levels, rounded up)
- **14 Nexus Gifts**: Arcane Battery, Borrowed Brilliance, Cognitive Backup, Diffuse Strain, Distributed War Mind, Distributive Action, Full Override, Group Symbiosis, Psychic Battery, Red Well, Reflexive Action, Shared Mind, Symbiotic Healing, Two Minds One Flesh

#### Godhunter Details
- **Level 1**: 3 base abilities (Grim Determination, True Hand, Armor of Contempt)
- **Levels 2-10**: Gain abilities specified for each level
- **Grim Determination**: +1 HP at odd levels (1, 3, 5, 7, 9)
- **True Hand**: +½ level to hit vs Shadows/cultists
- **13 Total Abilities** at level 10

#### Sunblade Details
- **Level 1**: 3 automatic abilities (Sacred Weapon, Sunblade Effort, Radiance)
- **Levels 2, 4, 6, 8, 10**: Gain 1 selectable ability each (8 total at level 10)
- **Sacred Weapon**: Chosen melee weapon with special properties
- **Effort Pool**: Number of abilities + max(WIS, CHA modifier)
- **Hit Bonus**: +½ level with sacred weapon

#### Yama King Details
- **Level 1**: 3 base abilities (Passport of Hell, Uncanny Bargain, Tallies Thrown Down)
- **Levels 2-10**: Gain abilities specified for each level
- **13 Total Abilities** at level 10
- Specializes in social manipulation, judgment, and execution attacks

## Available Backgrounds

### General Backgrounds (20)

Available to all classes. Each background provides a Free Skill (level -1) and 3 Quick Skills to choose from (level 0).

| Background | Free Skill | Quick Skills |
|------------|------------|--------------|
| Barbarian | Survive | Survive, Notice, Any Combat |
| Clergy | Talk | Talk, Perform, Know |
| Courtesan | Perform | Perform, Notice, Connect |
| Criminal | Sneak | Sneak, Connect, Talk |
| Dilettante | Connect | Connect, Know, Talk |
| Entertainer | Perform | Perform, Talk, Connect |
| Merchant | Trade | Trade, Talk, Connect |
| Noble | Lead | Lead, Connect, Administer |
| Official | Administer | Administer, Talk, Connect |
| Peasant | Exert | Exert, Sneak, Survive |
| Physician | Heal | Heal, Know, Notice |
| Pilot | Pilot | Pilot, Fix, Shoot |
| Politician | Talk | Talk, Lead, Connect |
| Scholar | Know | Know, Connect, Administer |
| Soldier | Any Combat | Any Combat, Exert, Survive |
| Spacer | Fix | Fix, Pilot, Program |
| Technician | Fix | Fix, Exert, Notice |
| Thug | Any Combat | Any Combat, Talk, Connect |
| Vagabond | Survive | Survive, Sneak, Notice |
| Worker | Work | Connect, Exert, Work |

**Special Skill Placeholders:**
- **Any Combat**: Resolves to Shoot, Stab, or Punch (randomly selected)
- **Any Skill**: Resolves to any random non-psychic skill

### Class-Specific Backgrounds (24)

These backgrounds are thematically designed for specific classes but can be used by any class.

#### Arcanist Backgrounds (3)
| Background | Free Skill | Quick Skills | Description |
|------------|------------|--------------|-------------|
| Arcanist Scholar | Know Magic | Know Magic, Know, Notice | Bookish wizard dedicated to magical scholarship |
| Hirespell | Cast Magic | Cast Magic, Trade, Any Combat | Mercenary wizard who hires out magical talents |
| Government Mage | Connect | Connect, Administer, Work | Arcanist employed by government or civil authority |

#### Free Nexus Backgrounds (3)
| Background | Free Skill | Quick Skills | Description |
|------------|------------|--------------|-------------|
| Arcane Muse | Talk | Talk, Perform, Connect | Hired experience provider capable of granting impossible encounters |
| Escaped Familiar | Any Skill | Any Skill, Sneak, Notice | Former property who escaped their master's control |
| Occult Proxy | Exert | Exert, Notice, Sneak | Professional helper who goes to dangerous places for employers |

#### Godhunter Backgrounds (3)
| Background | Free Skill | Quick Skills | Description |
|------------|------------|--------------|-------------|
| Godhunter Inquisitor | Notice | Notice, Talk, Connect | Trained in sniffing out Shadow cults and heresy |
| Godhunter Templar | Any Combat | Any Combat, Exert, Notice | Consecrated to war against Shadows |
| Vengeful Renegade | Any Combat | Any Combat, Any Skill, Connect | Former cult member using knowledge as weapon |

#### Pacter Backgrounds (3)
| Background | Free Skill | Quick Skills | Description |
|------------|------------|--------------|-------------|
| Pacter Chosen | Cast Magic | Cast Magic, Work, Notice | Received powers through non-traditional means |
| Pacter Controller | Cast Magic | Cast Magic, Lead, Exert | Specializes in summoning and controlling Shadows |
| Pacter Dragoman | Cast Magic | Cast Magic, Talk, Know Magic | Diplomat specializing in negotiating with Shadows |

#### Rectifier Backgrounds (3)
| Background | Free Skill | Quick Skills | Description |
|------------|------------|--------------|-------------|
| Amender of Flesh | Cast Magic | Cast Magic, Heal, Connect | Healer who corrects deformities and alters bodily forms |
| Identity Artist | Cast Magic | Cast Magic, Connect, Talk | Seeks enlightenment through changing physical form |
| Vessel of Will | Cast Magic | Cast Magic, Exert, Survive | Uses arcane arts to hone body as tool for will |

#### Sunblade Backgrounds (3)
| Background | Free Skill | Quick Skills | Description |
|------------|------------|--------------|-------------|
| Sunblade Mystic | Sunblade | Sunblade, Talk, Know | Spiritual guide embracing mysteries and seeking peaceful resolution |
| Sunblade Warrior | Sunblade | Sunblade, Any Combat, Exert | Warrior consecrated to the sword with ancient martial training |
| Sunblade Burnout | Sunblade | Sunblade, Connect, Any Skill | Former member who departed the order, living on society's edge |

#### War Mage Backgrounds (3)
| Background | Free Skill | Quick Skills | Description |
|------------|------------|--------------|-------------|
| War Mage Veteran | Cast Magic | Cast Magic, Any Combat, Exert | Combat veteran who served on front lines with magical abilities |
| War Mage Officer | Cast Magic | Cast Magic, Any Combat, Lead | Former military leader who coordinated soldiers in battle |
| War Mage Rebel | Cast Magic | Cast Magic, Sneak, Any Combat | Independent War Mage outside standing military forces |

#### Yama King Backgrounds (3)
| Background | Free Skill | Quick Skills | Description |
|------------|------------|--------------|-------------|
| Accountant of Life and Death | Notice | Notice, Talk, Connect | Investigator and judge trained in discernment and adjudication |
| Celestial Loss Preventer | Talk | Talk, Connect, Trade | Diplomat and negotiator salvaging bad situations |
| Devil's Incense | Any Combat | Any Combat, Sneak, Connect | Infiltrator trained in social assassination and execution |

## Project Structure

```
character_generator/
├── README.md                           # This file
├── QUICK_START.md                      # Quick reference guide
├── character_generator_notebook.ipynb  # ⭐ Interactive Jupyter notebook (NEW!)
├── example_usage.py                    # Usage examples
├── notebook_examples.py                # Jupyter-friendly examples
├── swn/                                # Main package
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
│   │   ├── arcanist_spells.json        # Academic magic tradition
│   │   ├── pacter_spells.json          # Shadow summoning tradition
│   │   ├── rectifier_spells.json       # Transformation tradition
│   │   ├── war_mage_spells.json        # Tactical magic tradition
│   │   ├── sunblade_abilities.json     # Sunblade special abilities
│   │   ├── yama_king_abilities.json    # Yama King special abilities
│   │   ├── godhunter_abilities.json    # Godhunter special abilities
│   │   ├── free_nexus_gifts.json       # Free Nexus gifts & abilities
│   │   ├── armor.json                  # 18 armor types
│   │   ├── weapons.json                # 33 weapons
│   │   └── gear.json                   # 27 gear items
│   └── models/                 # Data models
│       ├── __init__.py
│       ├── attributes.py
│       ├── backgrounds.py
│       ├── classes.py
│       ├── foci.py
│       ├── psychic.py          # Disciplines as skills system
│       ├── skills.py           # Correct skill costs
│       ├── spells.py           # Spell system with Arcanist/Magister progressions
│       ├── equipment.py        # Equipment selection system
│       ├── sunblade.py         # Sunblade abilities
│       ├── yama_king.py        # Yama King abilities
│       ├── godhunter.py        # Godhunter abilities
│       └── free_nexus.py       # Free Nexus gifts & abilities
```

## Spell Progression

### Magister Traditions (Pacter, Rectifier, War Mage)

These traditions use the standard Magister progression with limited known spells and spell slots:

| Level | L1 Known/Slots | L2 Known/Slots | L3 Known/Slots | L4 Known/Slots | L5 Known/Slots |
|-------|----------------|----------------|----------------|----------------|----------------|
| 1 | 2 / 3 | — | — | — | — |
| 2 | 2 / 4 | — | — | — | — |
| 3 | 3 / 5 | 2 / 2 | — | — | — |
| 4 | 3 / 6 | 2 / 3 | — | — | — |
| 5 | 4 / 6 | 2 / 3 | 2 / 2 | — | — |
| 6 | 4 / 6 | 3 / 4 | 2 / 3 | — | — |
| 7 | 5 / 6 | 3 / 4 | 2 / 3 | 2 / 2 | — |
| 8 | 5 / 6 | 4 / 5 | 3 / 4 | 2 / 3 | — |
| 9 | 5 / 6 | 4 / 5 | 3 / 4 | 3 / 3 | 2 / 2 |
| 10+ | 5 / 6 | 4 / 6 | 3 / 5 | 3 / 4 | 2 / 3 |

### Arcanist Tradition

Arcanists use a unique progression where they can learn **unlimited spells** but can only **prepare a limited number per day**:

**Prepared Spells per Day:**

| Level | L1 | L2 | L3 | L4 | L5 |
|-------|----|----|----|----|-----|
| 1 | 1 | — | — | — | — |
| 2 | 2 | — | — | — | — |
| 3 | 2 | 1 | — | — | — |
| 4 | 3 | 2 | — | — | — |
| 5 | 3 | 2 | 1 | — | — |
| 6 | 3 | 3 | 2 | — | — |
| 7 | 4 | 3 | 2 | 1 | — |
| 8 | 4 | 3 | 3 | 2 | — |
| 9 | 5 | 4 | 3 | 2 | 1 |
| 10+ | 5 | 4 | 3 | 3 | 2 |

**Spells Known (Generated):**
- Levels 1-5: 2-4 spells per level (similar to Magister)
- Levels 6+: 5-8 spells per level (extensive spell library)
- No hard limit on total spells that can be learned

**Key Differences:**
- **Arcanist**: FEWER prepared slots but MANY MORE spells known
- **Other Traditions**: MORE spell slots but LIMITED spells known
- Arcanists must prepare their daily spells from their larger spell library each day

## Tips & Best Practices

### For Balanced Characters
```python
# Use standard array for predictable stats
char = gen.generate_character(attribute_method="array")
```

### For Class-Specific Characters
```python
# Use class-specific backgrounds for thematic characters
arcanist = gen.generate_character(
    class_choice="Arcanist",
    background_choice="Arcanist Scholar"  # Thematic background
)

# Or use general backgrounds for variety
godhunter = gen.generate_character(
    class_choice="Godhunter",
    background_choice="Soldier"  # General background works too
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
- Make sure you're using a magic class (Arcanist, Pacter, Rectifier, War Mage, etc.)
- Power type is automatically set based on class choice
- Spells are only granted to classes with `is_spellcaster=True`

**Psychic class has no psychic powers**
- Psychic class automatically gets 2 bonus psychic skill picks
- Power type is automatically set to "psionic" for Psychic class
- Psychic powers are generated based on discipline skills

**Background not found**
- Check spelling of background name (case-insensitive)
- Use `gen.backgrounds.get_all_background_names()` to see all available backgrounds
- General backgrounds (20) work with all classes
- Class-specific backgrounds (24) are thematic but work with any class

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

## Version & Recent Updates

Current Version: 1.1.0

### Version 1.1.0 (Latest)
**Free Nexus Class Implementation**
- ✅ Added complete Free Nexus class with symbiotic abilities
- 2 base abilities at level 1 (Symbiosis, Free Nexus Effort)
- 14 Nexus gifts gained at even levels (2, 4, 6, 8, 10)
- Effort pool calculation: Number of gifts + max(WIS, CHA modifier)
- Symbiotic Healing scales with level (1d6 per 2 levels)
- 3 class-specific backgrounds (Arcane Muse, Escaped Familiar, Occult Proxy)

**Arcanist Spell Progression Fix**
- ✅ Fixed Arcanist to use correct spell slot progression
- Changed from Magister progression (6/5/4/3 slots) to Arcanist progression (4/3/3/2 slots)
- Arcanists now can learn many more spells but prepare fewer per day
- Levels 1-5: 2-4 spells known per level
- Levels 6+: 5-8 spells known per level (extensive spell library)
- Properly reflects "unlimited spells known, limited prepared" mechanic

**Append Functions for Multiple Character Generation**
- ✅ Added `append_to_file()` method to CharacterDisplay
- ✅ Added `append_json_to_file()` method to CharacterDisplay
- Generate multiple characters to one file for easy review
- `append_to_file()`: Appends formatted character sheets to text file with spacing
- `append_json_to_file()`: Maintains JSON array of characters `[{char1}, {char2}, ...]`
- Perfect workflow: Generate 5+ options, review them all, pick your favorite!

**Interactive Jupyter Notebook**
- ✅ Added `character_generator_notebook.ipynb`
- Complete documentation of all 14 classes and 44 backgrounds
- Easy variable configuration section - just change and run
- Pre-configured examples for common character types
- Perfect for beginners and learning the system
- Includes multiple character generation examples

### Version 1.0.0
- Initial release with 14 character classes
- Complete equipment system with tech levels 0-5
- Psychic disciplines, spell traditions, and special class abilities
- 44 backgrounds (20 general + 24 class-specific)
- Sunblade, Yama King, and Godhunter special classes

---

**Enjoy creating characters for your Stars Without Number adventures!** 🚀✨
