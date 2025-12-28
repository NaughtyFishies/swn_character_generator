"""Attribute system for SWN characters."""
from swn.dice import DiceRoller


class Attributes:
    """Manages the six core attributes (STR, DEX, CON, INT, WIS, CHA)."""

    ATTRIBUTE_NAMES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

    def __init__(self, str_val: int = 10, dex_val: int = 10, con_val: int = 10,
                 int_val: int = 10, wis_val: int = 10, cha_val: int = 10):
        """
        Initialize attributes with given values.

        Args:
            str_val: Strength score
            dex_val: Dexterity score
            con_val: Constitution score
            int_val: Intelligence score
            wis_val: Wisdom score
            cha_val: Charisma score
        """
        self.STR = str_val
        self.DEX = dex_val
        self.CON = con_val
        self.INT = int_val
        self.WIS = wis_val
        self.CHA = cha_val

    @classmethod
    def roll_attributes(cls, method: str = "roll") -> 'Attributes':
        """
        Generate attributes using official SWN method.

        Args:
            method: "roll" (3d6 six times in order, pick one to set to 14) or
                   "array" (assign 14, 12, 11, 10, 9, 7 as desired)

        Returns:
            New Attributes instance
        """
        import random

        if method == "array":
            # Standard array: 14, 12, 11, 10, 9, 7
            # Randomly assign to attributes for automated generation
            values = [14, 12, 11, 10, 9, 7]
            random.shuffle(values)
        else:
            # Roll 3d6 six times in order (STR, DEX, CON, INT, WIS, CHA)
            values = [DiceRoller.roll_3d6() for _ in range(6)]

            # Pick one attribute to change to 14
            # Strategy: Set the lowest score to 14 for maximum benefit
            min_idx = values.index(min(values))
            values[min_idx] = 14

        return cls(
            str_val=values[0],
            dex_val=values[1],
            con_val=values[2],
            int_val=values[3],
            wis_val=values[4],
            cha_val=values[5]
        )

    def get_modifier(self, attr_name: str) -> int:
        """
        Get the modifier for a given attribute.

        Args:
            attr_name: Name of the attribute (STR, DEX, CON, INT, WIS, CHA)

        Returns:
            Modifier value (-2 to +2)
        """
        attr_name = attr_name.upper()
        if attr_name not in self.ATTRIBUTE_NAMES:
            raise ValueError(f"Invalid attribute name: {attr_name}")

        score = getattr(self, attr_name)
        return DiceRoller.attribute_modifier(score)

    def get_score(self, attr_name: str) -> int:
        """
        Get the raw score for a given attribute.

        Args:
            attr_name: Name of the attribute (STR, DEX, CON, INT, WIS, CHA)

        Returns:
            Attribute score
        """
        attr_name = attr_name.upper()
        if attr_name not in self.ATTRIBUTE_NAMES:
            raise ValueError(f"Invalid attribute name: {attr_name}")

        return getattr(self, attr_name)

    def to_dict(self) -> dict:
        """Convert attributes to dictionary format."""
        return {
            attr: {
                "score": getattr(self, attr),
                "modifier": self.get_modifier(attr)
            }
            for attr in self.ATTRIBUTE_NAMES
        }

    def __str__(self) -> str:
        """Return formatted string of all attributes with modifiers."""
        lines = []
        for attr in self.ATTRIBUTE_NAMES:
            score = getattr(self, attr)
            mod = self.get_modifier(attr)
            mod_str = f"+{mod}" if mod >= 0 else str(mod)
            lines.append(f"{attr}: {score:2d} ({mod_str})")
        return "\n".join(lines)
