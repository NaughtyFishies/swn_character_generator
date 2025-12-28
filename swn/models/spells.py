"""Spell system for spellcasting classes."""
import json
import random
from pathlib import Path
from typing import List, Dict


class Spell:
    """Represents a single spell."""

    def __init__(self, name: str, level: int, description: str):
        """
        Initialize a spell.

        Args:
            name: Spell name
            level: Spell level (1-5)
            description: Spell description
        """
        self.name = name
        self.level = level
        self.description = description

    def to_dict(self) -> dict:
        """Convert spell to dictionary format."""
        return {
            "name": self.name,
            "level": self.level,
            "description": self.description
        }

    def __str__(self) -> str:
        """Return formatted spell description."""
        return f"   {self.name} (Level {self.level})\n      {self.description}"


class SpellList:
    """Manages known spells and spell slots for a spellcasting character."""

    def __init__(self, tradition: str):
        """
        Initialize a spell list.

        Args:
            tradition: Spell tradition (Pacter, Rectifier, War Mage, etc.)
        """
        self.tradition = tradition
        self.known_spells: List[Spell] = []
        self.spell_slots: Dict[int, int] = {}  # spell level -> number of slots

    def add_spell(self, spell: Spell):
        """
        Add a spell to the known spells list.

        Args:
            spell: Spell to add
        """
        if spell not in self.known_spells:
            self.known_spells.append(spell)

    def get_spells_by_level(self, level: int) -> List[Spell]:
        """
        Get all spells of a given level.

        Args:
            level: Spell level

        Returns:
            List of spells at that level
        """
        return [s for s in self.known_spells if s.level == level]

    def set_spell_slots(self, level: int, slots: int):
        """
        Set the number of spell slots for a given spell level.

        Args:
            level: Spell level (1-5)
            slots: Number of spell slots
        """
        self.spell_slots[level] = slots

    def get_spell_slots(self, level: int) -> int:
        """
        Get the number of spell slots for a given spell level.

        Args:
            level: Spell level (1-5)

        Returns:
            Number of spell slots (0 if none)
        """
        return self.spell_slots.get(level, 0)

    def to_dict(self) -> dict:
        """Convert spell list to dictionary format."""
        return {
            "tradition": self.tradition,
            "spells": [spell.to_dict() for spell in self.known_spells],
            "spell_slots": self.spell_slots
        }

    def __str__(self) -> str:
        """Return formatted spell list."""
        if not self.known_spells:
            return "No spells known"

        lines = [f"{self.tradition} Tradition:"]

        # Show spell slots per level
        if self.spell_slots:
            lines.append("\nSpell Slots per Day:")
            for level in range(1, 6):
                slots = self.spell_slots.get(level, 0)
                if slots > 0:
                    level_spells = self.get_spells_by_level(level)
                    lines.append(f"  Level {level}: {len(level_spells)} known / {slots} slots")
            lines.append("")

        # Group spells by level
        for level in range(1, 6):
            level_spells = self.get_spells_by_level(level)
            if level_spells:
                lines.append(f"Level {level} Spells Known:")
                for spell in level_spells:
                    lines.append(f"  - {spell.name}")
                    lines.append(f"    {spell.description}")
                lines.append("")

        return "\n".join(lines)


def get_spell_progression(character_level: int) -> Dict[int, Dict[str, int]]:
    """
    Get spell progression for Magister spellcasters.

    Returns dictionary mapping spell level to {known, slots}.
    Format: {1: {"known": 2, "slots": 3}, 2: {"known": 0, "slots": 0}, ...}

    Progression table (Magister):
    Level  L1    L2    L3    L4    L5
    1      2/3   -     -     -     -
    2      2/4   -     -     -     -
    3      3/5   2/2   -     -     -
    4      3/6   2/3   -     -     -
    5      4/6   2/3   2/2   -     -
    6      4/6   3/4   2/3   -     -
    7      5/6   3/4   2/3   2/2   -
    8      5/6   4/5   3/4   2/3   -
    9      5/6   4/5   3/4   3/3   2/2
    10+    5/6   4/6   3/5   3/4   2/3

    Args:
        character_level: Character level

    Returns:
        Dictionary of spell level -> {known, slots}
    """
    progression_table = {
        1:  {1: {"known": 2, "slots": 3}},
        2:  {1: {"known": 2, "slots": 4}},
        3:  {1: {"known": 3, "slots": 5}, 2: {"known": 2, "slots": 2}},
        4:  {1: {"known": 3, "slots": 6}, 2: {"known": 2, "slots": 3}},
        5:  {1: {"known": 4, "slots": 6}, 2: {"known": 2, "slots": 3}, 3: {"known": 2, "slots": 2}},
        6:  {1: {"known": 4, "slots": 6}, 2: {"known": 3, "slots": 4}, 3: {"known": 2, "slots": 3}},
        7:  {1: {"known": 5, "slots": 6}, 2: {"known": 3, "slots": 4}, 3: {"known": 2, "slots": 3}, 4: {"known": 2, "slots": 2}},
        8:  {1: {"known": 5, "slots": 6}, 2: {"known": 4, "slots": 5}, 3: {"known": 3, "slots": 4}, 4: {"known": 2, "slots": 3}},
        9:  {1: {"known": 5, "slots": 6}, 2: {"known": 4, "slots": 5}, 3: {"known": 3, "slots": 4}, 4: {"known": 3, "slots": 3}, 5: {"known": 2, "slots": 2}},
        10: {1: {"known": 5, "slots": 6}, 2: {"known": 4, "slots": 6}, 3: {"known": 3, "slots": 5}, 4: {"known": 3, "slots": 4}, 5: {"known": 2, "slots": 3}},
    }

    # Levels 10+ use the same progression as level 10
    if character_level >= 10:
        character_level = 10

    return progression_table.get(character_level, {1: {"known": 2, "slots": 3}})


class SpellSelector:
    """Manages spell selection for spellcasting classes."""

    def __init__(self, tradition: str, spell_data: Dict):
        """
        Initialize spell selector.

        Args:
            tradition: Spell tradition name
            spell_data: Dictionary of spells by level
        """
        self.tradition = tradition
        self.spell_data = spell_data

    @classmethod
    def load_from_file(cls, tradition: str, file_path: str) -> 'SpellSelector':
        """
        Load spells from JSON file.

        Args:
            tradition: Spell tradition name
            file_path: Path to spell JSON file

        Returns:
            SpellSelector instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Spell file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        return cls(tradition, data["spells"])

    def create_spell_list(self, character_level: int) -> SpellList:
        """
        Create a complete spell list for a character based on Magister progression.

        Args:
            character_level: Character level

        Returns:
            SpellList instance with appropriate spells and spell slots
        """
        spell_list = SpellList(self.tradition)

        # Get spell progression for this level
        progression = get_spell_progression(character_level)

        # For each spell level in the progression
        for spell_level, counts in progression.items():
            known = counts["known"]
            slots = counts["slots"]

            # Set spell slots
            spell_list.set_spell_slots(spell_level, slots)

            # Select known spells
            spell_key = f"level_{spell_level}"
            available_spells = self.spell_data.get(spell_key, [])

            if available_spells and known > 0:
                num_to_select = min(known, len(available_spells))
                selected = random.sample(available_spells, num_to_select)

                for spell_info in selected:
                    spell = Spell(
                        name=spell_info["name"],
                        level=spell_level,
                        description=spell_info["description"]
                    )
                    spell_list.add_spell(spell)

        return spell_list
