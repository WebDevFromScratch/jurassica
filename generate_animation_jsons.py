#!/usr/bin/env python3
"""
Generate animation JSON descriptor files for all Jurassica creatures.
These map VCMI animation groups to the PNG frame files.
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(BASE, "Mods", "jurassica", "Content")
SPRITES = os.path.join(CONTENT, "sprites", "creatures")

CREATURES = [
    "ozimek", "ozimekVolans", "raptor", "utahraptor",
    "triceratops", "torosaurus", "stegosaurus", "kentrosaurus",
    "pterodactyl", "quetzalcoatlus", "elasmosaurus", "mosasaurus",
    "trex", "giganotosaurus"
]

RANGED = {"pterodactyl", "quetzalcoatlus"}

# VCMI creature animation groups:
# 0  = Moving
# 1  = Mouse hover / Idle
# 2  = Getting hit
# 3  = Defend
# 4  = Death
# 5  = Death (ranged) - reuse group 4 frames
# 7  = Turn left
# 8  = Turn right
# 11 = Attack up
# 12 = Attack forward
# 13 = Attack down
# 14 = Ranged attack up (ranged only)
# 15 = Ranged attack forward (ranged only)
# 16 = Ranged attack down (ranged only)
# 20 = Start moving
# 21 = End moving

ANIM_GROUPS = {
    0:  ("move", 4),
    1:  ("idle", 3),
    2:  ("hit", 3),
    3:  ("defend", 2),
    4:  ("death", 4),
    5:  ("death", 4),       # Reuse death frames for ranged death
    7:  ("idle", 1),        # Turn left - reuse idle frame 0
    8:  ("idle", 1),        # Turn right - reuse idle frame 0
    11: ("atkUp", 4),
    12: ("atkFwd", 4),
    13: ("atkDwn", 4),
    20: ("startMove", 2),
    21: ("endMove", 2),
}

RANGED_GROUPS = {
    14: ("shootUp", 4),
    15: ("shootFwd", 4),
    16: ("shootDwn", 4),
}


def generate_battle_animation(creature_name):
    """Generate the battle animation JSON for a creature."""
    groups = dict(ANIM_GROUPS)
    if creature_name in RANGED:
        groups.update(RANGED_GROUPS)

    sequences = []
    for group_id in sorted(groups.keys()):
        label, num_frames = groups[group_id]
        frames = [f"{label}_{i:02d}.png" for i in range(num_frames)]
        seq = {
            "group": group_id,
            "frames": frames
        }
        if group_id in (0, 1, 11, 12, 13):
            seq["generateShadow"] = 1
            seq["generateOverlay"] = 1
        sequences.append(seq)

    return {
        "basepath": f"sprites/creatures/{creature_name}/",
        "sequences": sequences
    }


def generate_map_animation(creature_name):
    """Generate the adventure map animation JSON for a creature."""
    return {
        "basepath": f"sprites/creatures/{creature_name}/",
        "sequences": [
            {
                "group": 0,
                "frames": ["map_00.png"]
            }
        ]
    }


def generate_missile_animation(creature_name):
    """Generate the missile animation JSON for ranged creatures."""
    sequences = []
    for angle_idx in range(13):
        sequences.append({
            "group": angle_idx,
            "frames": [f"missile_{angle_idx:02d}.png"]
        })

    return {
        "basepath": f"sprites/creatures/{creature_name}/",
        "sequences": sequences
    }


def generate_adventure_town_animation(variant):
    """Generate adventure map town sprite animation JSON."""
    return {
        "basepath": "sprites/adventure/",
        "sequences": [
            {
                "group": 0,
                "frames": [f"jurassica{variant}.png"]
            }
        ]
    }


# Building key -> building ID mapping (must match jurassica.json building IDs)
BUILDING_IDS = {
    "mageGuild1": 0, "mageGuild2": 1, "mageGuild3": 2, "mageGuild4": 3,
    "tavern": 5,
    "fort": 7, "citadel": 8, "castle": 9,
    "villageHall": 10, "townHall": 11, "cityHall": 12, "capitol": 13,
    "marketplace": 14, "resourceSilo": 15, "blacksmith": 16,
    "horde1": 18, "grail": 26,
    "dwelling1": 30, "dwelling2": 31, "dwelling3": 32, "dwelling4": 33,
    "dwelling5": 34, "dwelling6": 35, "dwelling7": 36,
    "upgDwelling1": 37, "upgDwelling2": 38, "upgDwelling3": 39, "upgDwelling4": 40,
    "upgDwelling5": 41, "upgDwelling6": 42, "upgDwelling7": 43,
    "special1": 44, "special2": 45, "special3": 46, "special4": 47,
}

BUILDINGS = list(BUILDING_IDS.keys())


def generate_building_animation(building_key):
    """Generate a building animation JSON (single-frame static)."""
    return {
        "basepath": "sprites/towns/jurassica/buildings/",
        "sequences": [
            {
                "group": 0,
                "frames": [f"{building_key}.png"]
            }
        ]
    }


def main():
    print("Generating animation JSON descriptors...")

    for name in CREATURES:
        creature_dir = os.path.join(SPRITES, name)
        os.makedirs(creature_dir, exist_ok=True)

        # Battle animation
        battle_anim = generate_battle_animation(name)
        battle_path = os.path.join(creature_dir, f"{name}.json")
        with open(battle_path, 'w') as f:
            json.dump(battle_anim, f, indent='\t')

        # Map animation
        map_anim = generate_map_animation(name)
        map_path = os.path.join(creature_dir, f"{name}Map.json")
        with open(map_path, 'w') as f:
            json.dump(map_anim, f, indent='\t')

        # Missile animation (ranged only)
        if name in RANGED:
            missile_anim = generate_missile_animation(name)
            missile_path = os.path.join(creature_dir, f"{name}Missile.json")
            with open(missile_path, 'w') as f:
                json.dump(missile_anim, f, indent='\t')

        print(f"  {name}: battle + map" + (" + missile" if name in RANGED else ""))

    # Adventure map town animations
    adventure_dir = os.path.join(CONTENT, "sprites", "adventure")
    os.makedirs(adventure_dir, exist_ok=True)

    for variant in ["Village", "Fort", "Castle"]:
        anim = generate_adventure_town_animation(variant)
        anim_path = os.path.join(adventure_dir, f"jurassica{variant}.json")
        with open(anim_path, 'w') as f:
            json.dump(anim, f, indent='\t')
        print(f"  Adventure map: jurassica{variant}")

    # Hero animations (placeholder - single frame)
    heroes_dir = os.path.join(CONTENT, "sprites", "heroes")
    os.makedirs(heroes_dir, exist_ok=True)

    for hero_type in ["sauromancer", "warchief"]:
        # Battle animation (single-frame placeholder using portrait)
        battle_anim = {
            "basepath": "sprites/heroes/",
            "sequences": [
                {
                    "group": 0,
                    "frames": ["primalusSmall.png"]
                }
            ]
        }
        battle_path = os.path.join(heroes_dir, f"{hero_type}Battle.json")
        with open(battle_path, 'w') as f:
            json.dump(battle_anim, f, indent='\t')

        # Map animation — groups 0-7 for 8 compass directions, 4 walking frames each
        map_sequences = []
        for direction in range(8):
            frames = [f"{hero_type}Map_dir{direction}_f{fi}.png" for fi in range(4)]
            map_sequences.append({
                "group": direction,
                "frames": frames
            })
        map_anim = {
            "basepath": "sprites/heroes/",
            "sequences": map_sequences
        }
        map_path = os.path.join(heroes_dir, f"{hero_type}Map.json")
        with open(map_path, 'w') as f:
            json.dump(map_anim, f, indent='\t')

        print(f"  Hero animation: {hero_type} (battle + map with 8 directions)")

    # Building animations
    buildings_dir = os.path.join(CONTENT, "sprites", "towns", "jurassica", "buildings")
    os.makedirs(buildings_dir, exist_ok=True)

    for bkey in BUILDINGS:
        banim = generate_building_animation(bkey)
        bpath = os.path.join(buildings_dir, f"{bkey}.json")
        with open(bpath, 'w') as f:
            json.dump(banim, f, indent='\t')
    print(f"  Buildings: {len(BUILDINGS)} animation JSONs")

    # Building hall icons animation JSON
    # Group numbers must match building IDs from jurassica.json
    icon_sequences = []
    for bkey in BUILDINGS:
        icon_sequences.append({
            "group": BUILDING_IDS[bkey],
            "frames": [f"{bkey}_icon.png"]
        })
    icons_anim = {
        "basepath": "sprites/towns/jurassica/buildings/",
        "sequences": icon_sequences
    }
    icons_path = os.path.join(buildings_dir, "icons.json")
    with open(icons_path, 'w') as f:
        json.dump(icons_anim, f, indent='\t')
    print("  Building icons: icons.json")

    print("\nDone! All animation JSONs generated.")


if __name__ == "__main__":
    main()
