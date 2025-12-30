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
from swn.models.sunblade import SunbladeAbilitySelector
from swn.models.yama_king import YamaKingAbilitySelector
from swn.models.godhunter import GodhunterAbilitySelector
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

        # Load Sunblade ability selector
        sunblade_file = data_dir / "sunblade_abilities.json"
        if sunblade_file.exists():
            self.sunblade_selector = SunbladeAbilitySelector.load_from_file(str(sunblade_file))
        else:
            self.sunblade_selector = None

        # Load Yama King ability selector
        yama_king_file = data_dir / "yama_king_abilities.json"
        if yama_king_file.exists():
            self.yama_king_selector = YamaKingAbilitySelector.load_from_file(str(yama_king_file))
        else:
            self.yama_king_selector = None

        # Load Godhunter ability selector
        godhunter_file = data_dir / "godhunter_abilities.json"
        if godhunter_file.exists():
            self.godhunter_selector = GodhunterAbilitySelector.load_from_file(str(godhunter_file))
        else:
            self.godhunter_selector = None

        # Load equipment selector
        self.equipment_selector = EquipmentSelector.load_from_files(data_dir)

    def generate_character(
        self,
        name: Optional[str] = None,
        level: int = 1,
        attribute_method: str = "roll",
        class_choice: Optional[str] = None,
        background_choice: Optional[str] = None,
        use_quick_skills: bool = True,
        tech_level: int = 4
    ) -> Character:
        """
        Generate a complete character using official SWN rules.

        Args:
            name: Character name (random if None)
            level: Character level (default 1)
            attribute_method: "roll" (3d6, pick one to 14) or "array" (14,12,11,10,9,7)
            class_choice: Class name or None for random
            background_choice: Background name or None for random
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

        # Step 2: Generate attributes using chosen method
        character.attributes = Attributes.roll_attributes(attribute_method)

        # Step 3: Assign or randomize class
        if class_choice:
            character.character_class = self.classes.get_class(class_choice)
        else:
            character.character_class = self.classes.get_random_class(exclude_psychic=False)

        # Set power type from class
        character.power_type = character.character_class.power_type

        # Step 4: Assign or randomize background
        if background_choice:
            character.background = self.backgrounds.get_background_by_name(background_choice)
            if not character.background:
                raise ValueError(f"Unknown background: {background_choice}")
        else:
            # Select random background filtered by class (includes class-specific + general)
            character.background = self.backgrounds.get_random_background(
                class_name=character.character_class.name
            )

        # Step 5: Initialize skills and apply background skills
        character.skills = SkillSet()

        # For "Any Skill" resolution, exclude psychic disciplines and class-specific skills
        psychic_disciplines = ["Biopsionics", "Metapsionics", "Precognition",
                              "Telekinesis", "Telepathy", "Teleportation"]
        class_specific_skills = ["Sunblade", "Cast Magic", "Know Magic"]

        # Build list of available skills for background selection
        # Exclude both psychic disciplines and class-specific skills
        background_available_skills = [
            s for s in self.all_skills
            if s not in psychic_disciplines and s not in class_specific_skills
        ]

        # Use resolve_free_skill() to handle "Any Combat", "Any Skill", and other special cases
        free_skill = character.background.resolve_free_skill(available_skills=background_available_skills)
        character.skills.add_skill(free_skill, -1)
        # select_quick_skill() also handles "Any Combat", "Any Skill", and other special cases
        quick_skill = character.background.select_quick_skill(available_skills=background_available_skills)
        character.skills.add_skill(quick_skill, 0)

        # Step 6: Add class starting skills (if applicable)
        # Grant psychic discipline bonus skills for Psychic class
        # Psychic class gets 2 psychic skill picks as bonus skills
        # Can pick same discipline twice to get level-1 and a free level-1 technique
        if character.character_class.name == "Psychic":
            psychic_disciplines = ["Biopsionics", "Metapsionics", "Precognition",
                                  "Telekinesis", "Telepathy", "Teleportation"]

            # Pick 2 bonus psychic skills (can be same or different)
            # For random generation, we'll randomly decide if same or different
            if random.random() < 0.3:  # 30% chance to specialize in one discipline
                # Pick same discipline twice -> level-1
                chosen_discipline = random.choice(psychic_disciplines)
                character.skills.add_skill(chosen_discipline, 1)
            else:
                # Pick two different disciplines -> level-0 each
                chosen_disciplines = random.sample(psychic_disciplines, 2)
                for disc_name in chosen_disciplines:
                    character.skills.add_skill(disc_name, 0)

        # Grant Sunblade skill for Sunblade class
        if character.character_class.name == "Sunblade":
            # Sunblades automatically get Sunblade skill at level 0
            character.skills.add_skill("Sunblade", 0)

        # Step 7: Calculate available skill points
        # Formula: (class base + INT modifier) + (3 points per level)
        int_mod = character.attributes.get_modifier("INT")
        base_from_class = character.character_class.skill_points_base + int_mod
        points_from_levels = 3 * character.level
        total_points = base_from_class + points_from_levels
        total_points = max(1, total_points)  # Minimum 1 skill point

        # Step 7.5: For Sunblade class, max out Sunblade skill first
        if character.character_class.name == "Sunblade":
            # Determine max skill level based on character level
            if character.level <= 2:
                max_sunblade_level = 1
            elif character.level <= 5:
                max_sunblade_level = 2
            elif character.level <= 8:
                max_sunblade_level = 3
            else:
                max_sunblade_level = 4

            # Spend points to max out Sunblade skill
            current_sunblade_level = character.skills.get_level("Sunblade")
            while current_sunblade_level < max_sunblade_level:
                # Cost to level up: (current_level + 1) + 1
                cost = current_sunblade_level + 2
                if cost <= total_points:
                    # Can afford to level up
                    current_sunblade_level += 1
                    character.skills.skills["Sunblade"].level = current_sunblade_level
                    total_points -= cost
                else:
                    # Can't afford more levels
                    break

        # Step 8: Allocate remaining skill points
        # Exclude psychic disciplines from random allocation unless character is psychic
        psychic_disciplines = ["Biopsionics", "Metapsionics", "Precognition",
                              "Telekinesis", "Telepathy", "Teleportation"]
        is_psychic = (character.power_type == "psionic")

        # Class-specific skills that should never be randomly allocated
        class_specific_skills = [
            "Sunblade",      # Only for Sunblade class
            "Cast Magic",    # Only for spellcaster classes
            "Know Magic"     # Only for magic-using classes
        ]

        # Filter skills list for allocation
        available_skills = [s for s in self.all_skills if s not in class_specific_skills]

        # Also exclude psychic disciplines for non-psychic characters
        if not is_psychic:
            available_skills = [s for s in available_skills if s not in psychic_disciplines]

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

        # Step 9: Select foci based on class and level
        # Base: Everyone gets 1 focus at level 1 (Adventurer gets 2)
        # Level progression: +1 focus at levels 2, 5, 7, and 10
        # Class bonuses: Warriors get +1 combat, Experts get +1 non-combat

        has_psychic = (character.power_type == "psionic")
        class_name = character.character_class.name

        # Determine combat foci (simplified - common combat foci)
        combat_foci_names = [
            "Armsman", "Close Combatant", "Gunslinger", "Shocking Assault", "Sniper",
            "Unarmed Combatant", "Assassin", "Mageblade", "Elemental Warrior",
            "Arcane Physique", "Blade Ward", "Soul Shield", "Weapon Unity"
        ]

        # Calculate total foci to grant
        base_foci = 2 if class_name == "Adventurer" else 1

        # Add foci from level progression (levels 2, 5, 7, 10)
        level_foci = sum(1 for threshold in [2, 5, 7, 10] if character.level >= threshold)

        # Add class-specific bonus foci
        class_bonus_foci = 0
        if class_name in ["Warrior", "Arcane Warrior", "Expert", "Arcane Expert"]:
            class_bonus_foci = 1

        total_foci = base_foci + level_foci + class_bonus_foci

        foci_list = []

        def can_add_or_upgrade_focus(focus_name: str, existing_foci: List) -> bool:
            """Check if we can add a new focus or upgrade an existing one."""
            existing_focus = next((f for f in existing_foci if f.name == focus_name), None)
            if existing_focus:
                # Can only upgrade if currently at level 1
                return existing_focus.level == 1
            # Can add if not incompatible with existing foci
            return True

        def add_or_upgrade_focus(focus: 'Focus', existing_foci: List):
            """Add a new focus or upgrade an existing level 1 focus to level 2."""
            existing_focus = next((f for f in existing_foci if f.name == focus.name), None)
            if existing_focus and existing_focus.level == 1:
                # Upgrade existing focus to level 2
                existing_focus.level = 2
            elif not existing_focus:
                # Add new focus at level 1
                import copy
                new_focus = copy.deepcopy(focus)
                new_focus.level = 1
                existing_foci.append(new_focus)

        # Select foci one at a time to ensure compatibility
        for i in range(total_foci):
            # Determine what type of focus this should be
            if i == 0:
                # First focus is always normal
                focus_type = "normal"
            elif class_name == "Adventurer" and i == 1:
                # Second focus for Adventurer is normal
                focus_type = "normal"
            elif class_name in ["Warrior", "Arcane Warrior"] and i == (base_foci + level_foci):
                # Last focus for Warriors must be combat
                focus_type = "combat"
            elif class_name in ["Expert", "Arcane Expert"] and i == (base_foci + level_foci):
                # Last focus for Experts must be non-combat, non-psychic
                focus_type = "non-combat"
            else:
                # All other foci are normal
                focus_type = "normal"

            # Select appropriate focus
            if focus_type == "combat":
                all_foci = self.foci_selector.foci
                available = [
                    f for f in all_foci
                    if f.name in combat_foci_names
                    and (f.allowed_classes is None or class_name in f.allowed_classes)
                    and can_add_or_upgrade_focus(f.name, foci_list)
                    and all(f.is_truly_incompatible_with(existing) for existing in foci_list)
                ]
                if available:
                    add_or_upgrade_focus(random.choice(available), foci_list)
            elif focus_type == "non-combat":
                all_foci = self.foci_selector.foci
                available = [
                    f for f in all_foci
                    if f.name not in combat_foci_names and not f.psychic_only
                    and (f.allowed_classes is None or class_name in f.allowed_classes)
                    and can_add_or_upgrade_focus(f.name, foci_list)
                    and all(f.is_truly_incompatible_with(existing) for existing in foci_list)
                ]
                if available:
                    add_or_upgrade_focus(random.choice(available), foci_list)
            else:  # normal
                selected = self.foci_selector.select_random_foci(
                    1, "normal", has_psychic, class_name
                )
                if selected:
                    # Check if we can add or upgrade this focus
                    focus_candidate = selected[0]
                    if (can_add_or_upgrade_focus(focus_candidate.name, foci_list)
                        and all(focus_candidate.is_truly_incompatible_with(existing) for existing in foci_list)):
                        add_or_upgrade_focus(focus_candidate, foci_list)
                    else:
                        # Try again with different focus
                        all_foci = self.foci_selector.foci
                        available = [
                            f for f in all_foci
                            if (f.allowed_classes is None or class_name in f.allowed_classes)
                            and can_add_or_upgrade_focus(f.name, foci_list)
                            and all(f.is_truly_incompatible_with(existing) for existing in foci_list)
                        ]
                        if available:
                            add_or_upgrade_focus(random.choice(available), foci_list)

        character.foci = foci_list

        # Step 10: Handle psychic powers
        # Generate psychic powers based on discipline skills
        if character.power_type == "psionic":
            # Get all discipline skills the character has
            psychic_disciplines = ["Biopsionics", "Metapsionics", "Precognition",
                                  "Telekinesis", "Telepathy", "Teleportation"]
            discipline_skills = {}
            for disc_name in psychic_disciplines:
                if character.skills.has_skill(disc_name):
                    discipline_skills[disc_name] = character.skills.get_level(disc_name)

            # Only create psychic powers if character has at least one discipline
            if discipline_skills:
                # Effort pool uses better of WIS or CON modifier
                effort_mod = max(
                    character.attributes.get_modifier("WIS"),
                    character.attributes.get_modifier("CON")
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

        # Step 10.6: Handle Sunblade abilities for Sunblade class
        if character.character_class.name == "Sunblade" and self.sunblade_selector:
            # Get Sunblade skill level
            sunblade_skill_level = character.skills.get_level("Sunblade")

            # Generate Sunblade abilities based on character level
            character.sunblade_abilities = self.sunblade_selector.create_sunblade_abilities(
                character.level,
                sunblade_skill_level
            )

        # Step 10.7: Handle Yama King abilities for Yama King class
        if character.character_class.name == "Yama King" and self.yama_king_selector:
            # Generate Yama King abilities based on character level
            character.yama_king_abilities = self.yama_king_selector.create_yama_king_abilities(
                character.level
            )

        # Step 10.8: Handle Godhunter abilities for Godhunter class
        if character.character_class.name == "Godhunter" and self.godhunter_selector:
            # Generate Godhunter abilities based on character level
            character.godhunter_abilities = self.godhunter_selector.create_godhunter_abilities(
                character.level
            )

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
            starting_credits,
            character.power_type,
            character.foci
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
