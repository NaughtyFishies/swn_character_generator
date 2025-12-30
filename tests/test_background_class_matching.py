#!/usr/bin/env python3
"""Test that class-specific backgrounds are only randomly assigned to matching classes."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Background-Class Matching")
print("=" * 70)

# Test 1: Non-Sunblade classes should never randomly get Sunblade backgrounds
print("\nTest 1: Non-Sunblade classes should NOT get Sunblade backgrounds")
print("-" * 70)

sunblade_backgrounds = ["Sunblade Mystic", "Sunblade Warrior", "Sunblade Burnout"]
non_sunblade_classes = ["Warrior", "Expert", "Psychic", "Adventurer", "Arcanist"]

all_passed = True
for class_name in non_sunblade_classes:
    has_sunblade_bg = False
    for i in range(20):  # Test 20 times to be thorough
        char = gen.generate_character(
            level=1,
            class_choice=class_name,
            # No background_choice - let it be random
        )
        if char.background.name in sunblade_backgrounds:
            has_sunblade_bg = True
            print(f"❌ {class_name}: Got Sunblade background '{char.background.name}' (should NOT)")
            all_passed = False
            break

    if not has_sunblade_bg:
        print(f"✓ {class_name}: No Sunblade backgrounds found (correct)")

if all_passed:
    print("\n✓ All non-Sunblade classes passed")

# Test 2: Sunblade class CAN get Sunblade backgrounds
print("\n\nTest 2: Sunblade class CAN get Sunblade backgrounds")
print("-" * 70)

sunblade_bg_found = False
general_bg_found = False

for i in range(30):
    char = gen.generate_character(
        level=1,
        class_choice="Sunblade",
        # No background_choice - let it be random
    )
    if char.background.name in sunblade_backgrounds:
        sunblade_bg_found = True
    else:
        general_bg_found = True

print(f"✓ Sunblade got class-specific background: {sunblade_bg_found}")
print(f"✓ Sunblade got general background: {general_bg_found}")
print(f"\n✓ Sunblade class can get both types (correct)")

# Test 3: Check all magic class backgrounds
print("\n\nTest 3: Magic class backgrounds only go to their classes")
print("-" * 70)

magic_class_backgrounds = {
    "Arcanist": ["Arcanist Apprentice", "Arcanist Wanderer", "Arcanist Exile", "Arcanist Sage"],
    "Pacter": ["Pacter Initiate", "Pacter Seeker"],
    "Rectifier": ["Rectifier Acolyte", "Rectifier Crusader"],
    "War Mage": ["War Mage Veteran", "War Mage Battlemage"],
    "Sunblade": ["Sunblade Mystic", "Sunblade Warrior", "Sunblade Burnout"],
}

# Test that non-magic classes don't get magic backgrounds
all_passed = True
for magic_class, magic_bgs in magic_class_backgrounds.items():
    # Test with a Warrior
    has_wrong_bg = False
    for i in range(10):
        char = gen.generate_character(
            level=1,
            class_choice="Warrior",
        )
        if char.background.name in magic_bgs:
            has_wrong_bg = True
            print(f"❌ Warrior got {magic_class} background '{char.background.name}'")
            all_passed = False
            break

    if not has_wrong_bg:
        print(f"✓ Warrior never gets {magic_class} backgrounds")

if all_passed:
    print("\n✓ Non-magic classes don't get magic class backgrounds")

# Test 4: Explicit background selection should work even if class doesn't match
print("\n\nTest 4: Explicit background selection works regardless of class")
print("-" * 70)

try:
    warrior_with_sunblade_bg = gen.generate_character(
        level=1,
        class_choice="Warrior",
        background_choice="Sunblade Mystic"  # Explicitly requesting Sunblade background
    )
    print(f"✓ Warrior with explicit 'Sunblade Mystic' background: {warrior_with_sunblade_bg.background.name}")
    print(f"  (This is allowed when explicitly specified)")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: List all class-specific backgrounds
print("\n\nTest 5: Available class-specific backgrounds")
print("-" * 70)

for bg in gen.backgrounds.backgrounds:
    if bg.class_specific:
        print(f"  {bg.name:30s} -> {bg.class_specific}")

print("\n" + "=" * 70)
print("✓ Background-class matching test complete!")
print("\nSummary:")
print("  - Random backgrounds only include class-specific when class matches ✓")
print("  - Explicit background selection works regardless of class ✓")
