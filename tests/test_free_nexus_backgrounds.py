#!/usr/bin/env python3
"""Test Free Nexus-specific backgrounds."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Free Nexus-Specific Backgrounds")
print("=" * 70)

# Test 1: Arcane Muse
print("\nTest 1: Arcane Muse background")
print("-" * 70)

muse = gen.generate_character(
    name="Test Muse",
    level=1,
    class_choice="Free Nexus",
    background_choice="Arcane Muse",
    attribute_method="array"
)

print(f"Character: {muse.name}")
print(f"Class: {muse.character_class.name}")
print(f"Background: {muse.background.name}")
print(f"Class-specific: {muse.background.class_specific}")

# Check for Talk skill
has_talk = muse.skills.has_skill("Talk")
print(f"\nHas Talk skill: {has_talk}")
if has_talk:
    level = muse.skills.get_level("Talk")
    print(f"Talk level: {level} (should be -1 for free skill)")

# Test 2: Escaped Familiar
print("\n\nTest 2: Escaped Familiar background")
print("-" * 70)

familiar = gen.generate_character(
    name="Test Familiar",
    level=1,
    class_choice="Free Nexus",
    background_choice="Escaped Familiar",
    attribute_method="array"
)

print(f"Character: {familiar.name}")
print(f"Class: {familiar.character_class.name}")
print(f"Background: {familiar.background.name}")
print(f"Class-specific: {familiar.background.class_specific}")

# Check what skill was assigned from "Any Skill"
all_skills = familiar.skills.get_all_skills()
level_neg1 = [s for s in all_skills if familiar.skills.get_level(s.name) == -1]
print(f"\nLevel -1 skills (free skill): {[s.name for s in level_neg1]}")
print(f"Free skill was resolved from 'Any Skill'")

# Test 3: Occult Proxy
print("\n\nTest 3: Occult Proxy background")
print("-" * 70)

proxy = gen.generate_character(
    name="Test Proxy",
    level=1,
    class_choice="Free Nexus",
    background_choice="Occult Proxy",
    attribute_method="array"
)

print(f"Character: {proxy.name}")
print(f"Class: {proxy.character_class.name}")
print(f"Background: {proxy.background.name}")
print(f"Class-specific: {proxy.background.class_specific}")

# Check for Exert skill
has_exert = proxy.skills.has_skill("Exert")
print(f"\nHas Exert skill: {has_exert}")
if has_exert:
    level = proxy.skills.get_level("Exert")
    print(f"Exert level: {level} (should be -1 for free skill)")

# Test 4: "Any Skill" resolution diversity
print("\n\nTest 4: 'Any Skill' resolution diversity (10 Escaped Familiars)")
print("-" * 70)

skills_seen = {}
for i in range(10):
    char = gen.generate_character(
        level=1,
        class_choice="Free Nexus",
        background_choice="Escaped Familiar",
        attribute_method="array"
    )

    # Get the free skill (level -1)
    all_skills = char.skills.get_all_skills()
    for skill in all_skills:
        if char.skills.get_level(skill.name) == -1:
            skills_seen[skill.name] = skills_seen.get(skill.name, 0) + 1

print(f"Skills assigned from 'Any Skill' (10 trials):")
for skill, count in sorted(skills_seen.items()):
    print(f"  {skill}: {count}/10")

# Verify no psychic disciplines were assigned
psychic_disciplines = ["Biopsionics", "Metapsionics", "Precognition",
                      "Telekinesis", "Telepathy", "Teleportation"]
psychic_assigned = any(skill in psychic_disciplines for skill in skills_seen)
if psychic_assigned:
    print(f"❌ ERROR: Psychic disciplines were assigned from 'Any Skill'!")
else:
    print(f"✓ No psychic disciplines assigned (correct)")

# Test 5: Check background filtering
print("\n\nTest 5: Background count verification")
print("-" * 70)

general_bgs = gen.backgrounds.get_all_background_names(include_class_specific=False)
all_bgs = gen.backgrounds.get_all_background_names(include_class_specific=True)

print(f"General backgrounds: {len(general_bgs)}")
print(f"All backgrounds (including class-specific): {len(all_bgs)}")
print(f"Class-specific backgrounds: {len(all_bgs) - len(general_bgs)}")

# Count by class
arcanist_specific = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == "Arcanist"]
nexus_specific = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == "Free Nexus"]

print(f"\nArcanist-specific: {len(arcanist_specific)}")
print(f"Free Nexus-specific: {len(nexus_specific)}")

print("\nFree Nexus-specific backgrounds:")
for bg in nexus_specific:
    print(f"  - {bg.name}: {bg.description}")

print("\n" + "=" * 70)
print("✓ Free Nexus background test complete!")
