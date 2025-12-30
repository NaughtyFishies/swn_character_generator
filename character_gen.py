#!/usr/bin/env python3
"""
Stars Without Number Character Generator
Main entry point for CLI and interactive character generation.
"""
import argparse
import sys
from pathlib import Path

from swn.generator import CharacterGenerator
from swn.display import CharacterDisplay
from swn.interactive import InteractivePrompt


def main():
    """Main entry point for character generator."""
    parser = argparse.ArgumentParser(
        description="Generate characters for Stars Without Number RPG"
    )

    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )

    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Generate a completely random character"
    )

    parser.add_argument(
        "--name", "-n",
        type=str,
        help="Character name (random if not specified)"
    )

    parser.add_argument(
        "--class", "-c",
        dest="char_class",
        help="Character class (random if not specified)"
    )

    parser.add_argument(
        "--background", "-b",
        dest="background",
        help="Character background (random if not specified)"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of characters to generate (default: 1)"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Save character to file"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Export character as JSON"
    )

    args = parser.parse_args()

    # Initialize generator
    try:
        generator = CharacterGenerator()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Make sure you're running from the character_generator directory.", file=sys.stderr)
        sys.exit(1)

    # Interactive mode
    if args.interactive:
        prompt = InteractivePrompt(generator)
        prompt.run()
        return

    # Generate character(s)
    try:
        if args.count == 1:
            character = generator.generate_character(
                name=args.name,
                class_choice=args.char_class,
                background_choice=args.background
            )

            # Display character
            CharacterDisplay.print_character(character)

            # Save to file if requested
            if args.output:
                if args.json:
                    CharacterDisplay.export_json(character, args.output)
                    print(f"\nCharacter exported to {args.output}")
                else:
                    CharacterDisplay.save_to_file(character, args.output)
                    print(f"\nCharacter saved to {args.output}")

        else:
            # Generate multiple characters
            characters = generator.generate_multiple(
                args.count,
                name=None,  # Always random names for batch
                class_choice=args.char_class,
                background_choice=args.background
            )

            for i, character in enumerate(characters, 1):
                print(f"\n{'='*70}")
                print(f"CHARACTER {i} OF {args.count}".center(70))
                print(f"{'='*70}\n")
                CharacterDisplay.print_character(character)

                # Save each character if output specified
                if args.output:
                    base_name = Path(args.output).stem
                    ext = Path(args.output).suffix
                    filename = f"{base_name}_{i}{ext}"

                    if args.json:
                        CharacterDisplay.export_json(character, filename)
                    else:
                        CharacterDisplay.save_to_file(character, filename)

            if args.output:
                print(f"\n{args.count} characters saved with base name {args.output}")

    except Exception as e:
        print(f"Error generating character: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
