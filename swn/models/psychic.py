"""Psychic powers system for SWN characters.

In SWN, each psychic discipline (Biopsionics, Telepathy, etc.) is its own skill.
When a character has level-0 in a discipline, they automatically get the core technique.
Each time they increase the skill level, they choose ONE new technique from that discipline.
"""
import json
import random
from pathlib import Path
from typing import List, Dict, Optional


class PsychicTechnique:
    """Represents a single psychic technique."""

    def __init__(self, name: str, level: int, effort_cost: int, description: str):
        """
        Initialize a psychic technique.

        Args:
            name: Technique name
            level: Required skill level in the discipline (0-4)
            effort_cost: Effort points required to use
            description: Technique description
        """
        self.name = name
        self.level = level
        self.effort_cost = effort_cost
        self.description = description

    def to_dict(self) -> dict:
        """Convert technique to dictionary format."""
        return {
            "name": self.name,
            "level": self.level,
            "effort_cost": self.effort_cost,
            "description": self.description
        }

    def __str__(self) -> str:
        """Return formatted technique description."""
        effort_str = f"({self.effort_cost} Effort)" if self.effort_cost > 0 else "(Core)"
        return f"   {self.name} {effort_str}\n      {self.description}"

    def __eq__(self, other):
        """Check equality based on name."""
        if isinstance(other, PsychicTechnique):
            return self.name == other.name
        return False

    def __hash__(self):
        """Make hashable for use in sets/dicts."""
        return hash(self.name)


class PsychicDiscipline:
    """Represents a psychic discipline with its techniques."""

    def __init__(self, name: str, description: str, core_technique: PsychicTechnique,
                 techniques: List[PsychicTechnique]):
        """
        Initialize a psychic discipline.

        Args:
            name: Discipline name (matches skill name)
            description: Discipline description
            core_technique: Level 0 core technique (always available at level-0)
            techniques: List of higher-level techniques (levels 1-4)
        """
        self.name = name
        self.description = description
        self.core_technique = core_technique
        self.techniques = techniques

    def get_techniques_at_level(self, skill_level: int) -> List[PsychicTechnique]:
        """
        Get all techniques available at a specific skill level.

        Args:
            skill_level: Skill level in this discipline (0-4)

        Returns:
            List of techniques available at exactly this level (not including lower levels)
        """
        if skill_level == 0:
            return [self.core_technique]
        return [t for t in self.techniques if t.level == skill_level]

    def get_available_techniques(self, skill_level: int) -> List[PsychicTechnique]:
        """
        Get all techniques available up to and including a skill level.

        Args:
            skill_level: Skill level in this discipline (0-4)

        Returns:
            List of all techniques available (core + all techniques <= skill_level)
        """
        available = [self.core_technique]
        for tech in self.techniques:
            if tech.level <= skill_level:
                available.append(tech)
        return available

    def to_dict(self) -> dict:
        """Convert discipline to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "core_technique": self.core_technique.to_dict(),
            "techniques": [tech.to_dict() for tech in self.techniques]
        }

    def __str__(self) -> str:
        """Return formatted discipline description."""
        return f"{self.name}: {self.description}"


class PsychicPowers:
    """Manages a character's psychic powers.

    Tracks which techniques have been chosen for each discipline skill.
    The discipline skills themselves are stored in the character's SkillSet.
    """

    def __init__(self, effort_pool: int):
        """
        Initialize psychic powers.

        Args:
            effort_pool: Maximum effort points (1 + highest discipline skill + WIS/INT mod)
        """
        self.effort_pool = effort_pool
        # Map: discipline name -> list of chosen techniques (in order chosen)
        # Core techniques are implicit based on having the skill at level-0+
        self.discipline_techniques: Dict[str, List[PsychicTechnique]] = {}

    def add_technique(self, discipline_name: str, technique: PsychicTechnique):
        """
        Add a chosen technique for a discipline.

        Args:
            discipline_name: Name of the discipline
            technique: Technique that was chosen
        """
        if discipline_name not in self.discipline_techniques:
            self.discipline_techniques[discipline_name] = []
        if technique not in self.discipline_techniques[discipline_name]:
            self.discipline_techniques[discipline_name].append(technique)

    def get_techniques(self, discipline_name: str) -> List[PsychicTechnique]:
        """
        Get all chosen techniques for a discipline.

        Args:
            discipline_name: Name of the discipline

        Returns:
            List of chosen techniques (does not include core technique)
        """
        return self.discipline_techniques.get(discipline_name, [])

    def get_all_disciplines(self) -> List[str]:
        """
        Get names of all disciplines the character has techniques in.

        Returns:
            List of discipline names
        """
        return list(self.discipline_techniques.keys())

    def to_dict(self) -> dict:
        """Convert psychic powers to dictionary format."""
        return {
            "effort_pool": self.effort_pool,
            "disciplines": {
                disc: [tech.to_dict() for tech in techs]
                for disc, techs in self.discipline_techniques.items()
            }
        }

    def __str__(self) -> str:
        """Return formatted psychic powers description."""
        lines = [f"Effort Pool: {self.effort_pool}"]
        lines.append("")

        for disc_name, techniques in self.discipline_techniques.items():
            lines.append(f"{disc_name}:")
            for tech in techniques:
                lines.append(str(tech))
            lines.append("")

        return "\n".join(lines)


class PsychicPowerSelector:
    """Manages psychic discipline and technique selection."""

    def __init__(self, disciplines: List[PsychicDiscipline]):
        """
        Initialize psychic power selector.

        Args:
            disciplines: List of all available disciplines
        """
        self.disciplines = disciplines
        self.disciplines_by_name = {d.name: d for d in disciplines}

    @classmethod
    def load_from_file(cls, file_path: str) -> 'PsychicPowerSelector':
        """
        Load psychic disciplines from JSON file.

        Args:
            file_path: Path to psychic disciplines JSON file

        Returns:
            PsychicPowerSelector instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Psychic disciplines file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        disciplines = []
        for disc_data in data["disciplines"]:
            # Parse core technique
            core_data = disc_data["core_technique"]
            core_technique = PsychicTechnique(
                name=core_data["name"],
                level=core_data["level"],
                effort_cost=core_data["effort_cost"],
                description=core_data["description"]
            )

            # Parse other techniques
            techniques = [
                PsychicTechnique(
                    name=tech["name"],
                    level=tech["level"],
                    effort_cost=tech["effort_cost"],
                    description=tech["description"]
                )
                for tech in disc_data["techniques"]
            ]

            discipline = PsychicDiscipline(
                name=disc_data["name"],
                description=disc_data["description"],
                core_technique=core_technique,
                techniques=techniques
            )
            disciplines.append(discipline)

        return cls(disciplines)

    def get_discipline(self, name: str) -> Optional[PsychicDiscipline]:
        """
        Get a discipline by name.

        Args:
            name: Discipline name

        Returns:
            PsychicDiscipline or None if not found
        """
        return self.disciplines_by_name.get(name)

    def get_random_disciplines(self, count: int) -> List[str]:
        """
        Get random discipline names.

        Args:
            count: Number of disciplines to select

        Returns:
            List of discipline names
        """
        count = min(count, len(self.disciplines))
        selected = random.sample(self.disciplines, count)
        return [d.name for d in selected]

    def select_technique_for_level(self, discipline_name: str,
                                   skill_level: int,
                                   already_chosen: List[PsychicTechnique]) -> Optional[PsychicTechnique]:
        """
        Select a random technique when a discipline skill level increases.

        Args:
            discipline_name: Name of the discipline
            skill_level: New skill level (1-4)
            already_chosen: List of techniques already chosen for this discipline

        Returns:
            Selected technique, or None if no valid options
        """
        discipline = self.get_discipline(discipline_name)
        if not discipline:
            return None

        # Get techniques available at this level that haven't been chosen yet
        available_at_level = discipline.get_techniques_at_level(skill_level)

        # Filter out already chosen techniques
        valid_choices = [t for t in available_at_level if t not in already_chosen]

        if not valid_choices:
            # If no techniques at this exact level, try lower levels not yet chosen
            all_available = discipline.get_available_techniques(skill_level)
            valid_choices = [t for t in all_available
                           if t != discipline.core_technique and t not in already_chosen]

        if valid_choices:
            return random.choice(valid_choices)

        return None

    def calculate_effort_pool(self, discipline_skills: Dict[str, int],
                             effort_modifier: int) -> int:
        """
        Calculate effort pool based on highest discipline skill.

        Formula: 1 + highest discipline skill level + WIS or INT modifier (whichever is higher)

        Args:
            discipline_skills: Dict of discipline_name -> skill_level
            effort_modifier: WIS or INT modifier (whichever is higher)

        Returns:
            Effort pool value
        """
        if not discipline_skills:
            return 1

        highest_skill = max(discipline_skills.values())
        return 1 + highest_skill + max(0, effort_modifier)

    def create_psychic_powers_for_character(self, discipline_skills: Dict[str, int],
                                           effort_modifier: int) -> PsychicPowers:
        """
        Create PsychicPowers object for a character with discipline skills.

        For each discipline skill level from 1 to current, selects one technique.
        Core techniques (level-0) are automatically added for each discipline.

        Args:
            discipline_skills: Dict of discipline_name -> skill_level
            effort_modifier: WIS or INT modifier for effort pool

        Returns:
            PsychicPowers instance
        """
        effort_pool = self.calculate_effort_pool(discipline_skills, effort_modifier)
        powers = PsychicPowers(effort_pool)

        # For each discipline the character has
        for disc_name, skill_level in discipline_skills.items():
            if skill_level < 0:
                continue

            discipline = self.get_discipline(disc_name)
            if not discipline:
                continue

            # Always add the core technique (available at level 0+)
            powers.add_technique(disc_name, discipline.core_technique)

            # Initialize technique list for this discipline
            already_chosen = []

            # For each level from 1 to current skill level, pick one technique
            for level in range(1, skill_level + 1):
                technique = self.select_technique_for_level(disc_name, level, already_chosen)
                if technique:
                    powers.add_technique(disc_name, technique)
                    already_chosen.append(technique)

        return powers
