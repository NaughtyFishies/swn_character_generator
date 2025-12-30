#!/usr/bin/env python3
"""Test that Sunblade skill is maxed out for Sunblade characters."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Sunblade Skill Prioritization")
print("=" * 70)

# Test different levels of Sunblade characters
test_levels = [
    (1, 1),   # Level 1: max skill +1
    (2, 1),   # Level 2: max skill +1
    (3, 2),   # Level 3: max skill +2
    (5, 2),   # Level 5: max skill +2
    (6, 3),   # Level 6: max skill +3
    (8, 3),   # Level 8: max skill +3
    (9, 4),   # Level 9: max skill +4
    (10, 4),  # Level 10: max skill +4
]

print("\nSunblade Skill Level by Character Level:")
print("-" * 70)
print(f"{'Level':>6} | {'Expected Max':>12} | {'Actual':>6} | {'Status':>6}")
print("-" * 70)

all_passed = True

for char_level, expected_max in test_levels:
    # Generate 5 characters at this level to verify consistency
    sunblade_levels = []

    for _ in range(5):
        char = gen.generate_character(
            level=char_level,
            class_choice="Sunblade",
            attribute_method="array"
        )
        sunblade_skill_level = char.skills.get_level("Sunblade")
        sunblade_levels.append(sunblade_skill_level)

    # Check if all are at expected max
    all_maxed = all(level == expected_max for level in sunblade_levels)
    status = "✓" if all_maxed else "❌"

    if not all_maxed:
        all_passed = False

    # Show the range of levels seen
    min_level = min(sunblade_levels)
    max_level = max(sunblade_levels)

    if min_level == max_level:
        actual_str = str(min_level)
    else:
        actual_str = f"{min_level}-{max_level}"

    print(f"{char_level:6d} | {expected_max:12d} | {actual_str:>6s} | {status:>6s}")

if all_passed:
    print("\n✓ All Sunblade characters have maxed Sunblade skill!")
else:
    print("\n❌ Some Sunblade characters don't have maxed Sunblade skill")

# Detailed example for a level 10 Sunblade
print("\n\nDetailed Level 10 Sunblade Example:")
print("-" * 70)

sunblade10 = gen.generate_character(
    name="Master Sunblade",
    level=10,
    class_choice="Sunblade",
    attribute_method="array"
)

print(f"Name: {sunblade10.name}")
print(f"Level: {sunblade10.level}")
print(f"Class: {sunblade10.character_class.name}")
print(f"\nSkills:")

skills_sorted = sorted(sunblade10.skills.skills.items(),
                      key=lambda x: (-x[1].level, x[0]))

for skill_name, skill in skills_sorted:
    print(f"  {skill_name:20s} - Level {skill.level}")

sunblade_level = sunblade10.skills.get_level("Sunblade")
print(f"\n✓ Sunblade skill level: {sunblade_level} (expected: 4)")

if sunblade_level == 4:
    print("✓ Sunblade skill is maxed!")
else:
    print(f"❌ Sunblade skill is not maxed (only level {sunblade_level})")

# Show Sunblade abilities
if sunblade10.sunblade_abilities:
    wis_mod = sunblade10.attributes.get_modifier("WIS")
    cha_mod = sunblade10.attributes.get_modifier("CHA")
    effort_pool = sunblade10.sunblade_abilities.calculate_effort_pool(wis_mod, cha_mod)
    hit_bonus = sunblade10.sunblade_abilities.calculate_hit_bonus()

    print(f"\nSunblade Abilities:")
    print(f"  Sacred Weapon: {sunblade10.sunblade_abilities.sacred_weapon.weapon_type}")
    print(f"  Effort Pool: {effort_pool}")
    print(f"  Hit Bonus: +{hit_bonus}")
    print(f"  Total Abilities: {len(sunblade10.sunblade_abilities.selected_abilities)}")

print("\n" + "=" * 70)
print("✓ Sunblade skill prioritization test complete!")
