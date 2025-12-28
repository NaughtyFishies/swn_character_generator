"""Character generation orchestrator for Stars Without Number."""
import json
import random
from pathlib import Path
from typing import Optional, List

from swn.character import Character
from swn.models.attributes import Attributes
from swn.models.backgrounds import BackgroundTable
from swn.models.classes import ClassTable
from swn.models.foci import FociSelector
from swn.models.psychic import PsychicPowerSelector
from swn.models.spells import SpellSelector
from swn.models.skills import SkillSet, allocate_skill_points
from swn.models.equipment import EquipmentSelector, calculate_starting_credits


class CharacterGenerator:
    """Main character generation orchestrator."""

    def __init__(self, data_dir: str = None):
        """
        Initialize the character generator.

        Args:
            data_dir: Directory containing data JSON files
        """
        if data_dir is None:
            # Default to swn/data directory
            data_dir = Path(__file__).parent / "data"
        else:
            data_dir = Path(data_dir)

        # Load all game data
        self.backgrounds = BackgroundTable.load_from_file(str(data_dir / "backgrounds.json"))
        self.classes = ClassTable.load_from_file(str(data_dir / "classes.json"))
        self.foci_selector = FociSelector.load_from_file(str(data_dir / "foci.json"))
        self.psychic_selector = PsychicPowerSelector.load_from_file(str(data_dir / "psychic_disciplines.json"))

        # Load spell selectors for spellcasting traditions
        self.spell_selectors = {}
        spell_files = {
            "Pacter": data_dir / "pacter_spells.json",
            "Rectifier": data_dir / "rectifier_spells.json",
            "War Mage": data_dir / "war_mage_spells.json",
            "Arcanist": data_dir / "arcanist_spells.json"
        }

        for tradition, file_path in spell_files.items():
            if file_path.exists():
                self.spell_selectors[tradition] = SpellSelector.load_from_file(tradition, str(file_path))

        # Load skills list
        with open(data_dir / "skills.json", 'r') as f:
            skills_data = json.load(f)
            self.all_skills = [skill["name"] for skill in skills_data["skills"]]

        # Load equipment selector
        self.equipment_selector = EquipmentSelector.load_from_files(data_dir)

    def generate_character(
        self,
        name: Optional[str] = None,
        level: int = 1,
        attribute_method: str = "roll",
        power_type: str = "normal",
        class_choice: Optional[str] = None,
        use_quick_skills: bool = True,
        tech_level: int = 4
    ) -> Character:
        """
        Generate a complete character using official SWN rules.

        Args:
            name: Character name (random if None)
            level: Character level (default 1)
            attribute_method: "roll" (3d6, pick one to 14) or "array" (14,12,11,10,9,7)
            power_type: "normal", "magic", or "psionic"
            class_choice: Class name or None for random
            use_quick_skills: True to use quick skills, False to roll on tables (simplified)
            tech_level: Technology level for equipment (0-5, default 4)

        Returns:
            Complete Character instance
        """
        # Step 1: Validate level (1-10)
        if level < 1:
            level = 1
        if level > 10:
            level = 10

        # Step 2: Create character with name
        if name is None:
            name = self._generate_random_name()

        character = Character(name)
        character.level = level
        character.power_type = power_type

        # Step 2: Generate attributes using chosen method
        character.attributes = Attributes.roll_attributes(attribute_method)

        # Step 3: Assign or randomize class
        if class_choice:
            character.character_class = self.classes.get_class(class_choice)
        else:
            # Don't randomly select Psychic class unless power_type is magic/psionic
            exclude_psychic = (power_type == "normal")
            character.character_class = self.classes.get_random_class(exclude_psychic)

        # Step 4: Roll random background
        character.background = self.backgrounds.get_random_background()

        # Step 5: Initialize skills and apply background skills
        character.skills = SkillSet()
        character.skills.add_skill(character.background.free_skill, -1)
        quick_skill = character.background.select_quick_skill()
        character.skills.add_skill(quick_skill, 0)

        # Step 6: Add class starting skills (if applicable)
        # Grant psychic discipline skills for psychic characters
        # Full Psychic: 2 disciplines, Partial Psychic/Psionic type: 1 discipline
        discipline_count = 0
        if character.character_class.name == "Psychic":
            discipline_count = 2  # Full psychic gets 2 disciplines
        elif power_type in ["magic", "psionic"]:
            discipline_count = 1  # Partial psychic gets 1 discipline

        # Select and grant random disciplines as skills at level 0
        if discipline_count > 0:
            discipline_names = self.psychic_selector.get_random_disciplines(discipline_count)
            for disc_name in discipline_names:
                if not character.skills.has_skill(disc_name):
                    character.skills.add_skill(disc_name, 0)

        # Step 7: Calculate available skill points
        # Formula: (class base + INT modifier) + (3 points per level)
        int_mod = character.attributes.get_modifier("INT")
        base_from_class = character.character_class.skill_points_base + int_mod
        points_from_levels = 3 * character.level
        total_points = base_from_class + points_from_levels
        total_points = max(1, total_points)  # Minimum 1 skill point

        # Step 8: Allocate remaining skill points
        # Exclude psychic disciplines from random allocation unless character is psychic
        psychic_disciplines = ["Biopsionics", "Metapsionics", "Precognition",
                              "Telekinesis", "Telepathy", "Teleportation"]
        is_psychic = (power_type in ["magic", "psionic"] or
                     character.character_class.name == "Psychic")

        # Filter skills list for allocation
        if is_psychic:
            available_skills = self.all_skills
        else:
            available_skills = [s for s in self.all_skills if s not in psychic_disciplines]

        priority_skills = character.character_class.get_priority_skills()
        allocate_skill_points(
            character.skills,
            total_points,
            available_skills,
            priority_skills,
            character.level  # Pass character level for skill cap calculation
        )

        # Step 8.5: No longer adding a "free" skill here
        # (Removed to match official SWN rules and fix skill point budget)

        # Step 9: Select foci based on class
        # Everyone gets 1 focus
        # Experts/Partial Experts get +1 non-combat, non-psychic focus
        # Warriors/Partial Warriors get +1 combat focus

        has_psychic = (power_type in ["magic", "psionic"] or
                      character.character_class.name == "Psychic")

        # Determine combat foci (simplified - common combat foci)
        combat_foci_names = [
            "Armsman", "Close Combatant", "Gunslinger", "Shocking Assault", "Sniper",
            "Unarmed Combatant", "Assassin", "Mageblade", "Elemental Warrior",
            "Arcane Physique", "Blade Ward", "Soul Shield", "Weapon Unity"
        ]

        foci_list = []

        # Base focus for everyone
        base_focus = self.foci_selector.select_random_foci(
            1, "normal", has_psychic, character.character_class.name
        )
        if base_focus:
            foci_list.extend(base_focus)

        # Class-specific bonus focus
        class_name = character.character_class.name

        # Experts and Partial Experts get non-combat, non-psychic bonus
        if class_name in ["Expert", "Arcane Expert"]:  # Partial Expert in Adventurer handled separately
            all_foci = self.foci_selector.foci
            non_combat_non_psychic = [
                f for f in all_foci
                if f.name not in combat_foci_names and not f.psychic_only
                and (f.allowed_classes is None or class_name in f.allowed_classes)
                and all(f.is_compatible_with(existing) for existing in foci_list)
            ]
            if non_combat_non_psychic:
                bonus = random.choice(non_combat_non_psychic)
                foci_list.append(bonus)

        # Warriors and Partial Warriors get combat bonus
        elif class_name in ["Warrior", "Arcane Warrior"]:  # Partial Warrior in Adventurer handled separately
            all_foci = self.foci_selector.foci
            combat_foci = [
                f for f in all_foci
                if f.name in combat_foci_names
                and (f.allowed_classes is None or class_name in f.allowed_classes)
                and all(f.is_compatible_with(existing) for existing in foci_list)
            ]
            if combat_foci:
                bonus = random.choice(combat_foci)
                foci_list.append(bonus)

        character.foci = foci_list

        # Step 10: Handle psychic powers
        # Generate psychic powers based on discipline skills
        if power_type in ["magic", "psionic"] or character.character_class.name == "Psychic":
            # Get all discipline skills the character has
            psychic_disciplines = ["Biopsionics", "Metapsionics", "Precognition",
                                  "Telekinesis", "Telepathy", "Teleportation"]
            discipline_skills = {}
            for disc_name in psychic_disciplines:
                if character.skills.has_skill(disc_name):
                    discipline_skills[disc_name] = character.skills.get_level(disc_name)

            # Only create psychic powers if character has at least one discipline
            if discipline_skills:
                effort_mod = max(
                    character.attributes.get_modifier("WIS"),
                    character.attributes.get_modifier("INT")
                )

                character.psychic_powers = self.psychic_selector.create_psychic_powers_for_character(
                    discipline_skills,
                    effort_mod
                )

        # Step 10.5: Handle spell assignment for spellcasting classes
        if character.character_class.is_spellcaster:
            spell_tradition = character.character_class.spell_tradition
            if spell_tradition and spell_tradition in self.spell_selectors:
                character.spells = self.spell_selectors[spell_tradition].create_spell_list(character.level)
                # Spellcasters get Cast Magic skill
                if not character.skills.has_skill("Cast Magic"):
                    character.skills.add_skill("Cast Magic", 0)

        # Step 11: Calculate HP
        character.hp = character.calculate_hp()

        # Step 12: Calculate saving throws
        character.saving_throws = character.calculate_saves()

        # Step 13: Set attack bonus
        character.attack_bonus = character.character_class.attack_bonus * character.level

        # Step 14: Select equipment based on tech level
        starting_credits = calculate_starting_credits(character.character_class.name, character.level)
        character.equipment = self.equipment_selector.select_equipment(
            character.character_class.name,
            tech_level,
            starting_credits
        )

        # Calculate remaining credits after equipment purchase
        equipment_cost = character.equipment.total_cost()
        character.credits = max(0, starting_credits - equipment_cost)

        return character

    def _generate_random_name(self) -> str:
        """
        Generate a random character name.

        Returns:
            Random name string
        """
        first_names = [
            "Kara", "Drake", "Lyra", "Rex", "Nova", "Zane", "Maya", "Cole",
            "Aria", "Jax", "Luna", "Vex", "Sage", "Kai", "Echo", "Finn",
            "Nyx", "Dex", "Vera", "Orion", "Skye", "Nash", "Iris", "Rafe"
        ]

        last_names = [
            "Voss", "Kane", "Storm", "Cross", "Vale", "Reeves", "Drake", "Stone",
            "Night", "Fox", "Ryder", "Hayes", "West", "Black", "Chase", "Hunt",
            "Wells", "Reed", "Blake", "Wolf", "Cole", "Grey", "Steele", "Quinn"
        ]

        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def generate_multiple(self, count: int, **kwargs) -> List[Character]:
        """
        Generate multiple characters.

        Args:
            count: Number of characters to generate
            **kwargs: Arguments to pass to generate_character

        Returns:
            List of Character instances
        """
        return [self.generate_character(**kwargs) for _ in range(count)]
