"""Psychic powers system for SWN characters."""
import json
import random
from pathlib import Path
from typing import List, Dict


class PsychicTechnique:
    """Represents a single psychic technique."""

    def __init__(self, name: str, level: int, effort_cost: int, description: str):
        """
        Initialize a psychic technique.

        Args:
            name: Technique name
            level: Required Psychic skill level (0-4)
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


class PsychicDiscipline:
    """Represents a psychic discipline with its techniques."""

    def __init__(self, name: str, description: str, core_technique: PsychicTechnique,
                 techniques: List[PsychicTechnique]):
        """
        Initialize a psychic discipline.

        Args:
            name: Discipline name
            description: Discipline description
            core_technique: Level 0 core technique (always available)
            techniques: List of higher-level techniques
        """
        self.name = name
        self.description = description
        self.core_technique = core_technique
        self.techniques = techniques

    def get_available_techniques(self, psychic_skill_level: int) -> List[PsychicTechnique]:
        """
        Get techniques available at a given Psychic skill level.

        Args:
            psychic_skill_level: Character's Psychic skill level

        Returns:
            List of available techniques (always includes core)
        """
        available = [self.core_technique]
        for tech in self.techniques:
            if tech.level <= psychic_skill_level:
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
    """Manages a character's psychic powers."""

    def __init__(self, disciplines: List[PsychicDiscipline], psychic_skill_level: int,
                 effort_pool: int):
        """
        Initialize psychic powers.

        Args:
            disciplines: List of disciplines the character knows
            psychic_skill_level: Character's Psychic skill level
            effort_pool: Maximum effort points
        """
        self.disciplines = disciplines
        self.psychic_skill_level = psychic_skill_level
        self.effort_pool = effort_pool
        self.selected_techniques: List[PsychicTechnique] = []

        # Automatically grant all core techniques
        for discipline in disciplines:
            self.selected_techniques.append(discipline.core_technique)

    def add_technique(self, technique: PsychicTechnique):
        """
        Add a technique to the character's known techniques.

        Args:
            technique: Technique to add
        """
        if technique not in self.selected_techniques:
            self.selected_techniques.append(technique)

    def get_all_techniques(self) -> List[PsychicTechnique]:
        """
        Get all known techniques.

        Returns:
            List of known techniques
        """
        return self.selected_techniques

    def to_dict(self) -> dict:
        """Convert psychic powers to dictionary format."""
        return {
            "disciplines": [disc.name for disc in self.disciplines],
            "psychic_skill_level": self.psychic_skill_level,
            "effort_pool": self.effort_pool,
            "techniques": [tech.to_dict() for tech in self.selected_techniques]
        }

    def __str__(self) -> str:
        """Return formatted psychic powers description."""
        lines = [f"Effort Pool: {self.effort_pool}"]
        lines.append(f"Psychic Skill: {self.psychic_skill_level}")
        lines.append("")

        for discipline in self.disciplines:
            lines.append(f"{discipline.name}:")
            # Get techniques for this discipline
            disc_techs = [t for t in self.selected_techniques
                         if t in [discipline.core_technique] + discipline.techniques]
            for tech in disc_techs:
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

    def create_psychic_powers(self, power_type: str, power_level: str,
                             psychic_skill_level: int, effort_modifier: int) -> PsychicPowers:
        """
        Create psychic powers for a character.

        Args:
            power_type: "magic" or "psionic"
            power_level: "weak", "normal", or "strong"
            psychic_skill_level: Character's Psychic skill level
            effort_modifier: Modifier to effort pool (usually WIS or INT mod)

        Returns:
            PsychicPowers instance
        """
        # Determine number of disciplines
        if power_type == "magic":
            num_disciplines = 1 if power_level != "strong" else 2
        else:  # psionic
            num_disciplines = 2 if power_level == "normal" else 3
            if power_level == "weak":
                num_disciplines = 1

        # Select random disciplines
        num_disciplines = min(num_disciplines, len(self.disciplines))
        selected_disciplines = random.sample(self.disciplines, num_disciplines)

        # Calculate effort pool: 1 + Psychic skill + WIS/INT modifier
        effort_pool = 1 + psychic_skill_level + max(0, effort_modifier)

        # Create psychic powers
        powers = PsychicPowers(selected_disciplines, psychic_skill_level, effort_pool)

        # Grant additional techniques based on Psychic skill level
        for discipline in selected_disciplines:
            available_techs = discipline.get_available_techniques(psychic_skill_level)
            # Grant 1-2 techniques per discipline beyond the core
            num_to_grant = min(2, len(available_techs) - 1)  # -1 for core which is already added

            # Filter out core technique
            non_core = [t for t in available_techs if t != discipline.core_technique]
            if non_core and num_to_grant > 0:
                granted = random.sample(non_core, min(num_to_grant, len(non_core)))
                for tech in granted:
                    powers.add_technique(tech)

        return powers
