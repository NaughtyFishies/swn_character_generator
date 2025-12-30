#!/usr/bin/env python3
"""Test Godhunter-specific backgrounds."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Godhunter-Specific Backgrounds")
print("=" * 70)

# Test 1: Godhunter Inquisitor
print("\nTest 1: Godhunter Inquisitor background")
print("-" * 70)

inquisitor = gen.generate_character(
    name="Test Inquisitor",
    level=1,
    class_choice="Godhunter",
    background_choice="Godhunter Inquisitor",
    attribute_method="array"
)

print(f"Character: {inquisitor.name}")
print(f"Class: {inquisitor.character_class.name}")
print(f"Background: {inquisitor.background.name}")
print(f"Class-specific: {inquisitor.background.class_specific}")

# Check for Notice skill
has_notice = inquisitor.skills.has_skill("Notice")
print(f"\nHas Notice skill: {has_notice}")
if has_notice:
    level = inquisitor.skills.get_level("Notice")
    print(f"Notice level: {level} (should be at least -1 for free skill)")

# Test 2: Godhunter Templar
print("\n\nTest 2: Godhunter Templar background")
print("-" * 70)

templar = gen.generate_character(
    name="Test Templar",
    level=1,
    class_choice="Godhunter",
    background_choice="Godhunter Templar",
    attribute_method="array"
)

print(f"Character: {templar.name}")
print(f"Class: {templar.character_class.name}")
print(f"Background: {templar.background.name}")
print(f"Class-specific: {templar.background.class_specific}")

# Check for combat skill from "Any Combat"
all_skills = templar.skills.get_all_skills()
level_neg1 = [s for s in all_skills if templar.skills.get_level(s.name) == -1]
print(f"\nLevel -1 skills (free skill): {[s.name for s in level_neg1]}")

combat_skills = ["Shoot", "Stab", "Punch"]
has_combat = any(templar.skills.has_skill(cs) for cs in combat_skills)
print(f"Has combat skill from 'Any Combat': {has_combat}")

# Test 3: Vengeful Renegade
print("\n\nTest 3: Vengeful Renegade background")
print("-" * 70)

renegade = gen.generate_character(
    name="Test Renegade",
    level=1,
    class_choice="Godhunter",
    background_choice="Vengeful Renegade",
    attribute_method="array"
)

print(f"Character: {renegade.name}")
print(f"Class: {renegade.character_class.name}")
print(f"Background: {renegade.background.name}")
print(f"Class-specific: {renegade.background.class_specific}")

# Check for combat skill and "Any Skill" resolution
all_skills = renegade.skills.get_all_skills()
level_neg1 = [s for s in all_skills if renegade.skills.get_level(s.name) == -1]
print(f"\nLevel -1 skills (free skill): {[s.name for s in level_neg1]}")
print(f"Free skill should be from 'Any Combat' (Shoot/Stab/Punch)")

# Test 4: "Any Combat" and "Any Skill" diversity
print("\n\nTest 4: 'Any Combat' and 'Any Skill' diversity (10 Vengeful Renegades)")
print("-" * 70)

free_skills_seen = {}
quick_skills_seen = {}

for i in range(10):
    char = gen.generate_character(
        level=1,
        class_choice="Godhunter",
        background_choice="Vengeful Renegade",
        attribute_method="array"
    )

    # Get the free skill (level -1)
    all_skills = char.skills.get_all_skills()
    for skill in all_skills:
        if char.skills.get_level(skill.name) == -1:
            free_skills_seen[skill.name] = free_skills_seen.get(skill.name, 0) + 1

    # Get level 0 skills (includes quick skill from background)
    for skill in all_skills:
        if char.skills.get_level(skill.name) == 0:
            quick_skills_seen[skill.name] = quick_skills_seen.get(skill.name, 0) + 1

print(f"Free skills from 'Any Combat' (10 trials):")
for skill, count in sorted(free_skills_seen.items()):
    print(f"  {skill}: {count}/10")

print(f"\nQuick skills seen (10 trials) - should include 'Any Skill' variety:")
for skill, count in sorted(quick_skills_seen.items()):
    print(f"  {skill}: {count}/10")

# Test 5: Background count verification
print("\n\nTest 5: Background count verification")
print("-" * 70)

general_bgs = gen.backgrounds.get_all_background_names(include_class_specific=False)
all_bgs = gen.backgrounds.get_all_background_names(include_class_specific=True)

print(f"General backgrounds: {len(general_bgs)}")
print(f"All backgrounds (including class-specific): {len(all_bgs)}")
print(f"Class-specific backgrounds: {len(all_bgs) - len(general_bgs)}")

# Count by class
godhunter_specific = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == "Godhunter"]

print(f"\nGodhunter-specific: {len(godhunter_specific)}")

print("\nGodhunter-specific backgrounds:")
for bg in godhunter_specific:
    print(f"  - {bg.name}: {bg.description}")

print("\n" + "=" * 70)
print("✓ Godhunter background test complete!")
