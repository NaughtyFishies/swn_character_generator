"""Skill system for SWN characters."""
import random
from typing import Dict, List


class Skill:
    """Represents a single skill with a level."""

    def __init__(self, name: str, level: int = 0):
        """
        Initialize a skill.

        Args:
            name: Skill name
            level: Skill level (-1 to 4, where -1 is from background free skill)
        """
        self.name = name
        self.level = max(-1, min(4, level))  # Clamp to valid range

    def __str__(self) -> str:
        """Return formatted skill string."""
        return f"{self.name}-{self.level}"

    def __repr__(self) -> str:
        """Return representation string."""
        return f"Skill({self.name}, {self.level})"


class SkillSet:
    """Manages a character's collection of skills."""

    def __init__(self):
        """Initialize an empty skill set."""
        self.skills: Dict[str, Skill] = {}

    def add_skill(self, name: str, level: int = 0):
        """
        Add a skill or increase its level.

        Args:
            name: Skill name
            level: Skill level to set (if skill doesn't exist) or add
        """
        if name in self.skills:
            # If skill exists and new level is higher, use new level
            if level > self.skills[name].level:
                self.skills[name].level = min(4, level)
        else:
            # Add new skill
            self.skills[name] = Skill(name, level)

    def get_level(self, name: str) -> int:
        """
        Get the level of a skill.

        Args:
            name: Skill name

        Returns:
            Skill level (0 if skill not known)
        """
        if name in self.skills:
            return self.skills[name].level
        return 0

    def has_skill(self, name: str) -> bool:
        """
        Check if character has a skill.

        Args:
            name: Skill name

        Returns:
            True if character has the skill
        """
        return name in self.skills

    def get_all_skills(self) -> List[Skill]:
        """
        Get list of all skills.

        Returns:
            List of Skill objects
        """
        return sorted(self.skills.values(), key=lambda s: s.name)

    def total_points_spent(self) -> int:
        """
        Calculate total skill points spent.

        In SWN, skill costs are:
        Level -1: 0 points (from background)
        Level 0: 1 point
        Level 1: 2 points
        Level 2: 3 points
        Level 3: 4 points
        Level 4: 5 points

        Returns:
            Total points spent
        """
        total = 0
        for skill in self.skills.values():
            if skill.level == -1:
                total += 0
            elif skill.level == 0:
                total += 1
            elif skill.level == 1:
                total += 2
            elif skill.level == 2:
                total += 3
            elif skill.level == 3:
                total += 4
            elif skill.level == 4:
                total += 5
        return total

    def to_dict(self) -> Dict[str, int]:
        """
        Convert skills to dictionary format.

        Returns:
            Dictionary mapping skill names to levels
        """
        return {skill.name: skill.level for skill in self.skills.values()}

    def __str__(self) -> str:
        """Return formatted string of all skills."""
        if not self.skills:
            return "No skills"
        skill_list = [str(skill) for skill in sorted(self.skills.values(), key=lambda s: s.name)]
        return ", ".join(skill_list)


def allocate_skill_points(skill_set: SkillSet, points: int, all_skill_names: List[str],
                         priority_skills: List[str]):
    """
    Intelligently allocate skill points to a character using official SWN rules.

    Args:
        skill_set: SkillSet to add skills to
        points: Number of points to allocate
        all_skill_names: List of all valid skill names
        priority_skills: List of class-relevant skills to prioritize
    """
    spent = skill_set.total_points_spent()
    remaining = points - spent

    # Can't allocate if no points remaining
    if remaining <= 0:
        return

    # Determine how many skills to focus on based on points available
    # More focused for lower point totals
    max_attempts = 1000  # Prevent infinite loops
    attempts = 0

    while remaining > 0 and attempts < max_attempts:
        attempts += 1

        # 70% chance to improve priority skill for focused builds
        if random.random() < 0.7 and priority_skills:
            skill_name = random.choice(priority_skills)
        else:
            skill_name = random.choice(all_skill_names)

        current_level = skill_set.get_level(skill_name)

        # At character creation, cap at level 1 (official SWN rules)
        max_level = 1

        if current_level < max_level:
            # Calculate cost to increase skill
            cost = calculate_skill_cost(current_level)

            if cost <= remaining:
                skill_set.add_skill(skill_name, current_level + 1)
                remaining -= cost

        # If all priority skills are maxed, try any skill
        all_maxed = all(skill_set.get_level(s) >= max_level for s in all_skill_names)
        if all_maxed:
            break


def calculate_skill_cost(current_level: int) -> int:
    """
    Calculate cost to increase a skill from current level to next level.

    Args:
        current_level: Current skill level

    Returns:
        Point cost to increase to next level
    """
    # Cost to go from -1 to 0: 1 point
    # Cost to go from 0 to 1: 1 point (total 2)
    # Cost to go from 1 to 2: 1 point (total 3)
    # etc.
    if current_level == -1:
        return 1
    elif current_level == 0:
        return 1
    elif current_level == 1:
        return 1
    elif current_level == 2:
        return 1
    elif current_level == 3:
        return 1
    else:
        return 99  # Can't increase beyond level 4
