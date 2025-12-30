#!/usr/bin/env python3
"""Test Sunblade-specific backgrounds."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Sunblade-Specific Backgrounds")
print("=" * 70)

# Test 1: Sunblade Mystic
print("\nTest 1: Sunblade Mystic background")
print("-" * 70)

mystic = gen.generate_character(
    name="Test Mystic",
    level=1,
    class_choice="Sunblade",
    background_choice="Sunblade Mystic",
    attribute_method="array"
)

print(f"Character: {mystic.name}")
print(f"Class: {mystic.character_class.name}")
print(f"Background: {mystic.background.name}")
print(f"Class-specific: {mystic.background.class_specific}")

# Check for Sunblade skill
has_sunblade = mystic.skills.has_skill("Sunblade")
print(f"\nHas Sunblade skill: {has_sunblade}")
if has_sunblade:
    level = mystic.skills.get_level("Sunblade")
    print(f"Sunblade level: {level}")

# Test 2: Sunblade Warrior
print("\n\nTest 2: Sunblade Warrior background")
print("-" * 70)

warrior = gen.generate_character(
    name="Test Warrior",
    level=1,
    class_choice="Sunblade",
    background_choice="Sunblade Warrior",
    attribute_method="array"
)

print(f"Character: {warrior.name}")
print(f"Class: {warrior.character_class.name}")
print(f"Background: {warrior.background.name}")
print(f"Class-specific: {warrior.background.class_specific}")

# Check for Sunblade skill and combat skills
has_sunblade = warrior.skills.has_skill("Sunblade")
print(f"\nHas Sunblade skill: {has_sunblade}")
if has_sunblade:
    level = warrior.skills.get_level("Sunblade")
    print(f"Sunblade level: {level}")

# Test 3: Sunblade Burnout
print("\n\nTest 3: Sunblade Burnout background")
print("-" * 70)

burnout = gen.generate_character(
    name="Test Burnout",
    level=1,
    class_choice="Sunblade",
    background_choice="Sunblade Burnout",
    attribute_method="array"
)

print(f"Character: {burnout.name}")
print(f"Class: {burnout.character_class.name}")
print(f"Background: {burnout.background.name}")
print(f"Class-specific: {burnout.background.class_specific}")

# Check for Sunblade skill
has_sunblade = burnout.skills.has_skill("Sunblade")
print(f"\nHas Sunblade skill: {has_sunblade}")
if has_sunblade:
    level = burnout.skills.get_level("Sunblade")
    print(f"Sunblade level: {level}")

# Test 4: Background count verification
print("\n\nTest 4: Background count verification")
print("-" * 70)

general_bgs = gen.backgrounds.get_all_background_names(include_class_specific=False)
all_bgs = gen.backgrounds.get_all_background_names(include_class_specific=True)

print(f"General backgrounds: {len(general_bgs)}")
print(f"All backgrounds (including class-specific): {len(all_bgs)}")
print(f"Class-specific backgrounds: {len(all_bgs) - len(general_bgs)}")

# Count by class
sunblade_specific = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == "Sunblade"]

print(f"\nSunblade-specific: {len(sunblade_specific)}")

print("\nSunblade-specific backgrounds:")
for bg in sunblade_specific:
    print(f"  - {bg.name}: {bg.description}")

print("\n" + "=" * 70)
print("✓ Sunblade background test complete!")
