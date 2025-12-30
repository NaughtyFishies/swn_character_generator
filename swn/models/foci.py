"""Foci system for SWN characters."""
import json
import random
from pathlib import Path
from typing import List


class Focus:
    """Represents a single character focus."""

    def __init__(self, name: str, tier: str, level_1: str, level_2: str,
                 incompatible_with: List[str] = None, psychic_only: bool = False,
                 arcane_expert_only: bool = False, arcane_warrior_only: bool = False,
                 allowed_classes: List[str] = None):
        """
        Initialize a focus.

        Args:
            name: Focus name
            tier: Focus tier (basic, advanced, exotic)
            level_1: Level 1 benefit description
            level_2: Level 2 benefit description
            incompatible_with: List of incompatible focus names
            psychic_only: Whether this focus requires psychic powers
            arcane_expert_only: Whether this focus is only for Arcane Experts (deprecated)
            arcane_warrior_only: Whether this focus is only for Arcane Warriors (deprecated)
            allowed_classes: List of class names that can take this focus (None = any class)
        """
        self.name = name
        self.tier = tier
        self.level_1 = level_1
        self.level_2 = level_2
        self.incompatible_with = incompatible_with or []
        self.psychic_only = psychic_only
        self.arcane_expert_only = arcane_expert_only  # Deprecated but kept for compatibility
        self.arcane_warrior_only = arcane_warrior_only  # Deprecated but kept for compatibility
        self.allowed_classes = allowed_classes
        self.level = 1  # Characters start with level 1 foci

    def is_compatible_with(self, other_focus: 'Focus') -> bool:
        """
        Check if this focus is compatible with another.

        Args:
            other_focus: Focus to check compatibility with

        Returns:
            True if compatible
        """
        if self.name == other_focus.name:
            return False  # Can't have the same focus twice
        if other_focus.name in self.incompatible_with:
            return False
        if self.name in other_focus.incompatible_with:
            return False
        return True

    def is_truly_incompatible_with(self, other_focus: 'Focus') -> bool:
        """
        Check if this focus is truly incompatible (excluding same-name check).
        Used for leveling up foci.

        Args:
            other_focus: Focus to check compatibility with

        Returns:
            False if incompatible (returns opposite of is_compatible for consistency)
        """
        if other_focus.name in self.incompatible_with:
            return False
        if self.name in other_focus.incompatible_with:
            return False
        return True

    def to_dict(self) -> dict:
        """Convert focus to dictionary format."""
        return {
            "name": self.name,
            "tier": self.tier,
            "level": self.level,
            "level_1": self.level_1,
            "level_2": self.level_2
        }

    def __str__(self) -> str:
        """Return formatted focus description."""
        benefit = self.level_1 if self.level == 1 else f"{self.level_1}\n   {self.level_2}"
        return f"{self.name}\n   {benefit}"


class FociSelector:
    """Manages focus selection and filtering."""

    def __init__(self, foci: List[Focus]):
        """
        Initialize foci selector.

        Args:
            foci: List of all available foci
        """
        self.foci = foci

    @classmethod
    def load_from_file(cls, file_path: str) -> 'FociSelector':
        """
        Load foci from JSON file.

        Args:
            file_path: Path to foci JSON file

        Returns:
            FociSelector instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Foci file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        foci = [
            Focus(
                name=focus_data["name"],
                tier=focus_data["tier"],
                level_1=focus_data["level_1"],
                level_2=focus_data["level_2"],
                incompatible_with=focus_data.get("incompatible_with", []),
                psychic_only=focus_data.get("psychic_only", False),
                arcane_expert_only=focus_data.get("arcane_expert_only", False),
                arcane_warrior_only=focus_data.get("arcane_warrior_only", False),
                allowed_classes=focus_data.get("allowed_classes", None)
            )
            for focus_data in data["foci"]
        ]

        return cls(foci)

    def filter_by_power_level(self, power_level: str) -> List[Focus]:
        """
        Filter foci by power level.

        Args:
            power_level: "weak", "normal", or "strong"

        Returns:
            List of available foci for this power level
        """
        if power_level == "weak":
            return [f for f in self.foci if f.tier == "basic"]
        elif power_level == "normal":
            return [f for f in self.foci if f.tier in ["basic", "advanced"]]
        else:  # strong
            return self.foci  # All tiers available

    def select_random_foci(self, count: int, power_level: str = "normal",
                          has_psychic: bool = False, character_class: str = None) -> List[Focus]:
        """
        Select random compatible foci.

        Args:
            count: Number of foci to select
            power_level: Character power level
            has_psychic: Whether character has psychic powers
            character_class: Character's class name for class-exclusive foci

        Returns:
            List of selected foci
        """
        available = self.filter_by_power_level(power_level)

        # Filter out psychic-only foci if character isn't psychic
        if not has_psychic:
            available = [f for f in available if not f.psychic_only]

        # Filter based on class-exclusive foci
        if character_class:
            filtered = []
            for f in available:
                # Check new allowed_classes system first
                if f.allowed_classes is not None:
                    if character_class not in f.allowed_classes:
                        continue
                # Backwards compatibility with deprecated flags
                elif f.arcane_expert_only and character_class != "Arcane Expert":
                    continue
                elif f.arcane_warrior_only and character_class != "Arcane Warrior":
                    continue
                filtered.append(f)
            available = filtered

        if len(available) < count:
            count = len(available)

        selected = []
        max_attempts = 100
        attempts = 0

        while len(selected) < count and attempts < max_attempts:
            attempts += 1

            # Pick a random focus from available
            candidate = random.choice(available)

            # Check if compatible with already selected foci
            compatible = all(candidate.is_compatible_with(f) for f in selected)

            if compatible:
                # Create a new Focus instance to avoid sharing references
                new_focus = Focus(
                    name=candidate.name,
                    tier=candidate.tier,
                    level_1=candidate.level_1,
                    level_2=candidate.level_2,
                    incompatible_with=candidate.incompatible_with,
                    psychic_only=candidate.psychic_only,
                    arcane_expert_only=candidate.arcane_expert_only,
                    arcane_warrior_only=candidate.arcane_warrior_only,
                    allowed_classes=candidate.allowed_classes
                )
                selected.append(new_focus)

        return selected

    def get_focus_by_name(self, name: str) -> Focus:
        """
        Get a specific focus by name.

        Args:
            name: Focus name

        Returns:
            Focus instance

        Raises:
            ValueError if focus not found
        """
        for focus in self.foci:
            if focus.name.lower() == name.lower():
                return Focus(
                    name=focus.name,
                    tier=focus.tier,
                    level_1=focus.level_1,
                    level_2=focus.level_2,
                    incompatible_with=focus.incompatible_with,
                    psychic_only=focus.psychic_only,
                    arcane_expert_only=focus.arcane_expert_only,
                    arcane_warrior_only=focus.arcane_warrior_only,
                    allowed_classes=focus.allowed_classes
                )
        raise ValueError(f"Focus not found: {name}")
