#!/usr/bin/env python3
"""Test that class-specific skills are only granted to appropriate classes."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Class-Specific Skill Restrictions")
print("=" * 70)

# Test 1: Non-Sunblades should never have Sunblade skill
print("\nTest 1: Non-Sunblade classes should NOT have Sunblade skill")
print("-" * 70)

non_sunblade_classes = ["Warrior", "Expert", "Psychic", "Adventurer",
                        "Arcanist", "Arcane Warrior", "Arcane Expert"]

all_passed = True
for class_name in non_sunblade_classes:
    # Generate 10 characters of each class
    has_sunblade_skill = False
    for i in range(10):
        char = gen.generate_character(
            level=5,
            class_choice=class_name,
            attribute_method="array"
        )
        if char.skills.has_skill("Sunblade"):
            has_sunblade_skill = True
            print(f"❌ {class_name}: Found Sunblade skill (should NOT have it)")
            print(f"   Skills: {', '.join([s for s in char.skills.skills.keys()])}")
            all_passed = False
            break

    if not has_sunblade_skill:
        print(f"✓ {class_name}: No Sunblade skill found (correct)")

if all_passed:
    print("\n✓ All non-Sunblade classes passed")
else:
    print("\n❌ Some non-Sunblade classes incorrectly have Sunblade skill")

# Test 2: Only Sunblades should have Sunblade skill
print("\n\nTest 2: Sunblade class SHOULD have Sunblade skill")
print("-" * 70)

sunblade_has_skill = False
for i in range(5):
    char = gen.generate_character(
        level=5,
        class_choice="Sunblade",
        attribute_method="array"
    )
    if char.skills.has_skill("Sunblade"):
        sunblade_has_skill = True
        print(f"✓ Sunblade character #{i+1}: Has Sunblade skill (correct)")
    else:
        print(f"❌ Sunblade character #{i+1}: Missing Sunblade skill")

if sunblade_has_skill:
    print("\n✓ Sunblade class correctly has Sunblade skill")

# Test 3: Non-spellcasters should never have Cast Magic skill
print("\n\nTest 3: Non-spellcaster classes should NOT have Cast Magic skill")
print("-" * 70)

non_spellcaster_classes = ["Warrior", "Expert", "Psychic", "Adventurer",
                           "Arcane Warrior", "Arcane Expert", "Sunblade",
                           "Godhunter", "Yama King"]

all_passed = True
for class_name in non_spellcaster_classes:
    # Generate 10 characters of each class
    has_cast_magic = False
    for i in range(10):
        char = gen.generate_character(
            level=5,
            class_choice=class_name,
            attribute_method="array"
        )
        if char.skills.has_skill("Cast Magic"):
            has_cast_magic = True
            print(f"❌ {class_name}: Found Cast Magic skill (should NOT have it)")
            print(f"   Skills: {', '.join([s for s in char.skills.skills.keys()])}")
            all_passed = False
            break

    if not has_cast_magic:
        print(f"✓ {class_name}: No Cast Magic skill found (correct)")

if all_passed:
    print("\n✓ All non-spellcaster classes passed")
else:
    print("\n❌ Some non-spellcaster classes incorrectly have Cast Magic skill")

# Test 4: Spellcasters should have Cast Magic skill
print("\n\nTest 4: Spellcaster classes SHOULD have Cast Magic skill")
print("-" * 70)

spellcaster_classes = ["Arcanist", "Pacter", "Rectifier", "War Mage"]

for class_name in spellcaster_classes:
    char = gen.generate_character(
        level=5,
        class_choice=class_name,
        attribute_method="array"
    )

    if char.skills.has_skill("Cast Magic"):
        print(f"✓ {class_name}: Has Cast Magic skill (correct)")
    else:
        print(f"❌ {class_name}: Missing Cast Magic skill")

# Test 5: Check specific Sunblade character
print("\n\nTest 5: Detailed Sunblade Character Check")
print("-" * 70)

sunblade = gen.generate_character(
    name="Test Sunblade",
    level=5,
    class_choice="Sunblade",
    attribute_method="array"
)

print(f"Class: {sunblade.character_class.name}")
print(f"Power Type: {sunblade.power_type}")
print(f"Is Spellcaster: {sunblade.character_class.is_spellcaster}")
print(f"\nSkills:")
for skill_name, skill_level in sorted(sunblade.skills.skills.items()):
    print(f"  {skill_name}: {skill_level}")

has_sunblade = sunblade.skills.has_skill("Sunblade")
has_cast_magic = sunblade.skills.has_skill("Cast Magic")

print(f"\n✓ Has Sunblade skill: {has_sunblade} (should be True)")
print(f"✓ Has Cast Magic skill: {has_cast_magic} (should be False)")

if has_sunblade and not has_cast_magic:
    print("\n✓ Sunblade character configured correctly")
else:
    print("\n❌ Sunblade character has incorrect skills")

print("\n" + "=" * 70)
print("✓ Class-specific skill restriction test complete!")
