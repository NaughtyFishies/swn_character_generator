"""Equipment system for SWN characters."""
import json
import random
from pathlib import Path
from typing import List, Dict, Optional


class Equipment:
    """Represents a single piece of equipment."""

    def __init__(self, name: str, category: str, cost: int, enc: int,
                 tech_level: int, description: str = "", **kwargs):
        """
        Initialize equipment.

        Args:
            name: Equipment name
            category: Equipment category
            cost: Cost in credits
            enc: Encumbrance value
            tech_level: Required technology level
            description: Equipment description
            **kwargs: Additional equipment-specific properties
        """
        self.name = name
        self.category = category
        self.cost = cost
        self.enc = enc
        self.tech_level = tech_level
        self.description = description
        self.properties = kwargs

    def to_dict(self) -> dict:
        """Convert equipment to dictionary format."""
        return {
            "name": self.name,
            "category": self.category,
            "cost": self.cost,
            "enc": self.enc,
            "tech_level": self.tech_level,
            "description": self.description,
            **self.properties
        }

    def __str__(self) -> str:
        """Return formatted equipment string."""
        return f"{self.name} (TL{self.tech_level}, {self.cost}cr, {self.enc} enc)"


class EquipmentSet:
    """Manages a character's equipment."""

    def __init__(self):
        """Initialize empty equipment set."""
        self.armor: Optional[Equipment] = None
        self.weapons: List[Equipment] = []
        self.gear: List[Equipment] = []

    def add_armor(self, armor: Equipment):
        """Add armor to the set."""
        self.armor = armor

    def add_weapon(self, weapon: Equipment):
        """Add weapon to the set."""
        self.weapons.append(weapon)

    def add_gear(self, item: Equipment):
        """Add gear item to the set."""
        self.gear.append(item)

    def total_cost(self) -> int:
        """Calculate total equipment cost."""
        total = 0
        if self.armor:
            total += self.armor.cost
        total += sum(w.cost for w in self.weapons)
        total += sum(g.cost for g in self.gear)
        return total

    def total_encumbrance(self) -> int:
        """Calculate total encumbrance."""
        total = 0
        if self.armor:
            total += self.armor.enc
        total += sum(w.enc for w in self.weapons)
        total += sum(g.enc for g in self.gear)
        return total

    def get_all_items(self) -> List[Equipment]:
        """Get all equipment as a flat list."""
        items = []
        if self.armor:
            items.append(self.armor)
        items.extend(self.weapons)
        items.extend(self.gear)
        return items

    def to_dict(self) -> dict:
        """Convert equipment set to dictionary."""
        return {
            "armor": self.armor.to_dict() if self.armor else None,
            "weapons": [w.to_dict() for w in self.weapons],
            "gear": [g.to_dict() for g in self.gear],
            "total_cost": self.total_cost(),
            "total_encumbrance": self.total_encumbrance()
        }


class EquipmentSelector:
    """Manages equipment selection based on class and tech level."""

    def __init__(self, armor_data: List[dict], weapons_data: Dict[str, List[dict]],
                 gear_data: List[dict]):
        """
        Initialize equipment selector.

        Args:
            armor_data: List of armor items
            weapons_data: Dict with 'ranged_weapons' and 'melee_weapons' lists
            gear_data: List of gear items
        """
        self.armor_items = [Equipment(**item) for item in armor_data]
        # Weapons don't have category in JSON, so add it when creating Equipment
        self.ranged_weapons = [Equipment(category="ranged_weapon", **item)
                               for item in weapons_data.get("ranged_weapons", [])]
        self.melee_weapons = [Equipment(category="melee_weapon", **item)
                             for item in weapons_data.get("melee_weapons", [])]
        self.gear_items = [Equipment(**item) for item in gear_data]

    @classmethod
    def load_from_files(cls, data_dir: Path) -> 'EquipmentSelector':
        """
        Load equipment from JSON files.

        Args:
            data_dir: Path to data directory

        Returns:
            EquipmentSelector instance
        """
        with open(data_dir / "armor.json", 'r') as f:
            armor_data = json.load(f)["armor"]

        with open(data_dir / "weapons.json", 'r') as f:
            weapons_data = json.load(f)

        with open(data_dir / "gear.json", 'r') as f:
            gear_data = json.load(f)["gear"]

        return cls(armor_data, weapons_data, gear_data)

    def select_equipment(self, character_class: str, tech_level: int,
                        credits_budget: int = 10000) -> EquipmentSet:
        """
        Select appropriate equipment for a character.

        Args:
            character_class: Character class name
            tech_level: Technology level (0-5)
            credits_budget: Maximum credits to spend

        Returns:
            EquipmentSet with selected equipment
        """
        equipment_set = EquipmentSet()
        remaining_credits = credits_budget

        # Select armor based on class preferences
        armor = self._select_armor(character_class, tech_level, remaining_credits)
        if armor:
            equipment_set.add_armor(armor)
            remaining_credits -= armor.cost

        # Select 2 weapons (1 ranged, 1 melee typically)
        weapons = self._select_weapons(character_class, tech_level, remaining_credits)
        for weapon in weapons:
            equipment_set.add_weapon(weapon)
            remaining_credits -= weapon.cost

        # Select 3-5 gear items
        gear_count = random.randint(3, 5)
        gear = self._select_gear(character_class, tech_level, remaining_credits, gear_count)
        for item in gear:
            equipment_set.add_gear(item)
            remaining_credits -= item.cost

        return equipment_set

    def _select_armor(self, character_class: str, tech_level: int,
                     max_cost: int) -> Optional[Equipment]:
        """Select appropriate armor based on class."""
        # Filter by tech level and cost
        available = [a for a in self.armor_items
                    if a.tech_level <= tech_level and a.cost <= max_cost]

        if not available:
            return None

        # Class-based armor preferences
        if character_class in ["Warrior", "Adventurer"]:
            # Prefer combat armor
            combat = [a for a in available if a.category == "combat"]
            if combat:
                return random.choice(combat)
        elif character_class in ["Expert", "Psychic"]:
            # Prefer street armor
            street = [a for a in available if a.category == "street"]
            if street:
                return random.choice(street)

        # Default: prefer higher AC within budget
        available.sort(key=lambda a: self._parse_ac(a), reverse=True)
        # Pick from top 3 to add variety
        return random.choice(available[:min(3, len(available))])

    def _select_weapons(self, character_class: str, tech_level: int,
                       max_cost: int) -> List[Equipment]:
        """Select 2 weapons based on class preferences."""
        weapons = []

        # Filter by tech level
        available_ranged = [w for w in self.ranged_weapons if w.tech_level <= tech_level]
        available_melee = [w for w in self.melee_weapons if w.tech_level <= tech_level]

        # Class-based weapon preferences
        if character_class == "Warrior":
            # Warriors prefer heavy weapons
            rifles = [w for w in available_ranged
                     if w.enc == 2 and w.cost <= max_cost * 0.3]
            if rifles:
                weapons.append(random.choice(rifles))
                max_cost -= weapons[0].cost

            large_melee = [w for w in available_melee
                          if w.properties.get("size") == "large" and w.cost <= max_cost]
            if large_melee:
                weapons.append(random.choice(large_melee))

        elif character_class == "Expert":
            # Experts prefer versatile, concealable weapons
            pistols = [w for w in available_ranged
                      if w.enc == 1 and w.cost <= max_cost * 0.2]
            if pistols:
                weapons.append(random.choice(pistols))
                max_cost -= weapons[0].cost

            small_melee = [w for w in available_melee
                          if w.properties.get("size") == "small" and w.cost <= max_cost]
            if small_melee:
                weapons.append(random.choice(small_melee))

        elif character_class == "Psychic":
            # Psychics prefer light weapons
            light_ranged = [w for w in available_ranged
                           if w.enc == 1 and w.cost <= max_cost * 0.15]
            if light_ranged:
                weapons.append(random.choice(light_ranged))
                max_cost -= weapons[0].cost

            small_melee = [w for w in available_melee
                          if w.properties.get("size") == "small" and w.cost <= max_cost]
            if small_melee:
                weapons.append(random.choice(small_melee))

        else:  # Adventurer or others
            # Balanced approach - pistol + medium melee
            pistols = [w for w in available_ranged
                      if w.enc == 1 and w.cost <= max_cost * 0.2]
            if pistols:
                weapons.append(random.choice(pistols))
                max_cost -= weapons[0].cost

            medium_melee = [w for w in available_melee
                           if w.properties.get("size") in ["medium", "small"] and w.cost <= max_cost]
            if medium_melee:
                weapons.append(random.choice(medium_melee))

        # Ensure we have at least 2 weapons
        while len(weapons) < 2 and (available_ranged or available_melee):
            if len(weapons) == 0 and available_ranged:
                affordable = [w for w in available_ranged if w.cost <= max_cost]
                if affordable:
                    weapons.append(random.choice(affordable))
            elif available_melee:
                affordable = [w for w in available_melee if w.cost <= max_cost]
                if affordable:
                    weapons.append(random.choice(affordable))
                    break
            else:
                break

        return weapons[:2]

    def _select_gear(self, character_class: str, tech_level: int,
                    max_cost: int, count: int) -> List[Equipment]:
        """Select gear items based on class preferences."""
        gear = []
        available = [g for g in self.gear_items if g.tech_level <= tech_level]

        # Class-based gear preferences
        if character_class == "Warrior":
            priorities = ["medical", "ammo", "field"]
        elif character_class == "Expert":
            priorities = ["tools", "computing", "communications", "field"]
        elif character_class == "Psychic":
            priorities = ["medical", "communications", "field"]
        else:
            priorities = ["field", "medical", "communications"]

        # Always include essentials
        essentials = ["Compad", "Lazarus Patch", "Power Cell Type A", "Backpack"]
        for essential in essentials:
            item = next((g for g in available if g.name == essential), None)
            if item and item.cost <= max_cost and len(gear) < count:
                gear.append(item)
                max_cost -= item.cost
                available.remove(item)

        # Fill remaining slots with priority categories
        for priority in priorities:
            priority_items = [g for g in available
                            if g.category == priority and g.cost <= max_cost * 0.1]
            if priority_items and len(gear) < count:
                item = random.choice(priority_items)
                gear.append(item)
                max_cost -= item.cost
                available.remove(item)

        # Fill any remaining slots randomly
        while len(gear) < count and available:
            affordable = [g for g in available if g.cost <= max_cost * 0.05]
            if not affordable:
                break
            item = random.choice(affordable)
            gear.append(item)
            max_cost -= item.cost
            available.remove(item)

        return gear

    def _parse_ac(self, armor: Equipment) -> int:
        """Parse AC value from armor (handles '13' or '15/+1 bonus' formats)."""
        ac_str = str(armor.properties.get("ac", "10"))
        if "/" in ac_str:
            # Handle shield format "13/+1 bonus"
            return int(ac_str.split("/")[0])
        return int(ac_str)


def calculate_starting_credits(character_class: str, level: int) -> int:
    """
    Calculate starting credits for a character.

    Formula: Base (1000-2000 depending on class) + (level * 500)

    Args:
        character_class: Character class name
        level: Character level

    Returns:
        Starting credits amount
    """
    # Base credits by class
    if character_class == "Warrior":
        base = 1500
    elif character_class == "Expert":
        base = 2000
    elif character_class == "Psychic":
        base = 1000
    else:  # Adventurer and others
        base = 1500

    return base + (level * 500)
