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
        self.sunblade_abilities: Optional['SunbladeAbilitySet'] = None
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
        Calculate saving throws based on level and attributes.

        Formula for each save:
        - Physical: 16 - level - max(STR mod, CON mod)
        - Evasion: 16 - level - max(DEX mod, INT mod)
        - Mental: 16 - level - max(WIS mod, CHA mod)

        Returns:
            Dictionary with Physical, Evasion, and Mental saves
        """
        if not self.attributes:
            return {"Physical": 15, "Evasion": 15, "Mental": 15}

        # Get attribute modifiers
        str_mod = self.attributes.get_modifier("STR")
        con_mod = self.attributes.get_modifier("CON")
        dex_mod = self.attributes.get_modifier("DEX")
        int_mod = self.attributes.get_modifier("INT")
        wis_mod = self.attributes.get_modifier("WIS")
        cha_mod = self.attributes.get_modifier("CHA")

        # Calculate saves using formula: 16 - level - best_attribute_mod
        physical = 16 - self.level - max(str_mod, con_mod)
        evasion = 16 - self.level - max(dex_mod, int_mod)
        mental = 16 - self.level - max(wis_mod, cha_mod)

        return {
            "Physical": physical,
            "Evasion": evasion,
            "Mental": mental
        }

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
            "sunblade_abilities": self.sunblade_abilities.to_dict() if self.sunblade_abilities else None,
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
