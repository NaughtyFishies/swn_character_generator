"""Sunblade abilities and sacred weapon system."""
import json
import random
from pathlib import Path
from typing import List, Dict, Optional


class SunbladeAbility:
    """Represents a Sunblade ability/power."""

    def __init__(self, name: str, description: str, level_required: int = 1,
                 automatic: bool = False, hp_bonus: int = 0,
                 grants_focus: Optional[str] = None):
        """
        Initialize a Sunblade ability.

        Args:
            name: Ability name
            description: Ability description
            level_required: Minimum level to acquire this ability
            automatic: If True, granted automatically at level
            hp_bonus: HP bonus per level if ability grants it
            grants_focus: Name of focus granted by this ability
        """
        self.name = name
        self.description = description
        self.level_required = level_required
        self.automatic = automatic
        self.hp_bonus = hp_bonus
        self.grants_focus = grants_focus

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
        if self.grants_focus:
            result["grants_focus"] = self.grants_focus
        return result

    def __str__(self) -> str:
        """Return formatted ability description."""
        return f"{self.name}: {self.description}"


class SacredWeapon:
    """Represents a Sunblade's sacred weapon."""

    def __init__(self, weapon_type: str, damage: str, shock: str,
                 attribute: str, weapon_range: str):
        """
        Initialize a sacred weapon.

        Args:
            weapon_type: Type of sacred weapon
            damage: Damage formula
            shock: Shock damage and AC
            attribute: Governing attributes
            weapon_range: Range of weapon
        """
        self.weapon_type = weapon_type
        self.damage = damage
        self.shock = shock
        self.attribute = attribute
        self.range = weapon_range

    def to_dict(self) -> dict:
        """Convert weapon to dictionary format."""
        return {
            "type": self.weapon_type,
            "damage": self.damage,
            "shock": self.shock,
            "attribute": self.attribute,
            "range": self.range
        }

    def __str__(self) -> str:
        """Return formatted weapon description."""
        return f"{self.weapon_type} - Damage: {self.damage}, Shock: {self.shock}, Range: {self.range}"


class SunbladeAbilitySet:
    """Represents a Sunblade character's abilities."""

    def __init__(self, character_level: int, sunblade_skill_level: int,
                 selected_abilities: List[SunbladeAbility],
                 sacred_weapon: SacredWeapon):
        """
        Initialize Sunblade ability set.

        Args:
            character_level: Character's level
            sunblade_skill_level: Level of Sunblade skill
            selected_abilities: List of selected abilities
            sacred_weapon: Character's sacred weapon
        """
        self.character_level = character_level
        self.sunblade_skill_level = sunblade_skill_level
        self.selected_abilities = selected_abilities
        self.sacred_weapon = sacred_weapon

    def calculate_effort_pool(self, wis_modifier: int, cha_modifier: int) -> int:
        """
        Calculate Sunblade Effort pool.

        Formula: Sunblade skill + higher of WIS or CHA modifier

        Args:
            wis_modifier: Wisdom modifier
            cha_modifier: Charisma modifier

        Returns:
            Effort pool value
        """
        return self.sunblade_skill_level + max(wis_modifier, cha_modifier)

    def calculate_hit_bonus(self) -> int:
        """
        Calculate hit bonus with sacred weapon.

        Formula: Half character level, rounded up

        Returns:
            Hit bonus value
        """
        return (self.character_level + 1) // 2

    def to_dict(self) -> dict:
        """Convert ability set to dictionary format."""
        return {
            "character_level": self.character_level,
            "sunblade_skill_level": self.sunblade_skill_level,
            "abilities": [ability.to_dict() for ability in self.selected_abilities],
            "sacred_weapon": self.sacred_weapon.to_dict()
        }


class SunbladeAbilitySelector:
    """Manages Sunblade ability selection and loading."""

    def __init__(self, level_1_abilities: List[SunbladeAbility],
                 selectable_abilities: List[SunbladeAbility],
                 sacred_weapons: List[SacredWeapon]):
        """
        Initialize ability selector.

        Args:
            level_1_abilities: Automatic level 1 abilities
            selectable_abilities: Pool of selectable abilities
            sacred_weapons: Available sacred weapon types
        """
        self.level_1_abilities = level_1_abilities
        self.selectable_abilities = selectable_abilities
        self.sacred_weapons = sacred_weapons

    @classmethod
    def load_from_file(cls, file_path: str) -> 'SunbladeAbilitySelector':
        """
        Load Sunblade abilities from JSON file.

        Args:
            file_path: Path to sunblade_abilities.json

        Returns:
            SunbladeAbilitySelector instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Sunblade abilities file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        # Load level 1 automatic abilities
        level_1_abilities = [
            SunbladeAbility(
                name=ability["name"],
                description=ability["description"],
                level_required=ability.get("level_required", 1),
                automatic=ability.get("automatic", True),
                hp_bonus=ability.get("hp_bonus", 0),
                grants_focus=ability.get("grants_focus")
            )
            for ability in data["level_1_abilities"]
        ]

        # Load selectable abilities
        selectable_abilities = [
            SunbladeAbility(
                name=ability["name"],
                description=ability["description"],
                level_required=2,  # Selectable at level 2+
                automatic=False,
                hp_bonus=ability.get("hp_bonus", 0),
                grants_focus=ability.get("grants_focus")
            )
            for ability in data["selectable_abilities"]
        ]

        # Load sacred weapons
        sacred_weapons = [
            SacredWeapon(
                weapon_type=weapon["type"],
                damage=weapon["damage"],
                shock=weapon["shock"],
                attribute=weapon["attribute"],
                weapon_range=weapon["range"]
            )
            for weapon in data["sacred_weapons"]
        ]

        return cls(level_1_abilities, selectable_abilities, sacred_weapons)

    def create_sunblade_abilities(self, character_level: int,
                                   sunblade_skill_level: int) -> SunbladeAbilitySet:
        """
        Create abilities for a Sunblade character.

        Args:
            character_level: Character's level
            sunblade_skill_level: Level of Sunblade skill

        Returns:
            SunbladeAbilitySet instance
        """
        # All Sunblades get level 1 automatic abilities
        selected = list(self.level_1_abilities)

        # Calculate how many selectable abilities they get
        # Levels 2, 4, 6, 8, 10
        num_selectable = sum(1 for level in [2, 4, 6, 8, 10] if level <= character_level)

        # Randomly select from available abilities
        if num_selectable > 0 and self.selectable_abilities:
            available = list(self.selectable_abilities)
            random.shuffle(available)
            selected.extend(available[:num_selectable])

        # Select a random sacred weapon
        sacred_weapon = random.choice(self.sacred_weapons)

        return SunbladeAbilitySet(
            character_level=character_level,
            sunblade_skill_level=sunblade_skill_level,
            selected_abilities=selected,
            sacred_weapon=sacred_weapon
        )
