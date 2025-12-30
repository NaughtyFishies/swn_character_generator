"""Godhunter abilities system."""
import json
from pathlib import Path
from typing import List


class GodhunterAbility:
    """Represents a single Godhunter ability."""

    def __init__(self, name: str, description: str, level_required: int = 1,
                 automatic: bool = False, hp_bonus: int = 0):
        """
        Initialize a Godhunter ability.

        Args:
            name: Ability name
            description: Ability description
            level_required: Minimum level to acquire this ability
            automatic: If True, granted automatically at level
            hp_bonus: HP bonus per odd level if ability grants it
        """
        self.name = name
        self.description = description
        self.level_required = level_required
        self.automatic = automatic
        self.hp_bonus = hp_bonus

    def to_dict(self) -> dict:
        """Convert ability to dictionary format."""
        result = {
            "name": self.name,
            "description": self.description,
            "level_required": self.level_required,
            "automatic": self.automatic
        }
        if self.hp_bonus:
            result["hp_bonus"] = self.hp_bonus
        return result

    def __str__(self) -> str:
        """Return formatted ability description."""
        return f"{self.name}: {self.description}"


class GodhunterAbilitySet:
    """Represents a Godhunter character's abilities."""

    def __init__(self, character_level: int, selected_abilities: List[GodhunterAbility]):
        """
        Initialize Godhunter ability set.

        Args:
            character_level: Character's level
            selected_abilities: List of abilities gained
        """
        self.character_level = character_level
        self.selected_abilities = selected_abilities

    def calculate_true_hand_bonus(self) -> int:
        """
        Calculate True Hand hit bonus against Shadows.

        Returns:
            Half character level, rounded up
        """
        return (self.character_level + 1) // 2

    def calculate_armor_of_contempt_bonus(self) -> int:
        """
        Calculate Armor of Contempt AC bonus against Shadows.

        Returns:
            Half character level, rounded up
        """
        return (self.character_level + 1) // 2

    def calculate_sacrilegious_scorn_bonus(self) -> int:
        """
        Calculate Sacrilegious Scorn saving throw bonus.

        Returns:
            +2 at levels 2-5, +4 at level 6+
        """
        if self.character_level >= 6:
            return 4
        elif self.character_level >= 2:
            return 2
        return 0

    def calculate_grim_determination_bonus(self) -> int:
        """
        Calculate Grim Determination HP bonus.

        Returns:
            +1 HP per odd level (1, 3, 5, 7, 9)
        """
        odd_levels = [1, 3, 5, 7, 9]
        return sum(1 for level in odd_levels if level <= self.character_level)

    def calculate_righteous_fire_damage(self) -> int:
        """
        Calculate Righteous Fire damage bonus.

        Returns:
            Character level
        """
        return self.character_level

    def to_dict(self) -> dict:
        """Convert ability set to dictionary format."""
        return {
            "character_level": self.character_level,
            "abilities": [ability.to_dict() for ability in self.selected_abilities]
        }


class GodhunterAbilitySelector:
    """Manages Godhunter ability selection and loading."""

    def __init__(self, level_1_abilities: List[GodhunterAbility],
                 level_abilities: List[GodhunterAbility]):
        """
        Initialize ability selector.

        Args:
            level_1_abilities: Automatic level 1 abilities
            level_abilities: Abilities gained at levels 2-10
        """
        self.level_1_abilities = level_1_abilities
        self.level_abilities = level_abilities

    @classmethod
    def load_from_file(cls, file_path: str) -> 'GodhunterAbilitySelector':
        """
        Load Godhunter abilities from JSON file.

        Args:
            file_path: Path to godhunter_abilities.json

        Returns:
            GodhunterAbilitySelector instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Godhunter abilities file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        # Load level 1 automatic abilities
        level_1_abilities = [
            GodhunterAbility(
                name=ability["name"],
                description=ability["description"],
                level_required=ability.get("level_required", 1),
                automatic=ability.get("automatic", True),
                hp_bonus=ability.get("hp_bonus", 0)
            )
            for ability in data["level_1_abilities"]
        ]

        # Load abilities gained at levels 2-10
        level_abilities = [
            GodhunterAbility(
                name=ability["name"],
                description=ability["description"],
                level_required=ability["level_required"],
                automatic=False,
                hp_bonus=ability.get("hp_bonus", 0)
            )
            for ability in data["level_abilities"]
        ]

        return cls(level_1_abilities, level_abilities)

    def create_godhunter_abilities(self, character_level: int) -> GodhunterAbilitySet:
        """
        Create abilities for a Godhunter character.

        Godhunters gain abilities at multiple levels:
        - Level 1: 3 automatic abilities
        - Levels 2-10: Gain abilities specified for that level

        Args:
            character_level: Character's level

        Returns:
            GodhunterAbilitySet instance
        """
        # All Godhunters get level 1 automatic abilities
        selected = list(self.level_1_abilities)

        # Add abilities for each level reached
        for ability in self.level_abilities:
            if ability.level_required <= character_level:
                selected.append(ability)

        return GodhunterAbilitySet(
            character_level=character_level,
            selected_abilities=selected
        )
