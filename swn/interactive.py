"""Interactive character generation interface."""
from swn.generator import CharacterGenerator
from swn.display import CharacterDisplay


class InteractivePrompt:
    """Handles interactive character creation flow."""

    def __init__(self, generator: CharacterGenerator):
        """
        Initialize interactive prompt.

        Args:
            generator: CharacterGenerator instance
        """
        self.generator = generator

    def run(self):
        """Run the interactive character generation flow."""
        print("\n" + "=" * 70)
        print("STARS WITHOUT NUMBER CHARACTER GENERATOR".center(70))
        print("=" * 70)
        print()

        # Step 1: Get class
        print("\nChoose character class:")
        print("  1. Warrior - Combat specialist with high HP and attack bonus")
        print("  2. Expert - Skill specialist with many skill points")
        print("  3. Psychic - Psychic powers user")
        print("  4. Adventurer - Versatile character with 2 foci")
        print("  5. Random")
        print()

        class_map = {
            "1": "Warrior",
            "2": "Expert",
            "3": "Psychic",
            "4": "Adventurer",
            "5": None
        }

        class_choice = self._prompt_choice(
            "Select class (1-5): ",
            class_map,
            default="5"
        )

        # Step 2: Get background
        print("\nChoose character background:")
        print("  1. Random")
        print("  2. Barbarian - From a savage world of low technology")
        print("  3. Soldier - Professional fighter or military veteran")
        print("  4. Spacer - Voidborn worker in space")
        print("  5. Technician - Engineer or mechanic")
        print("  6. Physician - Doctor or medic")
        print("  7. Scholar - Scientist or professor")
        print("  8. Criminal - Thief, smuggler, or spy")
        print("  9. See full list...")
        print()

        bg_choice = input("Select background (1-9): ").strip()

        if bg_choice == "9":
            # Show full list
            print("\nAll available backgrounds:")
            bg_names = self.generator.backgrounds.get_all_background_names()
            for i, bg_name in enumerate(bg_names, 1):
                print(f"  {i}. {bg_name}")
            print()
            bg_input = input(f"Select background (1-{len(bg_names)}) or name: ").strip()

            # Try to parse as number
            try:
                bg_idx = int(bg_input) - 1
                if 0 <= bg_idx < len(bg_names):
                    background_choice = bg_names[bg_idx]
                else:
                    background_choice = None
            except ValueError:
                # Treat as name
                background_choice = bg_input if bg_input else None
        else:
            bg_map = {
                "1": None,
                "2": "Barbarian",
                "3": "Soldier",
                "4": "Spacer",
                "5": "Technician",
                "6": "Physician",
                "7": "Scholar",
                "8": "Criminal"
            }
            background_choice = bg_map.get(bg_choice, None)

        # Step 3: Get name
        print("\nEnter character name (press Enter for random name):")
        name = input("> ").strip()
        if not name:
            name = None

        # Step 4: Generate character
        print("\nGenerating character...")
        print()

        character = self.generator.generate_character(
            name=name,
            class_choice=class_choice,
            background_choice=background_choice
        )

        # Step 5: Display result
        CharacterDisplay.print_character(character)

        # Step 6: Offer to save
        print("\nWould you like to save this character to a file? (y/n): ", end="")
        save_choice = input().strip().lower()

        if save_choice in ["y", "yes"]:
            default_filename = f"{character.name.replace(' ', '_').lower()}.txt"
            print(f"Enter filename (default: {default_filename}): ", end="")
            filename = input().strip()
            if not filename:
                filename = default_filename

            CharacterDisplay.save_to_file(character, filename)
            print(f"\nCharacter saved to {filename}")

        # Step 7: Offer to generate another
        print("\nGenerate another character? (y/n): ", end="")
        again = input().strip().lower()

        if again in ["y", "yes"]:
            print("\n")
            self.run()
        else:
            print("\nThank you for using the SWN Character Generator!")

    def _prompt_choice(self, prompt: str, choices: dict, default: str = None) -> str:
        """
        Prompt user for a choice from a set of options.

        Args:
            prompt: Prompt text
            choices: Dictionary mapping input values to result values
            default: Default choice if user presses Enter

        Returns:
            Selected value from choices dict
        """
        while True:
            user_input = input(prompt).strip()

            if not user_input and default:
                return choices[default]

            if user_input in choices:
                return choices[user_input]

            print(f"Invalid choice. Please enter one of: {', '.join(choices.keys())}")
