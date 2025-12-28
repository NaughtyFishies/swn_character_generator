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

        # Step 1: Get power level
        print("Choose character power level:")
        print("  1. Weak - Below average stats, fewer skills, basic foci only")
        print("  2. Normal - Standard game balance (recommended)")
        print("  3. Strong - Above average stats, more skills, access to exotic foci")
        print()

        power_level = self._prompt_choice(
            "Select power level (1-3): ",
            {"1": "weak", "2": "normal", "3": "strong"},
            default="2"
        )

        # Step 2: Get power type
        print("\nChoose power type:")
        print("  1. Normal - Standard character, no psychic abilities")
        print("  2. Magic - Character with 1-2 psychic disciplines")
        print("  3. Psionic - Powerful psychic with 2-3 disciplines")
        print()

        power_type = self._prompt_choice(
            "Select power type (1-3): ",
            {"1": "normal", "2": "magic", "3": "psionic"},
            default="1"
        )

        # Step 3: Get class
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

        # Step 4: Get name
        print("\nEnter character name (press Enter for random name):")
        name = input("> ").strip()
        if not name:
            name = None

        # Step 5: Generate character
        print("\nGenerating character...")
        print()

        character = self.generator.generate_character(
            name=name,
            power_level=power_level,
            power_type=power_type,
            class_choice=class_choice
        )

        # Step 6: Display result
        CharacterDisplay.print_character(character)

        # Step 7: Offer to save
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

        # Step 8: Offer to generate another
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
