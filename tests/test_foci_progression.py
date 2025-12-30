#!/usr/bin/env python3
"""Test foci progression across character levels."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Foci Progression")
print("=" * 70)

# Test different classes at different levels
test_cases = [
    # (class_name, level, expected_foci, description)
    ("Warrior", 1, 2, "Level 1 Warrior: 1 base + 1 combat bonus"),
    ("Warrior", 2, 3, "Level 2 Warrior: 1 base + 1 from level 2 + 1 combat bonus"),
    ("Warrior", 5, 4, "Level 5 Warrior: 1 base + 2 from levels (2,5) + 1 combat bonus"),
    ("Warrior", 7, 5, "Level 7 Warrior: 1 base + 3 from levels (2,5,7) + 1 combat bonus"),
    ("Warrior", 10, 6, "Level 10 Warrior: 1 base + 4 from levels (2,5,7,10) + 1 combat bonus"),

    ("Expert", 1, 2, "Level 1 Expert: 1 base + 1 non-combat bonus"),
    ("Expert", 10, 6, "Level 10 Expert: 1 base + 4 from levels + 1 non-combat bonus"),

    ("Psychic", 1, 1, "Level 1 Psychic: 1 base only"),
    ("Psychic", 10, 5, "Level 10 Psychic: 1 base + 4 from levels"),

    ("Adventurer", 1, 2, "Level 1 Adventurer: 2 base"),
    ("Adventurer", 10, 6, "Level 10 Adventurer: 2 base + 4 from levels"),

    ("Arcanist", 1, 1, "Level 1 Arcanist: 1 base only"),
    ("Arcanist", 10, 5, "Level 10 Arcanist: 1 base + 4 from levels"),
]

print("\nTesting Foci Count by Level:")
print("-" * 70)

for class_name, level, expected, description in test_cases:
    char = gen.generate_character(
        level=level,
        class_choice=class_name,
        attribute_method="array"
    )

    actual = len(char.foci)
    status = "✓" if actual == expected else "❌"

    print(f"{status} {description}")
    print(f"   Expected: {expected}, Got: {actual}")
    if actual != expected:
        print(f"   Foci: {[f.name for f in char.foci]}")
    print()

# Detailed test for a level 10 Warrior
print("\nDetailed Level 10 Warrior Test:")
print("-" * 70)

warrior10 = gen.generate_character(
    name="Test Warrior",
    level=10,
    class_choice="Warrior",
    attribute_method="array"
)

print(f"Character: {warrior10.name}")
print(f"Class: {warrior10.character_class.name}")
print(f"Level: {warrior10.level}")
print(f"Total Foci: {len(warrior10.foci)} (expected: 6)")

combat_foci = ["Armsman", "Close Combatant", "Gunslinger", "Shocking Assault",
               "Sniper", "Unarmed Combatant", "Assassin"]

print(f"\nFoci List:")
for i, focus in enumerate(warrior10.foci, 1):
    is_combat = "COMBAT" if focus.name in combat_foci else "non-combat"
    print(f"  {i}. {focus.name} ({is_combat})")

# Check that at least one is combat (the class bonus)
has_combat = any(f.name in combat_foci for f in warrior10.foci)
print(f"\nHas combat focus (required for Warrior): {has_combat}")

# Detailed test for a level 10 Expert
print("\n\nDetailed Level 10 Expert Test:")
print("-" * 70)

expert10 = gen.generate_character(
    name="Test Expert",
    level=10,
    class_choice="Expert",
    attribute_method="array"
)

print(f"Character: {expert10.name}")
print(f"Class: {expert10.character_class.name}")
print(f"Level: {expert10.level}")
print(f"Total Foci: {len(expert10.foci)} (expected: 6)")

print(f"\nFoci List:")
for i, focus in enumerate(expert10.foci, 1):
    is_combat = "COMBAT" if focus.name in combat_foci else "non-combat"
    is_psychic = "PSYCHIC" if focus.psychic_only else ""
    print(f"  {i}. {focus.name} ({is_combat} {is_psychic})")

# Check constraints
has_psychic = any(f.psychic_only for f in expert10.foci)
all_combat = all(f.name in combat_foci for f in expert10.foci)

print(f"\nHas psychic focus (should be NO for Expert bonus): {has_psychic}")
print(f"All combat foci (should be NO, needs non-combat bonus): {all_combat}")

print("\n" + "=" * 70)
print("✓ Foci progression test complete!")
