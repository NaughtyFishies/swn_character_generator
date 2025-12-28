"""Dice rolling utilities for Stars Without Number character generation."""
import random


class DiceRoller:
    """Handles all dice rolling operations for character generation."""

    @staticmethod
    def roll(num_dice: int, sides: int, drop_lowest: int = 0) -> int:
        """
        Roll XdY, optionally dropping the lowest N dice.

        Args:
            num_dice: Number of dice to roll
            sides: Number of sides per die
            drop_lowest: Number of lowest dice to drop (default 0)

        Returns:
            Total of the dice roll
        """
        if num_dice <= 0 or sides <= 0:
            return 0

        rolls = [random.randint(1, sides) for _ in range(num_dice)]

        if drop_lowest > 0 and drop_lowest < num_dice:
            rolls.sort()
            rolls = rolls[drop_lowest:]

        return sum(rolls)

    @staticmethod
    def roll_3d6() -> int:
        """Roll 3d6 for standard attribute generation."""
        return DiceRoller.roll(3, 6)

    @staticmethod
    def roll_4d6_drop_lowest() -> int:
        """Roll 4d6 and drop the lowest die for strong characters."""
        return DiceRoller.roll(4, 6, drop_lowest=1)

    @staticmethod
    def roll_1d6(bonus: int = 0) -> int:
        """Roll 1d6 with optional bonus (for HP, etc.)."""
        return DiceRoller.roll(1, 6) + bonus

    @staticmethod
    def attribute_modifier(score: int) -> int:
        """
        Convert attribute score (3-18) to modifier (-2 to +2).

        SWN attribute modifiers:
        3: -2
        4-7: -1
        8-13: 0
        14-17: +1
        18: +2
        """
        if score <= 3:
            return -2
        elif score <= 7:
            return -1
        elif score <= 13:
            return 0
        elif score <= 17:
            return 1
        else:
            return 2
