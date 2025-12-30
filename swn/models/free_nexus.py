"""Free Nexus gifts and abilities system."""
import json
import random
from pathlib import Path
from typing import List


class NexusGift:
    """Represents a single Nexus gift."""

    def __init__(self, name: str, description: str):
        """
        Initialize a Nexus gift.

        Args:
            name: Gift name
            description: Gift description
        """
        self.name = name
        self.description = description

    def to_dict(self) -> dict:
        """Convert gift to dictionary format."""
        return {
            "name": self.name,
            "description": self.description
        }

    def __str__(self) -> str:
        """Return formatted gift description."""
        return f"{self.name}: {self.description}"


class FreeNexusAbility:
    """Represents a level 1 automatic ability."""

    def __init__(self, name: str, description: str, level_required: int = 1,
                 automatic: bool = True):
        """
        Initialize a Free Nexus ability.

        Args:
            name: Ability name
            description: Ability description
            level_required: Level required (always 1 for base abilities)
            automatic: Always True for base abilities
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


class FreeNexusAbilitySet:
    """Represents a Free Nexus character's abilities and gifts."""

    def __init__(self, character_level: int, base_abilities: List[FreeNexusAbility],
                 selected_gifts: List[NexusGift]):
        """
        Initialize Free Nexus ability set.

        Args:
            character_level: Character's level
            base_abilities: Level 1 automatic abilities (Symbiosis, Free Nexus Effort)
            selected_gifts: List of Nexus gifts gained
        """
        self.character_level = character_level
        self.base_abilities = base_abilities
        self.selected_gifts = selected_gifts

    def calculate_effort_pool(self, wis_modifier: int, cha_modifier: int) -> int:
        """
        Calculate Free Nexus Effort pool.

        Formula: Number of Nexus gifts + max(WIS, CHA modifier)

        Args:
            wis_modifier: Wisdom modifier
            cha_modifier: Charisma modifier

        Returns:
            Effort pool value
        """
        return len(self.selected_gifts) + max(wis_modifier, cha_modifier)

    def calculate_symbiotic_healing(self) -> str:
        """
        Calculate Symbiotic Healing dice.

        Returns:
            Healing dice string (e.g., "3d6" for level 5-6)
        """
        num_dice = (self.character_level + 1) // 2
        return f"{num_dice}d6"

    def to_dict(self) -> dict:
        """Convert ability set to dictionary format."""
        return {
            "character_level": self.character_level,
            "base_abilities": [ability.to_dict() for ability in self.base_abilities],
            "gifts": [gift.to_dict() for gift in self.selected_gifts]
        }


class FreeNexusGiftSelector:
    """Manages Free Nexus gift selection and loading."""

    def __init__(self, level_1_abilities: List[FreeNexusAbility],
                 available_gifts: List[NexusGift]):
        """
        Initialize gift selector.

        Args:
            level_1_abilities: Automatic level 1 abilities
            available_gifts: Pool of selectable Nexus gifts
        """
        self.level_1_abilities = level_1_abilities
        self.available_gifts = available_gifts

    @classmethod
    def load_from_file(cls, file_path: str) -> 'FreeNexusGiftSelector':
        """
        Load Free Nexus gifts from JSON file.

        Args:
            file_path: Path to free_nexus_gifts.json

        Returns:
            FreeNexusGiftSelector instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Free Nexus gifts file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        # Load level 1 automatic abilities
        level_1_abilities = [
            FreeNexusAbility(
                name=ability["name"],
                description=ability["description"],
                level_required=ability.get("level_required", 1),
                automatic=ability.get("automatic", True)
            )
            for ability in data["level_1_abilities"]
        ]

        # Load available Nexus gifts
        available_gifts = [
            NexusGift(
                name=gift["name"],
                description=gift["description"]
            )
            for gift in data["nexus_gifts"]
        ]

        return cls(level_1_abilities, available_gifts)

    def create_free_nexus_abilities(self, character_level: int) -> FreeNexusAbilitySet:
        """
        Create abilities for a Free Nexus character.

        Free Nexuses gain Nexus gifts at even levels:
        - Level 1: 2 automatic abilities (Symbiosis, Free Nexus Effort)
        - Levels 2, 4, 6, 8, 10: Gain one Nexus gift (5 gifts max at level 10)

        Args:
            character_level: Character's level

        Returns:
            FreeNexusAbilitySet instance
        """
        # All Free Nexuses get level 1 automatic abilities
        base_abilities = list(self.level_1_abilities)

        # Calculate how many gifts they get (one per even level)
        num_gifts = sum(1 for level in [2, 4, 6, 8, 10] if level <= character_level)

        # Randomly select gifts from available pool
        selected_gifts = []
        if num_gifts > 0 and self.available_gifts:
            available = list(self.available_gifts)
            random.shuffle(available)
            selected_gifts = available[:min(num_gifts, len(available))]

        return FreeNexusAbilitySet(
            character_level=character_level,
            base_abilities=base_abilities,
            selected_gifts=selected_gifts
        )
