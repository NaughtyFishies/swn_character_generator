#!/usr/bin/env python3
"""Test Rectifier-specific backgrounds."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Rectifier-Specific Backgrounds")
print("=" * 70)

# Test 1: Amender of Flesh
print("\nTest 1: Amender of Flesh background")
print("-" * 70)

amender = gen.generate_character(
    name="Test Amender",
    level=1,
    class_choice="Rectifier",
    background_choice="Amender of Flesh",
    attribute_method="array"
)

print(f"Character: {amender.name}")
print(f"Class: {amender.character_class.name}")
print(f"Background: {amender.background.name}")
print(f"Class-specific: {amender.background.class_specific}")

# Check for Cast Magic and Heal skills
has_cast = amender.skills.has_skill("Cast Magic")
has_heal = amender.skills.has_skill("Heal")
print(f"\nHas Cast Magic skill: {has_cast}")
print(f"Has Heal skill: {has_heal}")
if has_cast:
    level = amender.skills.get_level("Cast Magic")
    print(f"Cast Magic level: {level}")
if has_heal:
    level = amender.skills.get_level("Heal")
    print(f"Heal level: {level}")

# Test 2: Identity Artist
print("\n\nTest 2: Identity Artist background")
print("-" * 70)

artist = gen.generate_character(
    name="Test Artist",
    level=1,
    class_choice="Rectifier",
    background_choice="Identity Artist",
    attribute_method="array"
)

print(f"Character: {artist.name}")
print(f"Class: {artist.character_class.name}")
print(f"Background: {artist.background.name}")
print(f"Class-specific: {artist.background.class_specific}")

# Check for Cast Magic skill
has_cast = artist.skills.has_skill("Cast Magic")
print(f"\nHas Cast Magic skill: {has_cast}")
if has_cast:
    level = artist.skills.get_level("Cast Magic")
    print(f"Cast Magic level: {level}")

# Test 3: Vessel of Will
print("\n\nTest 3: Vessel of Will background")
print("-" * 70)

vessel = gen.generate_character(
    name="Test Vessel",
    level=1,
    class_choice="Rectifier",
    background_choice="Vessel of Will",
    attribute_method="array"
)

print(f"Character: {vessel.name}")
print(f"Class: {vessel.character_class.name}")
print(f"Background: {vessel.background.name}")
print(f"Class-specific: {vessel.background.class_specific}")

# Check for Cast Magic, Exert, and Survive skills
has_cast = vessel.skills.has_skill("Cast Magic")
has_exert = vessel.skills.has_skill("Exert")
has_survive = vessel.skills.has_skill("Survive")
print(f"\nHas Cast Magic skill: {has_cast}")
print(f"Has Exert skill: {has_exert}")
print(f"Has Survive skill: {has_survive}")
if has_cast:
    level = vessel.skills.get_level("Cast Magic")
    print(f"Cast Magic level: {level}")

# Test 4: Background count verification
print("\n\nTest 4: Background count verification")
print("-" * 70)

general_bgs = gen.backgrounds.get_all_background_names(include_class_specific=False)
all_bgs = gen.backgrounds.get_all_background_names(include_class_specific=True)

print(f"General backgrounds: {len(general_bgs)}")
print(f"All backgrounds (including class-specific): {len(all_bgs)}")
print(f"Class-specific backgrounds: {len(all_bgs) - len(general_bgs)}")

# Count by class
rectifier_specific = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == "Rectifier"]

print(f"\nRectifier-specific: {len(rectifier_specific)}")

print("\nRectifier-specific backgrounds:")
for bg in rectifier_specific:
    print(f"  - {bg.name}: {bg.description}")

# Show all class-specific backgrounds
print("\n\nAll class-specific backgrounds by class:")
for class_name in ["Arcanist", "Free Nexus", "Godhunter", "Pacter", "Rectifier"]:
    class_bgs = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == class_name]
    if class_bgs:
        print(f"\n{class_name} ({len(class_bgs)}):")
        for bg in class_bgs:
            print(f"  - {bg.name}")

print("\n" + "=" * 70)
print("✓ Rectifier background test complete!")
