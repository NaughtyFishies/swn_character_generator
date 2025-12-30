#!/usr/bin/env python3
"""Test that armor encumbrance restrictions work correctly."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Armor Encumbrance Restrictions")
print("=" * 70)

# Test 1: Magic classes get enc 0 unless they have Armored Technique
print("\nTest 1: Magic Classes (Arcane Expert, Arcane Warrior)")
print("-" * 70)
print(f"{'Character':20s} | {'Armor':25s} | {'Enc':3s} | {'Has Armored Tech':18s}")
print("-" * 70)

all_passed = True

for i in range(20):
    char = gen.generate_character(
        level=5,
        class_choice="Arcane Expert",
        attribute_method="array"
    )

    armor_enc = char.equipment.armor.enc if char.equipment.armor else 0
    armor_name = char.equipment.armor.name if char.equipment.armor else "None"

    # Check for Armored Technique focus
    armored_tech_focus = next((f for f in char.foci if f.name == "Armored Technique"), None)
    has_armored_tech = armored_tech_focus is not None
    armored_tech_level = armored_tech_focus.level if armored_tech_focus else 0

    # Verify encumbrance restriction
    expected_max_enc = 0
    if armored_tech_level == 1:
        expected_max_enc = 1
    elif armored_tech_level == 2:
        expected_max_enc = 2

    status = "✓" if armor_enc <= expected_max_enc else "❌"

    if armor_enc > expected_max_enc:
        all_passed = False

    tech_str = f"L{armored_tech_level}" if has_armored_tech else "No"
    if i < 5:  # Show first 5
        print(f"{char.name[:20]:20s} | {armor_name:25s} | {armor_enc:3d} | {tech_str:18s} | {status}")

if all_passed:
    print("\n✓ Magic classes respect enc 0 restriction (unless Armored Technique)")
else:
    print("\n❌ Magic classes got heavy armor without Armored Technique!")

# Test 2: Heavy warriors can use enc 2
print("\n\nTest 2: Heavy Warrior Classes (Warrior)")
print("-" * 70)
print(f"{'Character':20s} | {'Armor':25s} | {'Enc':3s} | {'Status':6s}")
print("-" * 70)

all_valid = True
enc_2_found = False

for i in range(10):
    char = gen.generate_character(
        level=10,
        class_choice="Warrior",
        attribute_method="array"
    )

    armor_enc = char.equipment.armor.enc if char.equipment.armor else 0
    armor_name = char.equipment.armor.name if char.equipment.armor else "None"

    if armor_enc == 2:
        enc_2_found = True

    status = "✓" if armor_enc <= 2 else "❌"

    if armor_enc > 2:
        all_valid = False

    if i < 5:  # Show first 5
        print(f"{char.name[:20]:20s} | {armor_name:25s} | {armor_enc:3d} | {status:6s}")

if all_valid and enc_2_found:
    print("\n✓ Warriors can use enc 2 armor")
elif all_valid:
    print("\n⚠ Warriors respect enc 2 limit but didn't get enc 2 in sample (OK)")
else:
    print("\n❌ Warriors got armor heavier than enc 2!")

# Test 3: Normal classes prefer enc 1
print("\n\nTest 3: Normal Classes (Expert, Adventurer)")
print("-" * 70)
print(f"{'Character':20s} | {'Class':15s} | {'Armor':25s} | {'Enc':3s}")
print("-" * 70)

all_valid = True

for class_choice in ["Expert", "Adventurer"]:
    for i in range(3):
        char = gen.generate_character(
            level=5,
            class_choice=class_choice,
            attribute_method="array"
        )

        armor_enc = char.equipment.armor.enc if char.equipment.armor else 0
        armor_name = char.equipment.armor.name if char.equipment.armor else "None"

        if armor_enc > 1:
            all_valid = False

        print(f"{char.name[:20]:20s} | {class_choice:15s} | {armor_name:25s} | {armor_enc:3d}")

if all_valid:
    print("\n✓ Normal classes use enc 0-1 armor")
else:
    print("\n❌ Normal classes got heavy armor!")

# Test 4: Encumbrance distribution
print("\n\nTest 4: Encumbrance Distribution (100 characters per class)")
print("-" * 70)

results = {}

for class_choice in ["Arcane Expert", "Warrior", "Expert"]:
    enc_counts = {0: 0, 1: 0, 2: 0}

    for i in range(100):
        char = gen.generate_character(
            level=5,
            class_choice=class_choice,
            attribute_method="array"
        )

        armor_enc = char.equipment.armor.enc if char.equipment.armor else 0
        enc_counts[armor_enc] = enc_counts.get(armor_enc, 0) + 1

    results[class_choice] = enc_counts

for class_name, enc_counts in results.items():
    print(f"\n{class_name}:")
    print(f"  Enc 0: {enc_counts[0]:3d} ({enc_counts[0]}%)")
    print(f"  Enc 1: {enc_counts[1]:3d} ({enc_counts[1]}%)")
    print(f"  Enc 2: {enc_counts[2]:3d} ({enc_counts[2]}%)")

print("\n" + "=" * 70)
print("✓ Armor encumbrance restriction test complete!")
