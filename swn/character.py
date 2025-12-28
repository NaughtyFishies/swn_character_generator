"""Character model for Stars Without Number."""
from typing import Optional, List, Dict
from swn.models.attributes import Attributes


class Character:
    """Main character data container for SWN characters."""

    def __init__(self, name: str = "Unnamed"):
        """
        Initialize a new character.

        Args:
            name: Character's name
        """
        self.name = name
        self.attributes: Optional[Attributes] = None
        self.character_class: Optional['CharacterClass'] = None
        self.background: Optional['Background'] = None
        self.skills: Optional['SkillSet'] = None
        self.foci: List['Focus'] = []
        self.psychic_powers: Optional['PsychicPowers'] = None
        self.spells: Optional['SpellList'] = None
        self.hp: int = 0
        self.saving_throws: Dict[str, int] = {}
        self.level: int = 1
        self.power_type: str = "normal"  # normal, magic, or psionic
        self.attack_bonus: int = 0
        self.equipment: Optional['EquipmentSet'] = None
        self.credits: int = 0

    def calculate_hp(self) -> int:
        """
        Calculate HP based on class, CON modifier, and level.

        Formula: Roll (1d6 + class_hp_bonus + CON_modifier) for each level and sum

        Returns:
            Hit points value
        """
        if not self.character_class or not self.attributes:
            return 1

        con_mod = self.attributes.get_modifier("CON")
        total_hp = 0

        # Roll HP for each level
        for _ in range(self.level):
            hp_roll = self.character_class.roll_hp()  # Includes class hp_bonus
            total_hp += max(1, hp_roll + con_mod)

        return total_hp

    def calculate_saves(self) -> Dict[str, int]:
        """
        Calculate saving throws based on class.

        Returns:
            Dictionary with Physical, Evasion, and Mental saves
        """
        if not self.character_class:
            return {"Physical": 15, "Evasion": 15, "Mental": 15}

        return self.character_class.get_saves()

    def to_dict(self) -> dict:
        """
        Serialize character to dictionary format.

        Returns:
            Dictionary representation of character
        """
        return {
            "name": self.name,
            "level": self.level,
            "power_type": self.power_type,
            "class": self.character_class.name if self.character_class else None,
            "background": self.background.name if self.background else None,
            "attributes": self.attributes.to_dict() if self.attributes else None,
            "skills": self.skills.to_dict() if self.skills else {},
            "foci": [focus.to_dict() for focus in self.foci],
            "psychic_powers": self.psychic_powers.to_dict() if self.psychic_powers else None,
            "spells": self.spells.to_dict() if self.spells else None,
            "hp": self.hp,
            "attack_bonus": self.attack_bonus,
            "saving_throws": self.saving_throws,
            "equipment": self.equipment.to_dict() if self.equipment else None,
            "credits": self.credits
        }

    def __str__(self) -> str:
        """Return brief character summary."""
        class_name = self.character_class.name if self.character_class else "No Class"
        bg_name = self.background.name if self.background else "No Background"
        return f"{self.name} - Level {self.level} {class_name} ({bg_name})"
