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
    """Manages known spells for a spellcasting character."""

    def __init__(self, tradition: str):
        """
        Initialize a spell list.

        Args:
            tradition: Spell tradition (Pacter, Rectifier, War Mage, etc.)
        """
        self.tradition = tradition
        self.known_spells: List[Spell] = []

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

    def to_dict(self) -> dict:
        """Convert spell list to dictionary format."""
        return {
            "tradition": self.tradition,
            "spells": [spell.to_dict() for spell in self.known_spells]
        }

    def __str__(self) -> str:
        """Return formatted spell list."""
        if not self.known_spells:
            return "No spells known"

        lines = [f"{self.tradition} Tradition:"]

        # Group by level
        for level in range(1, 6):
            level_spells = self.get_spells_by_level(level)
            if level_spells:
                lines.append(f"\nLevel {level} Spells:")
                for spell in level_spells:
                    lines.append(f"  - {spell.name}")
                    lines.append(f"    {spell.description}")

        return "\n".join(lines)


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

    def get_spells_for_level(self, character_level: int) -> List[Spell]:
        """
        Get appropriate number of spells for a character level.

        Spell progression:
        - Level 1: 4 level-1 spells
        - Level 2: 5 level-1 spells
        - Level 3: 6 level-1 spells + 2 level-2 spells
        - Level 4: 7 level-1 spells + 3 level-2 spells
        - Level 5+: 8 level-1 spells + 4 level-2 spells + 2 level-3 spells

        Args:
            character_level: Character level

        Returns:
            List of selected spells
        """
        spells = []

        # Determine spell counts by level
        spell_counts = {
            1: [(1, 4)],  # 4 level-1 spells
            2: [(1, 5)],  # 5 level-1 spells
            3: [(1, 6), (2, 2)],  # 6 level-1, 2 level-2
            4: [(1, 7), (2, 3)],  # 7 level-1, 3 level-2
            5: [(1, 8), (2, 4), (3, 2)],  # 8 level-1, 4 level-2, 2 level-3
        }

        # For levels above 5, use level 5 progression
        if character_level > 5:
            character_level = 5

        if character_level not in spell_counts:
            character_level = 1

        for spell_level, count in spell_counts[character_level]:
            spell_key = f"level_{spell_level}"
            spell_data = self.spell_data.get(spell_key, [])

            if spell_data:
                # Select random spells from this level
                num_to_select = min(count, len(spell_data))
                selected = random.sample(spell_data, num_to_select)

                for spell_info in selected:
                    spell = Spell(
                        name=spell_info["name"],
                        level=spell_level,
                        description=spell_info["description"]
                    )
                    spells.append(spell)

        return spells

    def create_spell_list(self, character_level: int) -> SpellList:
        """
        Create a complete spell list for a character.

        Args:
            character_level: Character level

        Returns:
            SpellList instance with appropriate spells
        """
        spell_list = SpellList(self.tradition)

        selected_spells = self.get_spells_for_level(character_level)
        for spell in selected_spells:
            spell_list.add_spell(spell)

        return spell_list
