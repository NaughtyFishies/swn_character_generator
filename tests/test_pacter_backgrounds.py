#!/usr/bin/env python3
"""Test Pacter-specific backgrounds."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Pacter-Specific Backgrounds")
print("=" * 70)

# Test 1: Pacter Chosen
print("\nTest 1: Pacter Chosen background")
print("-" * 70)

chosen = gen.generate_character(
    name="Test Chosen",
    level=1,
    class_choice="Pacter",
    background_choice="Pacter Chosen",
    attribute_method="array"
)

print(f"Character: {chosen.name}")
print(f"Class: {chosen.character_class.name}")
print(f"Background: {chosen.background.name}")
print(f"Class-specific: {chosen.background.class_specific}")

# Check for Cast Magic skill
has_cast = chosen.skills.has_skill("Cast Magic")
print(f"\nHas Cast Magic skill: {has_cast}")
if has_cast:
    level = chosen.skills.get_level("Cast Magic")
    print(f"Cast Magic level: {level} (should be at least -1 for free skill)")

# Test 2: Pacter Controller
print("\n\nTest 2: Pacter Controller background")
print("-" * 70)

controller = gen.generate_character(
    name="Test Controller",
    level=1,
    class_choice="Pacter",
    background_choice="Pacter Controller",
    attribute_method="array"
)

print(f"Character: {controller.name}")
print(f"Class: {controller.character_class.name}")
print(f"Background: {controller.background.name}")
print(f"Class-specific: {controller.background.class_specific}")

# Check for Cast Magic skill
has_cast = controller.skills.has_skill("Cast Magic")
print(f"\nHas Cast Magic skill: {has_cast}")
if has_cast:
    level = controller.skills.get_level("Cast Magic")
    print(f"Cast Magic level: {level}")

# Test 3: Pacter Dragoman
print("\n\nTest 3: Pacter Dragoman background")
print("-" * 70)

dragoman = gen.generate_character(
    name="Test Dragoman",
    level=1,
    class_choice="Pacter",
    background_choice="Pacter Dragoman",
    attribute_method="array"
)

print(f"Character: {dragoman.name}")
print(f"Class: {dragoman.character_class.name}")
print(f"Background: {dragoman.background.name}")
print(f"Class-specific: {dragoman.background.class_specific}")

# Check for Cast Magic and Know Magic skills
has_cast = dragoman.skills.has_skill("Cast Magic")
has_know_magic = dragoman.skills.has_skill("Know Magic")
print(f"\nHas Cast Magic skill: {has_cast}")
print(f"Has Know Magic skill: {has_know_magic}")
if has_cast:
    level = dragoman.skills.get_level("Cast Magic")
    print(f"Cast Magic level: {level}")
if has_know_magic:
    level = dragoman.skills.get_level("Know Magic")
    print(f"Know Magic level: {level}")

# Test 4: Background count verification
print("\n\nTest 4: Background count verification")
print("-" * 70)

general_bgs = gen.backgrounds.get_all_background_names(include_class_specific=False)
all_bgs = gen.backgrounds.get_all_background_names(include_class_specific=True)

print(f"General backgrounds: {len(general_bgs)}")
print(f"All backgrounds (including class-specific): {len(all_bgs)}")
print(f"Class-specific backgrounds: {len(all_bgs) - len(general_bgs)}")

# Count by class
pacter_specific = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == "Pacter"]

print(f"\nPacter-specific: {len(pacter_specific)}")

print("\nPacter-specific backgrounds:")
for bg in pacter_specific:
    print(f"  - {bg.name}: {bg.description}")

print("\n" + "=" * 70)
print("✓ Pacter background test complete!")
