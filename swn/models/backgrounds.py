"""Background system for SWN characters."""
import json
import random
from pathlib import Path
from typing import List, Optional


class Background:
    """Represents a character background."""

    def __init__(self, name: str, free_skill: str, quick_skills: List[str],
                 description: str = ""):
        """
        Initialize a background.

        Args:
            name: Background name
            free_skill: Skill automatically granted at level -1
            quick_skills: List of skills to choose from (granted at level 0)
            description: Background description
        """
        self.name = name
        self.free_skill = free_skill
        self.quick_skills = quick_skills
        self.description = description

    def select_quick_skill(self) -> str:
        """
        Randomly select one of the quick skills.

        Returns:
            Name of the selected skill
        """
        return random.choice(self.quick_skills)

    def to_dict(self) -> dict:
        """Convert background to dictionary format."""
        return {
            "name": self.name,
            "free_skill": self.free_skill,
            "quick_skills": self.quick_skills,
            "description": self.description
        }

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
                description=bg.get("description", "")
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

    def __len__(self) -> int:
        """Return number of available backgrounds."""
        return len(self.backgrounds)
