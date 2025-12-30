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
        self.yama_king_abilities: Optional['YamaKingAbilitySet'] = None
        self.godhunter_abilities: Optional['GodhunterAbilitySet'] = None
        self.free_nexus_abilities: Optional['FreeNexusAbilitySet'] = None
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
        Godhunter bonus: +1 HP at levels 1, 3, 5, 7, 9 (Grim Determination)

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

        # Add Godhunter Grim Determination bonus
        if self.godhunter_abilities:
            total_hp += self.godhunter_abilities.calculate_grim_determination_bonus()

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

    def calculate_ac(self) -> int:
        """
        Calculate Armor Class based on armor, shield, and DEX modifier.

        Formula:
        - Base AC = max(10, armor_ac) + DEX modifier
        - Shield: Either sets minimum AC or adds bonus, whichever is higher

        Returns:
            Armor Class value
        """
        if not self.attributes:
            return 10

        # Start with base AC
        base_ac = 10

        # Get DEX modifier
        dex_mod = self.attributes.get_modifier("DEX")

        # Apply armor if equipped
        if self.equipment and self.equipment.armor:
            armor_ac_value = self.equipment.armor.properties.get("ac", 10)
            # Handle numeric AC (most armor)
            if isinstance(armor_ac_value, int):
                base_ac = max(10, armor_ac_value)
            # Handle string AC (shouldn't happen for armor, but just in case)
            elif isinstance(armor_ac_value, str):
                try:
                    base_ac = max(10, int(armor_ac_value.split("/")[0]))
                except (ValueError, IndexError):
                    base_ac = 10

        # Add DEX modifier to AC
        ac = base_ac + dex_mod

        # Apply shield if equipped
        if self.equipment and self.equipment.shield:
            shield_ac_value = self.equipment.shield.properties.get("ac", "10")

            # Parse shield AC notation (e.g., "16/+2 bonus")
            if isinstance(shield_ac_value, str) and "/" in shield_ac_value:
                try:
                    parts = shield_ac_value.split("/")
                    min_ac = int(parts[0])
                    bonus_str = parts[1].replace("bonus", "").replace("+", "").strip()
                    bonus = int(bonus_str)

                    # Apply the better of: setting AC to min_ac, or adding bonus
                    ac = max(min_ac, ac + bonus)
                except (ValueError, IndexError):
                    pass  # If parsing fails, shield has no effect
            elif isinstance(shield_ac_value, int):
                # Simple numeric shield AC (just in case)
                ac = max(ac, shield_ac_value)

        return ac

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
            "yama_king_abilities": self.yama_king_abilities.to_dict() if self.yama_king_abilities else None,
            "godhunter_abilities": self.godhunter_abilities.to_dict() if self.godhunter_abilities else None,
            "free_nexus_abilities": self.free_nexus_abilities.to_dict() if self.free_nexus_abilities else None,
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
