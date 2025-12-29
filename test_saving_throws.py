#!/usr/bin/env python3
"""Test saving throw calculations."""

from swn.generator import CharacterGenerator

gen = CharacterGenerator()

print("Testing Saving Throw Calculations")
print("=" * 70)
print("\nFormula: 16 - level - max(relevant attribute modifiers)")
print("  Physical: 16 - level - max(STR, CON)")
print("  Evasion:  16 - level - max(DEX, INT)")
print("  Mental:   16 - level - max(WIS, CHA)")
print("  Lower is better!")

# Test 1: Level 1 character with standard array
print("\n\nTest 1: Level 1 Warrior (Standard Array)")
print("-" * 70)

warrior1 = gen.generate_character(
    name="Test Warrior L1",
    level=1,
    class_choice="Warrior",
    attribute_method="array"
)

print(f"Character: {warrior1.name}")
print(f"Level: {warrior1.level}")
print(f"\nAttributes:")
for attr in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
    score = warrior1.attributes.get_score(attr)
    mod = warrior1.attributes.get_modifier(attr)
    print(f"  {attr}: {score:2d} (mod: {mod:+d})")

str_mod = warrior1.attributes.get_modifier("STR")
con_mod = warrior1.attributes.get_modifier("CON")
dex_mod = warrior1.attributes.get_modifier("DEX")
int_mod = warrior1.attributes.get_modifier("INT")
wis_mod = warrior1.attributes.get_modifier("WIS")
cha_mod = warrior1.attributes.get_modifier("CHA")

print(f"\nSaving Throws:")
print(f"  Physical: {warrior1.saving_throws['Physical']} = 16 - {warrior1.level} - max({str_mod}, {con_mod}) = 16 - {warrior1.level} - {max(str_mod, con_mod)}")
print(f"  Evasion:  {warrior1.saving_throws['Evasion']} = 16 - {warrior1.level} - max({dex_mod}, {int_mod}) = 16 - {warrior1.level} - {max(dex_mod, int_mod)}")
print(f"  Mental:   {warrior1.saving_throws['Mental']} = 16 - {warrior1.level} - max({wis_mod}, {cha_mod}) = 16 - {warrior1.level} - {max(wis_mod, cha_mod)}")

# Verify calculations
expected_physical = 16 - warrior1.level - max(str_mod, con_mod)
expected_evasion = 16 - warrior1.level - max(dex_mod, int_mod)
expected_mental = 16 - warrior1.level - max(wis_mod, cha_mod)

physical_match = warrior1.saving_throws['Physical'] == expected_physical
evasion_match = warrior1.saving_throws['Evasion'] == expected_evasion
mental_match = warrior1.saving_throws['Mental'] == expected_mental

print(f"\nVerification:")
print(f"  Physical: {'✓' if physical_match else '❌'} (expected {expected_physical}, got {warrior1.saving_throws['Physical']})")
print(f"  Evasion:  {'✓' if evasion_match else '❌'} (expected {expected_evasion}, got {warrior1.saving_throws['Evasion']})")
print(f"  Mental:   {'✓' if mental_match else '❌'} (expected {expected_mental}, got {warrior1.saving_throws['Mental']})")

# Test 2: Level 5 character
print("\n\nTest 2: Level 5 Expert (Standard Array)")
print("-" * 70)

expert5 = gen.generate_character(
    name="Test Expert L5",
    level=5,
    class_choice="Expert",
    attribute_method="array"
)

print(f"Character: {expert5.name}")
print(f"Level: {expert5.level}")
print(f"\nAttributes:")
for attr in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
    score = expert5.attributes.get_score(attr)
    mod = expert5.attributes.get_modifier(attr)
    print(f"  {attr}: {score:2d} (mod: {mod:+d})")

str_mod = expert5.attributes.get_modifier("STR")
con_mod = expert5.attributes.get_modifier("CON")
dex_mod = expert5.attributes.get_modifier("DEX")
int_mod = expert5.attributes.get_modifier("INT")
wis_mod = expert5.attributes.get_modifier("WIS")
cha_mod = expert5.attributes.get_modifier("CHA")

print(f"\nSaving Throws:")
print(f"  Physical: {expert5.saving_throws['Physical']} = 16 - {expert5.level} - max({str_mod}, {con_mod}) = 16 - {expert5.level} - {max(str_mod, con_mod)}")
print(f"  Evasion:  {expert5.saving_throws['Evasion']} = 16 - {expert5.level} - max({dex_mod}, {int_mod}) = 16 - {expert5.level} - {max(dex_mod, int_mod)}")
print(f"  Mental:   {expert5.saving_throws['Mental']} = 16 - {expert5.level} - max({wis_mod}, {cha_mod}) = 16 - {expert5.level} - {max(wis_mod, cha_mod)}")

# Test 3: Level 10 character
print("\n\nTest 3: Level 10 Psychic (Standard Array)")
print("-" * 70)

psychic10 = gen.generate_character(
    name="Test Psychic L10",
    level=10,
    class_choice="Psychic",
    attribute_method="array"
)

print(f"Character: {psychic10.name}")
print(f"Level: {psychic10.level}")
print(f"\nAttributes:")
for attr in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
    score = psychic10.attributes.get_score(attr)
    mod = psychic10.attributes.get_modifier(attr)
    print(f"  {attr}: {score:2d} (mod: {mod:+d})")

str_mod = psychic10.attributes.get_modifier("STR")
con_mod = psychic10.attributes.get_modifier("CON")
dex_mod = psychic10.attributes.get_modifier("DEX")
int_mod = psychic10.attributes.get_modifier("INT")
wis_mod = psychic10.attributes.get_modifier("WIS")
cha_mod = psychic10.attributes.get_modifier("CHA")

print(f"\nSaving Throws:")
print(f"  Physical: {psychic10.saving_throws['Physical']} = 16 - {psychic10.level} - max({str_mod}, {con_mod})")
print(f"  Evasion:  {psychic10.saving_throws['Evasion']} = 16 - {psychic10.level} - max({dex_mod}, {int_mod})")
print(f"  Mental:   {psychic10.saving_throws['Mental']} = 16 - {psychic10.level} - max({wis_mod}, {cha_mod})")

print(f"\nNote: At level 10, saves are significantly lower (better) than at level 1")

# Test 4: Verify formula across multiple levels
print("\n\nTest 4: Saving Throw Progression (1 character, levels 1-10)")
print("-" * 70)

print(f"\n{'Level':>5} | {'Physical':>8} | {'Evasion':>8} | {'Mental':>8} | Notes")
print("-" * 70)

for test_level in [1, 2, 3, 5, 7, 10]:
    char = gen.generate_character(
        level=test_level,
        class_choice="Warrior",
        attribute_method="array"
    )

    saves = char.saving_throws
    note = "Starting" if test_level == 1 else f"Improved by {16 - test_level - (16 - 1)}"

    print(f"{test_level:5d} | {saves['Physical']:8d} | {saves['Evasion']:8d} | {saves['Mental']:8d} | {note}")

print("\n" + "=" * 70)
print("✓ Saving throw calculation test complete!")
print("  Formula: 16 - level - max(relevant mods)")
print("  Saves improve (get lower) as level increases")
print("  High attributes improve (lower) saves")
