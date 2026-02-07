#!/usr/bin/env python3
"""
Generate placeholder graphics for the Jurassica VCMI mod.

Creates simple colored silhouette PNGs for all creatures, icons, town graphics,
and hero portraits so the mod is loadable in VCMI before real art is created.

Requirements: pip install Pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(BASE, "Mods", "jurassica", "Content")

# Creature definitions: (name, color, size_w, size_h, is_double_wide)
CREATURES = [
    ("ozimek",         (120, 200, 120), 80, 90, False),
    ("ozimekVolans",   (100, 220, 100), 90, 100, False),
    ("raptor",         (200, 100, 80),  100, 110, False),
    ("utahraptor",     (220, 80, 60),   120, 130, False),
    ("triceratops",    (150, 130, 80),  150, 130, True),
    ("torosaurus",     (170, 110, 60),  160, 140, True),
    ("stegosaurus",    (100, 140, 100), 160, 120, True),
    ("kentrosaurus",   (80, 160, 80),   170, 130, True),
    ("pterodactyl",    (100, 150, 200), 140, 100, False),
    ("quetzalcoatlus", (80, 130, 220),  180, 120, True),
    ("elasmosaurus",   (80, 120, 180),  180, 130, True),
    ("mosasaurus",     (60, 100, 160),  200, 140, True),
    ("trex",           (180, 60, 60),   200, 180, True),
    ("giganotosaurus", (200, 40, 40),   220, 200, True),
]

# Hero names
HEROES = [
    "rexar", "clawdia", "thornback", "trika", "skytalon", "deepjaw",
    "stonehorn", "swiftclaw", "primalus", "ashara", "fossilus", "ambra",
    "volcanix", "fernweaver", "tremor", "ozimara"
]


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def draw_text_centered(draw, text, x, y, w, h, fill=(255, 255, 255)):
    """Draw text centered in a bounding box, wrapping if needed."""
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        except (OSError, IOError):
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # If text is too wide, try smaller or wrap
    if tw > w - 4:
        # Split into two lines
        mid = len(text) // 2
        # Find nearest space
        space_pos = text.rfind(' ', 0, mid + 5)
        if space_pos == -1:
            space_pos = mid
        line1 = text[:space_pos].strip()
        line2 = text[space_pos:].strip()

        bbox1 = draw.textbbox((0, 0), line1, font=font)
        bbox2 = draw.textbbox((0, 0), line2, font=font)
        tw1 = bbox1[2] - bbox1[0]
        tw2 = bbox2[2] - bbox2[0]

        tx1 = x + (w - tw1) // 2
        tx2 = x + (w - tw2) // 2
        ty = y + (h - th * 2 - 4) // 2
        draw.text((tx1, ty), line1, fill=fill, font=font)
        draw.text((tx2, ty + th + 2), line2, fill=fill, font=font)
    else:
        tx = x + (w - tw) // 2
        ty = y + (h - th) // 2
        draw.text((tx, ty), text, fill=fill, font=font)


def create_creature_frame(name, color, w, h, label="idle"):
    """Create a single creature sprite frame with a colored silhouette."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a simple dinosaur-ish shape
    margin = 8
    body_rect = [margin, margin, w - margin, h - margin]

    # Body ellipse
    draw.ellipse(body_rect, fill=color + (220,), outline=(0, 0, 0, 255), width=2)

    # Name and label
    draw_text_centered(draw, name, margin, margin, w - 2*margin, (h - 2*margin) // 2)
    draw_text_centered(draw, f"[{label}]", margin, h//2, w - 2*margin, (h - 2*margin) // 2,
                       fill=(200, 200, 200))

    return img


def create_icon(name, color, size, label=""):
    """Create a creature or town icon."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = 2
    draw.rounded_rectangle([margin, margin, size - margin, size - margin],
                           radius=4, fill=color + (220,), outline=(0, 0, 0, 255), width=1)

    display = label or name[:6]
    draw_text_centered(draw, display, margin, margin, size - 2*margin, size - 2*margin)

    return img


def create_town_background():
    """Create a placeholder town background (800x374)."""
    img = Image.new("RGB", (800, 374), (60, 80, 40))
    draw = ImageDraw.Draw(img)

    # Sky gradient (simple)
    for y in range(150):
        r = 80 + y
        g = 100 + y // 2
        b = 140 + y // 3
        draw.line([(0, y), (799, y)], fill=(min(r, 255), min(g, 255), min(b, 255)))

    # Volcano
    draw.polygon([(350, 50), (450, 50), (500, 150), (300, 150)], fill=(100, 60, 40))
    draw.polygon([(370, 50), (430, 50), (420, 30), (380, 30)], fill=(200, 80, 30))

    # Ground
    draw.rectangle([0, 200, 800, 374], fill=(80, 100, 50))

    # Jungle trees
    for x in [50, 150, 650, 730]:
        draw.polygon([(x, 180), (x + 40, 180), (x + 20, 120)], fill=(30, 100, 30))
        draw.rectangle([x + 15, 180, x + 25, 200], fill=(100, 70, 40))

    # Label
    draw_text_centered(draw, "JURASSICA — Placeholder Town Screen", 200, 300, 400, 50,
                       fill=(200, 200, 150))

    return img


def create_hero_portrait(name, size, is_large=False):
    """Create a placeholder hero portrait."""
    if is_large:
        img = Image.new("RGBA", (58, 64), (0, 0, 0, 0))
        w, h = 58, 64
    else:
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        w, h = 32, 32

    draw = ImageDraw.Draw(img)

    # Hash name for consistent color
    hsh = hash(name) % 360
    r = 100 + (hsh * 7) % 120
    g = 80 + (hsh * 13) % 120
    b = 80 + (hsh * 17) % 120

    draw.rounded_rectangle([1, 1, w-1, h-1], radius=3,
                           fill=(r, g, b, 220), outline=(200, 180, 100, 255), width=2)
    draw_text_centered(draw, name[:8], 2, 2, w-4, h-4)

    return img


def create_adventure_map_sprite(name, color):
    """Create a placeholder adventure map town sprite."""
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([2, 2, 30, 30], radius=4, fill=color + (220,),
                           outline=(0, 0, 0, 255), width=1)
    draw_text_centered(draw, name[:4], 2, 2, 28, 28)
    return img


def generate_all():
    print("Generating placeholder graphics for Jurassica mod...")

    sprites_dir = os.path.join(CONTENT, "sprites")
    icons_dir = os.path.join(sprites_dir, "icons")
    towns_dir = os.path.join(sprites_dir, "towns", "jurassica")
    adventure_dir = os.path.join(sprites_dir, "adventure")
    heroes_dir = os.path.join(sprites_dir, "heroes")

    ensure_dir(icons_dir)
    ensure_dir(towns_dir)
    ensure_dir(adventure_dir)
    ensure_dir(heroes_dir)

    # Animation groups for creatures (minimal set for MVP)
    # Group 0: Moving, Group 1: Idle/Hover, Group 2: Getting hit
    # Group 4: Death, Group 11: Attack up, Group 12: Attack front, Group 13: Attack down
    # Group 20: Start moving, Group 21: End moving
    ANIM_GROUPS = {
        0: ("move", 4),      # Moving - 4 frames
        1: ("idle", 3),      # Idle - 3 frames
        2: ("hit", 3),       # Getting hit - 3 frames
        3: ("defend", 2),    # Defend - 2 frames
        4: ("death", 4),     # Death - 4 frames
        11: ("atkUp", 4),    # Attack up - 4 frames
        12: ("atkFwd", 4),   # Attack forward - 4 frames
        13: ("atkDwn", 4),   # Attack down - 4 frames
        20: ("startMove", 2),  # Start moving
        21: ("endMove", 2),    # End moving
    }

    RANGED_GROUPS = {
        14: ("shootUp", 4),
        15: ("shootFwd", 4),
        16: ("shootDwn", 4),
    }

    ranged_creatures = {"pterodactyl", "quetzalcoatlus"}

    total_frames = 0

    for name, color, w, h, is_wide in CREATURES:
        creature_dir = os.path.join(sprites_dir, "creatures", name)
        ensure_dir(creature_dir)

        groups = dict(ANIM_GROUPS)
        if name in ranged_creatures:
            groups.update(RANGED_GROUPS)

        # Generate frames for each animation group
        for group_id, (label, num_frames) in groups.items():
            for frame_idx in range(num_frames):
                frame_label = f"{label}{frame_idx+1}"
                frame = create_creature_frame(name, color, w, h, frame_label)
                frame_path = os.path.join(creature_dir, f"{label}_{frame_idx:02d}.png")
                frame.save(frame_path)
                total_frames += 1

        # Adventure map sprite (single frame for now)
        map_frame = create_adventure_map_sprite(name, color)
        map_frame.save(os.path.join(creature_dir, "map_00.png"))
        total_frames += 1

        # Creature icons
        icon_small = create_icon(name, color, 32)
        icon_small.save(os.path.join(icons_dir, f"{name}Small.png"))

        icon_large = create_icon(name, color, 58, name)
        icon_large.save(os.path.join(icons_dir, f"{name}Large.png"))

        # Missile sprite for ranged creatures
        if name in ranged_creatures:
            missile_dir = creature_dir
            for angle_idx in range(13):
                missile = Image.new("RGBA", (20, 6), (0, 0, 0, 0))
                md = ImageDraw.Draw(missile)
                md.polygon([(0, 1), (0, 4), (18, 3)], fill=(180, 160, 100, 200))
                missile.save(os.path.join(missile_dir, f"missile_{angle_idx:02d}.png"))
                total_frames += 1

        print(f"  {name}: generated frames + icons")

    # Town screen graphics
    print("  Generating town screen...")
    town_bg = create_town_background()
    town_bg.save(os.path.join(towns_dir, "townBackground.png"))

    # Guild and hall backgrounds (reuse town bg with different tints)
    guild_bg = town_bg.copy()
    guild_bg.save(os.path.join(towns_dir, "guildWindow.png"))
    hall_bg = town_bg.copy()
    hall_bg.save(os.path.join(towns_dir, "hallBackground.png"))

    # Creature backgrounds for info panels
    for size, filename in [(120, "creatBg120.png"), (130, "creatBg130.png")]:
        bg = Image.new("RGBA", (size, size), (40, 60, 30, 200))
        draw = ImageDraw.Draw(bg)
        draw.rectangle([2, 2, size-2, size-2], outline=(100, 80, 40, 200), width=2)
        bg.save(os.path.join(towns_dir, filename))

    # Town icons (village/fort small/large, normal/built)
    print("  Generating town icons...")
    for variant in ["Village", "Fort"]:
        for state in ["", "Built"]:
            for size_name, size in [("Small", 32), ("Large", 58)]:
                icon = create_icon(f"J-{variant[0]}", (60, 100, 50), size, f"J {variant[:3]}")
                icon.save(os.path.join(icons_dir, f"town{variant}{state}{size_name}.png"))

    # Adventure map town sprites
    print("  Generating adventure map sprites...")
    for variant in ["Village", "Fort", "Castle"]:
        sprite = create_adventure_map_sprite(f"J-{variant[0]}", (60, 100, 50))
        sprite_path = os.path.join(adventure_dir, f"jurassica{variant}.png")
        sprite.save(sprite_path)

    # Hero portraits
    print("  Generating hero portraits...")
    for hero_name in HEROES:
        for suffix, is_large in [("Small", False), ("Large", True)]:
            portrait = create_hero_portrait(hero_name, 0, is_large)
            portrait.save(os.path.join(heroes_dir, f"{hero_name}{suffix}.png"))

        # Specialty icons (small only)
        spec_icon = create_icon(hero_name[:4], (180, 150, 80), 32, f"S:{hero_name[:4]}")
        spec_icon.save(os.path.join(heroes_dir, f"{hero_name}SpecSmall.png"))
        spec_icon_lg = create_icon(hero_name[:4], (180, 150, 80), 58, f"S:{hero_name[:5]}")
        spec_icon_lg.save(os.path.join(heroes_dir, f"{hero_name}SpecLarge.png"))

    print(f"\nDone! Generated {total_frames} sprite frames + icons, portraits, and town graphics.")
    print(f"All files saved under: {CONTENT}/sprites/")


if __name__ == "__main__":
    generate_all()
