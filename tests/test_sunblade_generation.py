#!/usr/bin/env python3
"""Test Sunblade character generation with abilities and sacred weapons."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Sunblade Character Generation")
print("=" * 70)

# Test 1: Level 1 Sunblade
print("\nTest 1: Level 1 Sunblade")
print("-" * 70)

sunblade1 = gen.generate_character(
    name="Test Sunblade L1",
    level=1,
    class_choice="Sunblade",
    background_choice="Sunblade Mystic",
    attribute_method="array"
)

print(f"Character: {sunblade1.name}")
print(f"Class: {sunblade1.character_class.name}")
print(f"Level: {sunblade1.level}")
print(f"Background: {sunblade1.background.name}")
print(f"Power Type: {sunblade1.power_type}")

# Check Sunblade skill
has_sunblade = sunblade1.skills.has_skill("Sunblade")
print(f"\nHas Sunblade skill: {has_sunblade}")
if has_sunblade:
    level = sunblade1.skills.get_level("Sunblade")
    print(f"Sunblade skill level: {level}")

# Check Sunblade abilities
if sunblade1.sunblade_abilities:
    print(f"\nSunblade Abilities:")
    print(f"  Character Level: {sunblade1.sunblade_abilities.character_level}")
    print(f"  Sunblade Skill Level: {sunblade1.sunblade_abilities.sunblade_skill_level}")

    # Calculate effort and hit bonus
    wis_mod = sunblade1.attributes.get_modifier("WIS")
    cha_mod = sunblade1.attributes.get_modifier("CHA")
    effort = sunblade1.sunblade_abilities.calculate_effort_pool(wis_mod, cha_mod)
    hit_bonus = sunblade1.sunblade_abilities.calculate_hit_bonus()

    print(f"  Effort Pool: {effort} (Sunblade skill {sunblade1.sunblade_abilities.sunblade_skill_level} + max(WIS {wis_mod}, CHA {cha_mod}))")
    print(f"  Sacred Weapon Hit Bonus: +{hit_bonus} (half level rounded up)")

    print(f"\n  Sacred Weapon: {sunblade1.sunblade_abilities.sacred_weapon}")

    print(f"\n  Abilities:")
    for ability in sunblade1.sunblade_abilities.selected_abilities:
        auto_marker = " (automatic)" if ability.automatic else ""
        print(f"    - {ability.name}{auto_marker}")
        print(f"      {ability.description[:100]}...")
else:
    print("\n❌ No Sunblade abilities generated!")

# Test 2: Level 5 Sunblade (should have selectable abilities)
print("\n\nTest 2: Level 5 Sunblade (with selectable abilities)")
print("-" * 70)

sunblade5 = gen.generate_character(
    name="Test Sunblade L5",
    level=5,
    class_choice="Sunblade",
    background_choice="Sunblade Warrior",
    attribute_method="array"
)

print(f"Character: {sunblade5.name}")
print(f"Level: {sunblade5.level}")

# Check Sunblade abilities
if sunblade5.sunblade_abilities:
    print(f"\nSunblade Abilities:")
    wis_mod = sunblade5.attributes.get_modifier("WIS")
    cha_mod = sunblade5.attributes.get_modifier("CHA")
    effort = sunblade5.sunblade_abilities.calculate_effort_pool(wis_mod, cha_mod)
    hit_bonus = sunblade5.sunblade_abilities.calculate_hit_bonus()

    print(f"  Effort Pool: {effort}")
    print(f"  Sacred Weapon Hit Bonus: +{hit_bonus}")
    print(f"  Sacred Weapon: {sunblade5.sunblade_abilities.sacred_weapon.weapon_type}")

    # Count automatic vs selectable
    automatic = [a for a in sunblade5.sunblade_abilities.selected_abilities if a.automatic]
    selectable = [a for a in sunblade5.sunblade_abilities.selected_abilities if not a.automatic]

    print(f"\n  Total Abilities: {len(sunblade5.sunblade_abilities.selected_abilities)}")
    print(f"    - Automatic (Level 1): {len(automatic)}")
    print(f"    - Selectable (Levels 2,4): {len(selectable)}")

    print(f"\n  All Abilities:")
    for ability in sunblade5.sunblade_abilities.selected_abilities:
        auto_marker = " [AUTO]" if ability.automatic else " [SELECT]"
        print(f"    {ability.name}{auto_marker}")

# Test 3: Level 10 Sunblade (maximum selectable abilities)
print("\n\nTest 3: Level 10 Sunblade (max abilities)")
print("-" * 70)

sunblade10 = gen.generate_character(
    name="Test Sunblade L10",
    level=10,
    class_choice="Sunblade",
    background_choice="Sunblade Burnout",
    attribute_method="array"
)

print(f"Character: {sunblade10.name}")
print(f"Level: {sunblade10.level}")

if sunblade10.sunblade_abilities:
    automatic = [a for a in sunblade10.sunblade_abilities.selected_abilities if a.automatic]
    selectable = [a for a in sunblade10.sunblade_abilities.selected_abilities if not a.automatic]

    print(f"\nSunblade Abilities:")
    print(f"  Total Abilities: {len(sunblade10.sunblade_abilities.selected_abilities)}")
    print(f"    - Automatic (Level 1): {len(automatic)}")
    print(f"    - Selectable (Levels 2,4,6,8,10): {len(selectable)}")
    print(f"    - Expected Selectable: 5")

    wis_mod = sunblade10.attributes.get_modifier("WIS")
    cha_mod = sunblade10.attributes.get_modifier("CHA")
    effort = sunblade10.sunblade_abilities.calculate_effort_pool(wis_mod, cha_mod)
    hit_bonus = sunblade10.sunblade_abilities.calculate_hit_bonus()

    print(f"\n  Effort Pool: {effort}")
    print(f"  Sacred Weapon Hit Bonus: +{hit_bonus} (should be +5 for level 10)")

    print(f"\n  All Abilities:")
    for ability in sunblade10.sunblade_abilities.selected_abilities:
        auto_marker = " [AUTO]" if ability.automatic else " [SELECT]"
        print(f"    {ability.name}{auto_marker}")

print("\n" + "=" * 70)
print("✓ Sunblade character generation tests complete!")
