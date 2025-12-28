"""Character display and formatting for console output."""
import json
from swn.character import Character


class CharacterDisplay:
    """Handles character sheet formatting and output."""

    @staticmethod
    def format_character_sheet(character: Character) -> str:
        """
        Create formatted character sheet for console display.

        Args:
            character: Character to format

        Returns:
            Formatted character sheet string
        """
        lines = []

        # Header
        lines.append("=" * 70)
        lines.append(f"CHARACTER: {character.name}".center(70))
        class_name = character.character_class.name if character.character_class else "Unknown"
        bg_name = character.background.name if character.background else "Unknown"
        lines.append(f"Class: {class_name} | Background: {bg_name}".center(70))
        lines.append(f"Level: {character.level} | Type: {character.power_type.title()}".center(70))
        lines.append("=" * 70)
        lines.append("")

        # Attributes
        lines.append("ATTRIBUTES")
        lines.append("-" * 70)
        if character.attributes:
            attr_pairs = [
                ("STR", "DEX", "CON"),
                ("INT", "WIS", "CHA")
            ]
            for attr_row in attr_pairs:
                attr_strs = []
                for attr in attr_row:
                    score = character.attributes.get_score(attr)
                    mod = character.attributes.get_modifier(attr)
                    mod_str = f"+{mod}" if mod >= 0 else str(mod)
                    attr_strs.append(f"{attr}: {score:2d} ({mod_str:>3})")
                lines.append("    ".join(attr_strs))
        lines.append("")

        # Skills
        lines.append("SKILLS")
        lines.append("-" * 70)
        if character.skills:
            skills_list = character.skills.get_all_skills()
            if skills_list:
                # Group skills into rows of 4
                skill_strs = [str(skill) for skill in skills_list]
                for i in range(0, len(skill_strs), 4):
                    row = skill_strs[i:i+4]
                    lines.append(", ".join(row))
            else:
                lines.append("No skills")
        lines.append("")

        # Foci
        lines.append("FOCI")
        lines.append("-" * 70)
        if character.foci:
            for focus in character.foci:
                lines.append(f"[{focus.name}]")
                lines.append(f"  {focus.level_1}")
                lines.append("")
        else:
            lines.append("No foci")
            lines.append("")

        # Psychic Powers
        if character.psychic_powers:
            lines.append("PSYCHIC POWERS")
            lines.append("-" * 70)
            lines.append(f"Effort Pool: {character.psychic_powers.effort_pool}")
            lines.append("")

            # Display each discipline the character has
            psychic_disciplines = ["Biopsionics", "Metapsionics", "Precognition",
                                  "Telekinesis", "Telepathy", "Teleportation"]

            for disc_name in psychic_disciplines:
                if character.skills and character.skills.has_skill(disc_name):
                    skill_level = character.skills.get_level(disc_name)
                    lines.append(f"{disc_name} (Level {skill_level}):")

                    # Get chosen techniques for this discipline
                    chosen_techs = character.psychic_powers.get_techniques(disc_name)
                    for tech in chosen_techs:
                        effort_str = f"({tech.effort_cost} Effort)" if tech.effort_cost > 0 else ""
                        lines.append(f"  - {tech.name} {effort_str}")
                        if len(tech.description) > 80:
                            # Truncate long descriptions for display
                            lines.append(f"    {tech.description[:77]}...")
                        else:
                            lines.append(f"    {tech.description}")
                    lines.append("")

        # Spells
        if character.spells:
            lines.append("SPELLS")
            lines.append("-" * 70)
            lines.append(f"Spell Tradition: {character.spells.tradition}")
            lines.append(f"Known Spells: {len(character.spells.known_spells)}")
            lines.append("")

            # Show spell slots per level
            if character.spells.spell_slots:
                lines.append("Spell Slots per Day:")
                for level in range(1, 6):
                    slots = character.spells.get_spell_slots(level)
                    if slots > 0:
                        level_spells = character.spells.get_spells_by_level(level)
                        lines.append(f"  Level {level}: {len(level_spells)} known / {slots} slots")
                lines.append("")

            # Group spells by level
            for level in range(1, 6):
                level_spells = character.spells.get_spells_by_level(level)
                if level_spells:
                    lines.append(f"Level {level} Spells:")
                    for spell in level_spells:
                        lines.append(f"  - {spell.name}")
                        lines.append(f"    {spell.description}")
                    lines.append("")

        # Combat Stats
        lines.append("COMBAT")
        lines.append("-" * 70)
        lines.append(f"Hit Points: {character.hp}")
        lines.append(f"Attack Bonus: +{character.attack_bonus}")
        if character.saving_throws:
            saves_str = ", ".join([f"{k}: {v}" for k, v in character.saving_throws.items()])
            lines.append(f"Saving Throws: {saves_str}")
        lines.append("")

        # Class Abilities
        if character.character_class and character.character_class.special_abilities:
            lines.append("SPECIAL ABILITIES")
            lines.append("-" * 70)
            for ability in character.character_class.special_abilities:
                lines.append(f"- {ability}")
            lines.append("")

        # Equipment
        if character.equipment:
            lines.append("EQUIPMENT")
            lines.append("-" * 70)
            lines.append(f"Credits: {character.credits} cr remaining")
            lines.append(f"Total Value: {character.equipment.total_cost()} cr")
            lines.append(f"Total Encumbrance: {character.equipment.total_encumbrance()}")
            lines.append("")

            # Armor
            if character.equipment.armor:
                armor = character.equipment.armor
                ac_display = armor.properties.get("ac", "10")
                lines.append(f"Armor: {armor.name} (AC {ac_display}, TL{armor.tech_level})")

            # Weapons
            if character.equipment.weapons:
                lines.append("Weapons:")
                for weapon in character.equipment.weapons:
                    damage = weapon.properties.get("damage", "")
                    range_val = weapon.properties.get("range", "")
                    burst = " (burst)" if weapon.properties.get("burst") else ""
                    shock = weapon.properties.get("shock", "")
                    if damage and range_val:
                        lines.append(f"  - {weapon.name}: {damage} damage, {range_val}m{burst} (TL{weapon.tech_level})")
                    elif damage and shock:
                        lines.append(f"  - {weapon.name}: {damage} damage, Shock {shock} (TL{weapon.tech_level})")

            # Gear
            if character.equipment.gear:
                lines.append("Gear:")
                for item in character.equipment.gear:
                    lines.append(f"  - {item.name} (TL{item.tech_level})")
            lines.append("")

        # Footer
        lines.append("=" * 70)

        return "\n".join(lines)

    @staticmethod
    def save_to_file(character: Character, filename: str):
        """
        Save character sheet to text file.

        Args:
            character: Character to save
            filename: Output filename
        """
        sheet = CharacterDisplay.format_character_sheet(character)
        with open(filename, 'w') as f:
            f.write(sheet)

    @staticmethod
    def export_json(character: Character, filename: str):
        """
        Export character as JSON.

        Args:
            character: Character to export
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump(character.to_dict(), f, indent=2)

    @staticmethod
    def print_character(character: Character):
        """
        Print character sheet to console.

        Args:
            character: Character to print
        """
        print(CharacterDisplay.format_character_sheet(character))
