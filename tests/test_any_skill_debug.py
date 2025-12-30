#!/usr/bin/env python3
"""Debug 'Any Skill' resolution."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Debugging 'Any Skill' Resolution")
print("=" * 70)

# Generate one Escaped Familiar to see what's happening
char = gen.generate_character(
    name="Debug Character",
    level=1,
    class_choice="Expert",  # Use Expert to avoid Free Nexus complications
    background_choice="Escaped Familiar",
    attribute_method="array"
)

print(f"Character: {char.name}")
print(f"Class: {char.character_class.name}")
print(f"Background: {char.background.name}")
print(f"Background free skill: {char.background.free_skill}")

# Show ALL skills
print(f"\nAll skills:")
all_skills = char.skills.get_all_skills()
for skill in sorted(all_skills, key=lambda s: s.name):
    level = char.skills.get_level(skill.name)
    print(f"  {skill.name}: level {level}")

# Check specifically for level -1
level_neg1 = [s for s in all_skills if char.skills.get_level(s.name) == -1]
print(f"\nLevel -1 skills: {[s.name for s in level_neg1]}")

# Check level 0
level_0 = [s for s in all_skills if char.skills.get_level(s.name) == 0]
print(f"Level 0 skills: {[s.name for s in level_0]}")
