"""Character classes for SWN."""
import json
import random
from pathlib import Path
from typing import Dict, List
from swn.dice import DiceRoller


class CharacterClass:
    """Base class for all SWN character classes."""

    def __init__(self, name: str, hp_die: int, hp_bonus: int, skill_points_base: int,
                 foci_count: int, attack_bonus: int, saving_throws: Dict[str, int],
                 description: str = "", special_abilities: List[str] = None,
                 is_spellcaster: bool = False, spell_tradition: str = None):
        """
        Initialize a character class.

        Args:
            name: Class name
            hp_die: Hit die size (typically 6 for SWN)
            hp_bonus: Bonus to HP rolls
            skill_points_base: Base skill points before INT modifier
            foci_count: Number of foci the class gets
            attack_bonus: Attack bonus per level
            saving_throws: Dict of save types to target numbers
            description: Class description
            special_abilities: List of special ability descriptions
            is_spellcaster: Whether this class casts spells
            spell_tradition: Spell tradition name if applicable
        """
        self.name = name
        self.hp_die = hp_die
        self.hp_bonus = hp_bonus
        self.skill_points_base = skill_points_base
        self.foci_count = foci_count
        self.attack_bonus = attack_bonus
        self.saving_throws = saving_throws
        self.description = description
        self.special_abilities = special_abilities or []
        self.is_spellcaster = is_spellcaster
        self.spell_tradition = spell_tradition

    def roll_hp(self) -> int:
        """
        Roll HP for this class.

        Returns:
            HP roll result
        """
        return DiceRoller.roll_1d6(self.hp_bonus)

    def get_skill_points(self, int_modifier: int, power_level: str = "normal") -> int:
        """
        Calculate total skill points for this class.

        Args:
            int_modifier: Intelligence modifier
            power_level: Character power level (affects points)

        Returns:
            Total skill points
        """
        base = self.skill_points_base + int_modifier

        # Adjust for power level
        if power_level == "weak":
            base -= 1
        elif power_level == "strong":
            base += 1

        return max(1, base)  # Minimum 1 skill point

    def get_saves(self) -> Dict[str, int]:
        """
        Get saving throw values.

        Returns:
            Dictionary of save types to values
        """
        return self.saving_throws.copy()

    def get_priority_skills(self) -> List[str]:
        """
        Get list of priority skills for this class.

        Returns:
            List of skill names
        """
        # Default priorities by class
        if self.name == "Warrior":
            return ["Shoot", "Stab", "Punch", "Exert", "Notice", "Lead"]
        elif self.name == "Expert":
            return ["Fix", "Program", "Notice", "Sneak", "Talk", "Connect"]
        elif self.name == "Psychic":
            # Psychics prioritize their discipline skills (which are granted at class creation)
            # Plus general useful skills
            return ["Know", "Notice", "Talk", "Connect", "Survive"]
        elif self.name == "Adventurer":
            return ["Notice", "Survive", "Shoot", "Fix", "Talk"]
        else:
            return []

    def to_dict(self) -> dict:
        """Convert class to dictionary format."""
        return {
            "name": self.name,
            "hp_die": self.hp_die,
            "hp_bonus": self.hp_bonus,
            "skill_points_base": self.skill_points_base,
            "foci_count": self.foci_count,
            "attack_bonus": self.attack_bonus,
            "saving_throws": self.saving_throws,
            "description": self.description,
            "special_abilities": self.special_abilities
        }

    def __str__(self) -> str:
        """Return class name and description."""
        return f"{self.name}: {self.description}"


class ClassTable:
    """Manages character class loading and selection."""

    def __init__(self, classes: Dict[str, CharacterClass]):
        """
        Initialize class table.

        Args:
            classes: Dictionary mapping class names to CharacterClass instances
        """
        self.classes = classes

    @classmethod
    def load_from_file(cls, file_path: str) -> 'ClassTable':
        """
        Load classes from JSON file.

        Args:
            file_path: Path to classes JSON file

        Returns:
            ClassTable instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Classes file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        classes = {}
        for class_name, class_data in data["classes"].items():
            classes[class_name] = CharacterClass(
                name=class_name,
                hp_die=class_data["hp_die"],
                hp_bonus=class_data["hp_bonus"],
                skill_points_base=class_data["skill_points_base"],
                foci_count=class_data["foci_count"],
                attack_bonus=class_data["attack_bonus"],
                saving_throws=class_data["saving_throws"],
                description=class_data.get("description", ""),
                special_abilities=class_data.get("special_abilities", []),
                is_spellcaster=class_data.get("is_spellcaster", False),
                spell_tradition=class_data.get("spell_tradition", None)
            )

        return cls(classes)

    def get_class(self, name: str) -> CharacterClass:
        """
        Get a class by name.

        Args:
            name: Class name

        Returns:
            CharacterClass instance

        Raises:
            ValueError if class not found
        """
        if name not in self.classes:
            raise ValueError(f"Unknown class: {name}")
        return self.classes[name]

    def get_random_class(self, exclude_psychic: bool = False) -> CharacterClass:
        """
        Get a random class.

        Args:
            exclude_psychic: If True, don't select Psychic class

        Returns:
            Random CharacterClass instance
        """
        available = list(self.classes.values())
        if exclude_psychic:
            available = [c for c in available if c.name != "Psychic"]
        return random.choice(available)

    def get_all_class_names(self) -> List[str]:
        """
        Get list of all class names.

        Returns:
            List of class names
        """
        return list(self.classes.keys())
