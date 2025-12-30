"""Yama King abilities system."""
import json
from pathlib import Path
from typing import List


class YamaKingAbility:
    """Represents a single Yama King ability."""

    def __init__(self, name: str, description: str, level_required: int = 1,
                 automatic: bool = False):
        """
        Initialize a Yama King ability.

        Args:
            name: Ability name
            description: Ability description
            level_required: Minimum level to acquire this ability
            automatic: If True, granted automatically at level
        """
        self.name = name
        self.description = description
        self.level_required = level_required
        self.automatic = automatic

    def to_dict(self) -> dict:
        """Convert ability to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "level_required": self.level_required,
            "automatic": self.automatic
        }

    def __str__(self) -> str:
        """Return formatted ability description."""
        return f"{self.name}: {self.description}"


class YamaKingAbilitySet:
    """Represents a Yama King character's abilities."""

    def __init__(self, character_level: int, selected_abilities: List[YamaKingAbility]):
        """
        Initialize Yama King ability set.

        Args:
            character_level: Character's level
            selected_abilities: List of abilities gained
        """
        self.character_level = character_level
        self.selected_abilities = selected_abilities

    def to_dict(self) -> dict:
        """Convert ability set to dictionary format."""
        return {
            "character_level": self.character_level,
            "abilities": [ability.to_dict() for ability in self.selected_abilities]
        }


class YamaKingAbilitySelector:
    """Manages Yama King ability selection and loading."""

    def __init__(self, level_1_abilities: List[YamaKingAbility],
                 level_abilities: List[YamaKingAbility]):
        """
        Initialize ability selector.

        Args:
            level_1_abilities: Automatic level 1 abilities
            level_abilities: Abilities gained at levels 2-10
        """
        self.level_1_abilities = level_1_abilities
        self.level_abilities = level_abilities

    @classmethod
    def load_from_file(cls, file_path: str) -> 'YamaKingAbilitySelector':
        """
        Load Yama King abilities from JSON file.

        Args:
            file_path: Path to yama_king_abilities.json

        Returns:
            YamaKingAbilitySelector instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Yama King abilities file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        # Load level 1 automatic abilities
        level_1_abilities = [
            YamaKingAbility(
                name=ability["name"],
                description=ability["description"],
                level_required=ability.get("level_required", 1),
                automatic=ability.get("automatic", True)
            )
            for ability in data["level_1_abilities"]
        ]

        # Load abilities gained at levels 2-10
        level_abilities = [
            YamaKingAbility(
                name=ability["name"],
                description=ability["description"],
                level_required=ability["level_required"],
                automatic=False
            )
            for ability in data["level_abilities"]
        ]

        return cls(level_1_abilities, level_abilities)

    def create_yama_king_abilities(self, character_level: int) -> YamaKingAbilitySet:
        """
        Create abilities for a Yama King character.

        Yama Kings gain abilities at every level (not just even levels):
        - Level 1: 3 automatic abilities
        - Levels 2-10: Gain abilities specified for that level

        Args:
            character_level: Character's level

        Returns:
            YamaKingAbilitySet instance
        """
        # All Yama Kings get level 1 automatic abilities
        selected = list(self.level_1_abilities)

        # Add abilities for each level reached
        for ability in self.level_abilities:
            if ability.level_required <= character_level:
                selected.append(ability)

        return YamaKingAbilitySet(
            character_level=character_level,
            selected_abilities=selected
        )
