"""Background system for SWN characters."""
import json
import random
from pathlib import Path
from typing import List, Optional


class Background:
    """Represents a character background."""

    def __init__(self, name: str, free_skill: str, quick_skills: List[str],
                 description: str = "", class_specific: Optional[str] = None):
        """
        Initialize a background.

        Args:
            name: Background name
            free_skill: Skill automatically granted at level -1
            quick_skills: List of skills to choose from (granted at level 0)
            description: Background description
            class_specific: Optional class name this background is designed for
        """
        self.name = name
        self.free_skill = free_skill
        self.quick_skills = quick_skills
        self.description = description
        self.class_specific = class_specific

    def select_quick_skill(self, available_skills: Optional[List[str]] = None) -> str:
        """
        Randomly select one of the quick skills.

        Handles special cases like "Any Combat", "Any Skill", and "Shoot or Trade".

        Args:
            available_skills: Optional list of all available skills for "Any Skill" resolution

        Returns:
            Name of the selected skill
        """
        skill = random.choice(self.quick_skills)

        # Handle "Any Combat" - choose from Shoot, Stab, or Punch
        if skill == "Any Combat":
            return random.choice(["Shoot", "Stab", "Punch"])

        # Handle "Shoot or Trade" - choose one
        if skill == "Shoot or Trade":
            return random.choice(["Shoot", "Trade"])

        # Handle "Any Skill" - choose from provided skills list
        if skill == "Any Skill":
            if available_skills:
                return random.choice(available_skills)
            else:
                # Fallback to common non-psychic skills
                return random.choice(["Administer", "Connect", "Exert", "Fix", "Know",
                                    "Lead", "Notice", "Perform", "Pilot", "Program",
                                    "Sneak", "Survive", "Talk", "Trade", "Work"])

        return skill

    def resolve_free_skill(self, available_skills: Optional[List[str]] = None) -> str:
        """
        Resolve the free skill, handling special cases.

        Handles special cases like "Any Combat" and "Any Skill".

        Args:
            available_skills: Optional list of all available skills for "Any Skill" resolution

        Returns:
            Name of the resolved free skill
        """
        # Handle "Any Combat" for free skill
        if self.free_skill == "Any Combat":
            return random.choice(["Shoot", "Stab", "Punch"])

        # Handle "Any Skill" for free skill
        if self.free_skill == "Any Skill":
            if available_skills:
                return random.choice(available_skills)
            else:
                # Fallback to common non-psychic skills
                return random.choice(["Administer", "Connect", "Exert", "Fix", "Know",
                                    "Lead", "Notice", "Perform", "Pilot", "Program",
                                    "Sneak", "Survive", "Talk", "Trade", "Work"])

        return self.free_skill

    def to_dict(self) -> dict:
        """Convert background to dictionary format."""
        result = {
            "name": self.name,
            "free_skill": self.free_skill,
            "quick_skills": self.quick_skills,
            "description": self.description
        }
        if self.class_specific:
            result["class_specific"] = self.class_specific
        return result

    def __str__(self) -> str:
        """Return formatted background description."""
        return f"{self.name}: {self.description}"


class BackgroundTable:
    """Manages background loading and selection."""

    def __init__(self, backgrounds: List[Background]):
        """
        Initialize background table.

        Args:
            backgrounds: List of available backgrounds
        """
        self.backgrounds = backgrounds

    @classmethod
    def load_from_file(cls, file_path: str) -> 'BackgroundTable':
        """
        Load backgrounds from JSON file.

        Args:
            file_path: Path to backgrounds JSON file

        Returns:
            BackgroundTable instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Backgrounds file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        backgrounds = [
            Background(
                name=bg["name"],
                free_skill=bg["free_skill"],
                quick_skills=bg["quick_skills"],
                description=bg.get("description", ""),
                class_specific=bg.get("class_specific")
            )
            for bg in data["backgrounds"]
        ]

        return cls(backgrounds)

    def get_random_background(self) -> Background:
        """
        Select a random background.

        Returns:
            Random Background instance
        """
        return random.choice(self.backgrounds)

    def get_background_by_name(self, name: str) -> Optional[Background]:
        """
        Get a specific background by name.

        Args:
            name: Background name to search for

        Returns:
            Background instance if found, None otherwise
        """
        for bg in self.backgrounds:
            if bg.name.lower() == name.lower():
                return bg
        return None

    def get_all_background_names(self, include_class_specific: bool = True) -> List[str]:
        """
        Get list of all background names.

        Args:
            include_class_specific: If True, include class-specific backgrounds

        Returns:
            List of background names
        """
        if include_class_specific:
            return [bg.name for bg in self.backgrounds]
        else:
            return [bg.name for bg in self.backgrounds if not bg.class_specific]

    def get_backgrounds_by_class(self, class_name: Optional[str] = None) -> List['Background']:
        """
        Get backgrounds for a specific class or general backgrounds.

        Args:
            class_name: Class name to filter by, or None for general backgrounds

        Returns:
            List of Background instances
        """
        if class_name:
            return [bg for bg in self.backgrounds
                    if bg.class_specific == class_name or not bg.class_specific]
        else:
            return [bg for bg in self.backgrounds if not bg.class_specific]

    def __len__(self) -> int:
        """Return number of available backgrounds."""
        return len(self.backgrounds)
