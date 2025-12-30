#!/usr/bin/env python3
"""Test that foci can be leveled up to level 2."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Foci Level System")
print("=" * 70)

# Generate many characters to see if any get level 2 foci
print("\nGenerating 50 level 10 Warriors to find level 2 foci:")
print("-" * 70)

level_2_foci_found = False
level_2_examples = []

for i in range(50):
    char = gen.generate_character(
        level=10,
        class_choice="Warrior",
        attribute_method="array"
    )

    for focus in char.foci:
        if focus.level == 2:
            level_2_foci_found = True
            level_2_examples.append((char.name, focus.name))
            if len(level_2_examples) <= 5:  # Show first 5 examples
                print(f"✓ Found: {char.name} has [{focus.name} - Level 2]")

if level_2_foci_found:
    print(f"\n✓ Level 2 foci system working! Found {len(level_2_examples)} characters with level 2 foci")
else:
    print("\n❌ No level 2 foci found in 50 characters (may need adjustment)")

# Show detailed example if we found one
if level_2_examples:
    print("\n\nDetailed Example with Level 2 Focus:")
    print("-" * 70)

    # Generate characters until we find one with a level 2 focus
    for i in range(100):
        char = gen.generate_character(
            name=f"Test Character {i}",
            level=10,
            class_choice="Warrior",
            attribute_method="array"
        )
        level_2_focus = next((f for f in char.foci if f.level == 2), None)
        if level_2_focus:
            print(f"Character: {char.name}")
            print(f"Level: {char.level}")
            print(f"\nAll Foci:")
            for focus in char.foci:
                level_str = f" - Level {focus.level}" if focus.level == 2 else ""
                print(f"  [{focus.name}{level_str}]")
                if focus.level == 2:
                    print(f"    Level 2 Benefit: {focus.level_2}")
                else:
                    print(f"    Level 1 Benefit: {focus.level_1}")
            break

# Test focus distribution
print("\n\nFocus Level Distribution (100 Level 10 Warriors):")
print("-" * 70)

level_1_count = 0
level_2_count = 0

for i in range(100):
    char = gen.generate_character(
        level=10,
        class_choice="Warrior",
        attribute_method="array"
    )
    for focus in char.foci:
        if focus.level == 1:
            level_1_count += 1
        elif focus.level == 2:
            level_2_count += 1

total_foci = level_1_count + level_2_count
print(f"Total foci granted: {total_foci}")
print(f"Level 1 foci: {level_1_count} ({100 * level_1_count / total_foci:.1f}%)")
print(f"Level 2 foci: {level_2_count} ({100 * level_2_count / total_foci:.1f}%)")

if level_2_count > 0:
    print("\n✓ Characters can get level 2 foci!")
else:
    print("\n⚠ No level 2 foci found - system may need tuning")

print("\n" + "=" * 70)
print("✓ Foci level system test complete!")
