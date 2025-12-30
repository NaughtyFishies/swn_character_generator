#!/usr/bin/env python3
"""Test War Mage and Yama King class-specific backgrounds."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing War Mage and Yama King Class-Specific Backgrounds")
print("=" * 70)

# Test War Mage backgrounds
print("\n=== WAR MAGE BACKGROUNDS ===\n")

# Test 1: War Mage Veteran
print("Test 1: War Mage Veteran background")
print("-" * 70)

veteran = gen.generate_character(
    name="Test Veteran",
    level=1,
    class_choice="War Mage",
    background_choice="War Mage Veteran",
    attribute_method="array"
)

print(f"Character: {veteran.name}")
print(f"Class: {veteran.character_class.name}")
print(f"Background: {veteran.background.name}")
print(f"Class-specific: {veteran.background.class_specific}")

# Check for Cast Magic skill
has_cast = veteran.skills.has_skill("Cast Magic")
print(f"\nHas Cast Magic skill: {has_cast}")
if has_cast:
    level = veteran.skills.get_level("Cast Magic")
    print(f"Cast Magic level: {level}")

# Test 2: War Mage Officer
print("\n\nTest 2: War Mage Officer background")
print("-" * 70)

officer = gen.generate_character(
    name="Test Officer",
    level=1,
    class_choice="War Mage",
    background_choice="War Mage Officer",
    attribute_method="array"
)

print(f"Character: {officer.name}")
print(f"Class: {officer.character_class.name}")
print(f"Background: {officer.background.name}")

has_cast = officer.skills.has_skill("Cast Magic")
has_lead = officer.skills.has_skill("Lead")
print(f"\nHas Cast Magic skill: {has_cast}")
print(f"Has Lead skill: {has_lead}")

# Test 3: War Mage Rebel
print("\n\nTest 3: War Mage Rebel background")
print("-" * 70)

rebel = gen.generate_character(
    name="Test Rebel",
    level=1,
    class_choice="War Mage",
    background_choice="War Mage Rebel",
    attribute_method="array"
)

print(f"Character: {rebel.name}")
print(f"Class: {rebel.character_class.name}")
print(f"Background: {rebel.background.name}")

has_cast = rebel.skills.has_skill("Cast Magic")
has_sneak = rebel.skills.has_skill("Sneak")
print(f"\nHas Cast Magic skill: {has_cast}")
print(f"Has Sneak skill: {has_sneak}")

# Test Yama King backgrounds
print("\n\n=== YAMA KING BACKGROUNDS ===\n")

# Test 4: Accountant of Life and Death
print("Test 4: Accountant of Life and Death background")
print("-" * 70)

accountant = gen.generate_character(
    name="Test Accountant",
    level=1,
    class_choice="Yama King",
    background_choice="Accountant of Life and Death",
    attribute_method="array"
)

print(f"Character: {accountant.name}")
print(f"Class: {accountant.character_class.name}")
print(f"Background: {accountant.background.name}")
print(f"Class-specific: {accountant.background.class_specific}")

has_notice = accountant.skills.has_skill("Notice")
print(f"\nHas Notice skill: {has_notice}")
if has_notice:
    level = accountant.skills.get_level("Notice")
    print(f"Notice level: {level}")

# Test 5: Celestial Loss Preventer
print("\n\nTest 5: Celestial Loss Preventer background")
print("-" * 70)

preventer = gen.generate_character(
    name="Test Preventer",
    level=1,
    class_choice="Yama King",
    background_choice="Celestial Loss Preventer",
    attribute_method="array"
)

print(f"Character: {preventer.name}")
print(f"Class: {preventer.character_class.name}")
print(f"Background: {preventer.background.name}")

has_talk = preventer.skills.has_skill("Talk")
has_connect = preventer.skills.has_skill("Connect")
print(f"\nHas Talk skill: {has_talk}")
print(f"Has Connect skill: {has_connect}")

# Test 6: Devil's Incense
print("\n\nTest 6: Devil's Incense background")
print("-" * 70)

incense = gen.generate_character(
    name="Test Incense",
    level=1,
    class_choice="Yama King",
    background_choice="Devil's Incense",
    attribute_method="array"
)

print(f"Character: {incense.name}")
print(f"Class: {incense.character_class.name}")
print(f"Background: {incense.background.name}")

# Check for combat skill from "Any Combat"
all_skills = incense.skills.get_all_skills()
level_neg1 = [s for s in all_skills if incense.skills.get_level(s.name) == -1]
print(f"\nLevel -1 skills (free skill): {[s.name for s in level_neg1]}")

combat_skills = ["Shoot", "Stab", "Punch"]
has_combat = any(incense.skills.has_skill(cs) for cs in combat_skills)
print(f"Has combat skill from 'Any Combat': {has_combat}")

# Test 7: Final background count
print("\n\n=== FINAL VERIFICATION ===\n")
print("-" * 70)

general_bgs = gen.backgrounds.get_all_background_names(include_class_specific=False)
all_bgs = gen.backgrounds.get_all_background_names(include_class_specific=True)

print(f"General backgrounds: {len(general_bgs)}")
print(f"All backgrounds (including class-specific): {len(all_bgs)}")
print(f"Class-specific backgrounds: {len(all_bgs) - len(general_bgs)}")

# Count by class
war_mage_specific = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == "War Mage"]
yama_king_specific = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == "Yama King"]

print(f"\nWar Mage-specific: {len(war_mage_specific)}")
print(f"Yama King-specific: {len(yama_king_specific)}")

print("\nAll class-specific backgrounds by class:")
for class_name in ["Arcanist", "Free Nexus", "Godhunter", "Pacter", "Rectifier", "Sunblade", "War Mage", "Yama King"]:
    class_bgs = [bg for bg in gen.backgrounds.backgrounds if bg.class_specific == class_name]
    if class_bgs:
        print(f"\n{class_name} ({len(class_bgs)}):")
        for bg in class_bgs:
            print(f"  - {bg.name}")

print("\n" + "=" * 70)
print("✓ All class-specific background tests complete!")
print(f"✓ Total: {len(all_bgs)} backgrounds ({len(general_bgs)} general + {len(all_bgs) - len(general_bgs)} class-specific)")
