#!/usr/bin/env python3
"""
Process AI-generated building art for the Jurassica VCMI mod.

Takes raw AI-generated building images and produces all VCMI-ready files:
  - Building sprite PNG (resized, background removed)
  - Area mask (white where clickable)
  - Border mask (gold hover outline)
  - 44x44 hall icon
  - Preview composite over town background

Usage:
  python process_building_art.py <building_key> <input_image.png>
  python process_building_art.py --batch raw/
  python process_building_art.py --show-prompt dwelling7
  python process_building_art.py --show-prompt --all
  python process_building_art.py dwelling7 raw/dwelling7.png --update-config

Requirements: pip install Pillow
"""

import argparse
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(BASE, "Mods", "jurassica", "Content")
BUILDINGS_DIR = os.path.join(CONTENT, "sprites", "towns", "jurassica", "buildings")
TOWN_BG_PATH = os.path.join(CONTENT, "sprites", "towns", "jurassica", "townBackground.png")
CONFIG_PATH = os.path.join(CONTENT, "config", "jurassica.json")
PREVIEWS_DIR = os.path.join(BASE, "previews")
RAW_DIR = os.path.join(BASE, "raw")

# Original placeholder size (all buildings were 100x80)
ORIG_W, ORIG_H = 100, 80

# Building sizes by category (2x original scale for 800x374 town background)
BUILDING_SIZES = {
    # Grand (400x348)
    "capitol":       (400, 348),
    "castle":        (400, 348),
    # Large (320x300)
    "cityHall":      (320, 300),
    "citadel":       (320, 300),
    "grail":         (320, 300),
    # Medium-Large (280x240)
    "townHall":      (280, 240),
    "fort":          (280, 240),
    "dwelling5":     (280, 240),
    "dwelling6":     (280, 240),
    "upgDwelling5":  (280, 240),
    "upgDwelling6":  (280, 240),
    "dwelling7":     (280, 240),
    "upgDwelling7":  (280, 240),
    # Medium (240x200)
    "villageHall":   (240, 200),
    "mageGuild1":    (240, 200),
    "mageGuild2":    (240, 200),
    "mageGuild3":    (240, 200),
    "mageGuild4":    (240, 200),
    "dwelling1":     (240, 200),
    "dwelling2":     (240, 200),
    "dwelling3":     (240, 200),
    "dwelling4":     (240, 200),
    "upgDwelling1":  (240, 200),
    "upgDwelling2":  (240, 200),
    "upgDwelling3":  (240, 200),
    "upgDwelling4":  (240, 200),
    "special1":      (240, 200),
    "special2":      (240, 200),
    "special3":      (240, 200),
    "special4":      (240, 200),
    # Small (200x160)
    "tavern":        (200, 160),
    "marketplace":   (200, 160),
    "resourceSilo":  (200, 160),
    "blacksmith":    (200, 160),
    "horde1":        (200, 160),
}

# Current positions from jurassica.json (x, y for each building)
BUILDING_POSITIONS = {
    "villageHall":   (0, 200),
    "townHall":      (0, 200),
    "cityHall":      (0, 200),
    "capitol":       (0, 200),
    "fort":          (350, 30),
    "citadel":       (350, 30),
    "castle":        (350, 30),
    "mageGuild1":    (680, 100),
    "mageGuild2":    (680, 100),
    "mageGuild3":    (680, 100),
    "mageGuild4":    (680, 100),
    "tavern":        (120, 240),
    "marketplace":   (460, 260),
    "resourceSilo":  (460, 180),
    "blacksmith":    (120, 150),
    "dwelling1":     (240, 120),
    "dwelling2":     (580, 200),
    "dwelling3":     (240, 220),
    "dwelling4":     (580, 120),
    "dwelling5":     (350, 140),
    "dwelling6":     (350, 260),
    "dwelling7":     (700, 220),
    "upgDwelling1":  (240, 120),
    "upgDwelling2":  (580, 200),
    "upgDwelling3":  (240, 220),
    "upgDwelling4":  (580, 120),
    "upgDwelling5":  (350, 140),
    "upgDwelling6":  (350, 260),
    "upgDwelling7":  (700, 220),
    "horde1":        (580, 280),
    "special1":      (0, 120),
    "special2":      (460, 100),
    "special3":      (700, 30),
    "special4":      (120, 60),
    "grail":         (350, 200),
}

# Building names (for prompt generation)
BUILDING_NAMES = {
    "villageHall":   "Village Hall",
    "townHall":      "Town Hall",
    "cityHall":      "City Hall",
    "capitol":       "Capitol",
    "fort":          "Fort",
    "citadel":       "Citadel",
    "castle":        "Castle",
    "mageGuild1":    "Circle of Elders I",
    "mageGuild2":    "Circle of Elders II",
    "mageGuild3":    "Circle of Elders III",
    "mageGuild4":    "Circle of Elders IV",
    "tavern":        "Watering Hole",
    "marketplace":   "Trading Grounds",
    "resourceSilo":  "Sulfur Vent",
    "blacksmith":    "Fossil Forge",
    "dwelling1":     "Glider Nest",
    "dwelling2":     "Raptor Den",
    "dwelling3":     "Ceratopsian Pen",
    "dwelling4":     "Plated Enclosure",
    "dwelling5":     "Pterosaur Roost",
    "dwelling6":     "Tidal Grotto",
    "dwelling7":     "Primeval Throne",
    "upgDwelling1":  "Volans Aerie",
    "upgDwelling2":  "Predator Lair",
    "upgDwelling3":  "Armored Stockade",
    "upgDwelling4":  "Spike Yard",
    "upgDwelling5":  "Sky Citadel",
    "upgDwelling6":  "Abyssal Pool",
    "upgDwelling7":  "Extinction Arena",
    "horde1":        "Breeding Grounds",
    "special1":      "Tar Pits",
    "special2":      "Amber Mine",
    "special3":      "Fossil Museum",
    "special4":      "Primordial Spring",
    "grail":         "Heart of Pangaea",
}

# Common prompt suffix for style, perspective, and background
_PROMPT_SUFFIX = (
    "HoMM3 painted art style, 3/4 isometric perspective, warm sunset lighting, "
    "the building must be fully self-contained and enclosed within the image — "
    "no elements cropped or extending beyond the edges, "
    "isolated on plain white background"
)

# Upgrade prompt instruction — tells AI to re-iterate on the base dwelling image
def _upg_prompt(base_key, base_desc, upgrade_desc):
    """Build an upgrade dwelling prompt that references the base dwelling.

    The prompt instructs the AI to take the EXACT image generated for the base
    dwelling and produce an upgraded/enhanced version of that same building,
    ensuring visual consistency between base and upgraded forms.
    """
    return (
        f"IMPORTANT: Use the attached image of the base '{BUILDING_NAMES[base_key]}' building "
        f"as the starting point. Re-iterate on this EXACT building to create its upgraded form. "
        f"Keep the same core structure, shape, and composition, but enhance it: {upgrade_desc} "
        f"The upgrade should be clearly recognizable as an enhanced version of the original. "
        f"{_PROMPT_SUFFIX}"
    )


# AI image generation prompts for each building
BUILDING_PROMPTS = {
    "villageHall": (
        "Prehistoric dinosaur village hall, simple thatched hut with dinosaur bone frame and "
        "fern-leaf roof, wooden platform with carved totem pole, primitive tribal settlement, "
        f"{_PROMPT_SUFFIX}"
    ),
    "townHall": (
        "Prehistoric dinosaur town hall, larger wooden longhouse with dinosaur rib-bone arches, "
        "thatched roof decorated with skulls and feathers, raised stone foundation, "
        f"tribal banners hanging from posts, {_PROMPT_SUFFIX}"
    ),
    "cityHall": (
        "Prehistoric dinosaur city hall, grand wooden and stone structure with massive dinosaur "
        "jawbone entrance arch, tiered thatched roofs, carved bone columns, amber lanterns, "
        f"{_PROMPT_SUFFIX}"
    ),
    "capitol": (
        "Prehistoric dinosaur capitol building, massive volcanic stone palace with T-Rex skull "
        "crowning the entrance, bone pillars and obsidian walls, flowing lava channels in the "
        "foundation, amber-crystal windows, tribal banners, the most impressive building in a "
        f"dinosaur town, {_PROMPT_SUFFIX}"
    ),
    "fort": (
        "Prehistoric dinosaur fort, wooden palisade walls reinforced with dinosaur bones, "
        "watchtower made from stacked logs and a pterodactyl skull, crude stone gate, "
        f"{_PROMPT_SUFFIX}"
    ),
    "citadel": (
        "Prehistoric dinosaur citadel, thick stone walls with embedded fossils, taller watchtowers "
        "with bone-spike battlements, reinforced gate with triceratops horn decorations, "
        f"{_PROMPT_SUFFIX}"
    ),
    "castle": (
        "Prehistoric dinosaur castle, massive volcanic stone fortress with obsidian-tipped towers, "
        "walls reinforced with giant dinosaur bones, T-Rex skull gate, lava moat visible at base, "
        f"the ultimate prehistoric fortification, {_PROMPT_SUFFIX}"
    ),
    "mageGuild1": (
        "Prehistoric shaman hut level 1, small dome-shaped mud hut with glowing amber crystals, "
        "carved bone totems around entrance, mystical fern garden, smoke rising from top, "
        f"{_PROMPT_SUFFIX}"
    ),
    "mageGuild2": (
        "Prehistoric shaman tower level 2, taller mud-and-stone structure with two tiers, "
        "glowing amber crystals embedded in walls, bone wind chimes, mystical smoke, "
        f"{_PROMPT_SUFFIX}"
    ),
    "mageGuild3": (
        "Prehistoric shaman tower level 3, three-tiered stone and bone tower with swirling "
        "magical energy, large amber crystal at top, carved fossil runes on walls, "
        f"{_PROMPT_SUFFIX}"
    ),
    "mageGuild4": (
        "Prehistoric shaman tower level 4, tall four-tiered mystical tower built from volcanic "
        "stone and giant bones, massive glowing amber crystal crown, magical aura surrounding it, "
        "ancient fossil runes glowing on every surface, most powerful magic building, "
        f"{_PROMPT_SUFFIX}"
    ),
    "tavern": (
        "Prehistoric dinosaur tavern, cozy wooden hut with a smoking chimney, dinosaur hide "
        "curtain door, wooden tables visible inside, hanging dried meat, watering trough outside, "
        f"{_PROMPT_SUFFIX}"
    ),
    "marketplace": (
        "Prehistoric dinosaur marketplace, open-air wooden stalls with thatched awnings, "
        "piles of amber and gems on display, bone-frame trading post, primitive scales, "
        f"{_PROMPT_SUFFIX}"
    ),
    "resourceSilo": (
        "Prehistoric sulfur vent, natural volcanic fissure with yellow-green sulfur deposits, "
        "crude wooden collection apparatus, steam rising, crystallized sulfur formations, "
        f"{_PROMPT_SUFFIX}"
    ),
    "blacksmith": (
        "Prehistoric dinosaur forge, stone anvil with bone hammer, small volcanic vent used as "
        "furnace, obsidian weapons on display, leather bellows, smoke and sparks, "
        f"{_PROMPT_SUFFIX}"
    ),
    "dwelling1": (
        "Prehistoric glider nest, elevated wooden platform in a tall tree with vine ladders, "
        "nest made of woven ferns and twigs, small flying lizard silhouettes, "
        "home for tiny gliding reptiles (ozimek), "
        f"{_PROMPT_SUFFIX}"
    ),
    "dwelling2": (
        "Prehistoric raptor den, rocky cave entrance with claw marks, scattered bones around, "
        "shadowy interior, raptor footprints in mud, crude bone fence, "
        f"home for velociraptors, {_PROMPT_SUFFIX}"
    ),
    "dwelling3": (
        "Prehistoric ceratopsian pen, sturdy wooden and stone corral with reinforced log fence, "
        "feeding trough with ferns, muddy ground, gate decorated with a triceratops horn, "
        f"{_PROMPT_SUFFIX}"
    ),
    "dwelling4": (
        "Prehistoric plated dinosaur enclosure, stone-walled paddock with crystal-embedded walls, "
        "thick vegetation, armored dinosaur silhouette, reinforced gate, "
        f"home for stegosaurus, {_PROMPT_SUFFIX}"
    ),
    "dwelling5": (
        "Prehistoric pterosaur roost, tall rocky spire with wooden platforms and nesting ledges, "
        "pterodactyl nests at different heights, wind-swept vines, cliff-side perches, "
        f"{_PROMPT_SUFFIX}"
    ),
    "dwelling6": (
        "Prehistoric tidal grotto, coastal cave entrance with water flowing in, bioluminescent "
        "algae glowing inside, tidal pool with prehistoric marine life, coral formations, "
        f"home for sea dinosaurs, {_PROMPT_SUFFIX}"
    ),
    "dwelling7": (
        "Prehistoric primeval throne, massive volcanic stone structure with T-Rex skull entrance, "
        "obsidian pillars, lava veins running through walls, bone throne visible inside, "
        "the most fearsome dwelling for the mightiest dinosaur, "
        f"{_PROMPT_SUFFIX}"
    ),
    "horde1": (
        "Prehistoric breeding grounds, fenced area with multiple nesting mounds, "
        "crushed eggshells, heat lamps made from volcanic vents, raptor egg incubators, "
        f"{_PROMPT_SUFFIX}"
    ),
    "special1": (
        "Prehistoric tar pits, bubbling black tar pool with trapped bones visible, "
        "wooden warning totems, sulfurous steam, dark viscous surface, "
        f"{_PROMPT_SUFFIX}"
    ),
    "special2": (
        "Prehistoric amber mine, rocky outcrop with glowing amber deposits, "
        "crude mining equipment, crystallized tree resin formations, golden glow, "
        f"{_PROMPT_SUFFIX}"
    ),
    "special3": (
        "Prehistoric fossil museum, stone building with large fossil skeleton display, "
        "carefully arranged bone exhibits, amber display cases, ancient knowledge, "
        f"{_PROMPT_SUFFIX}"
    ),
    "special4": (
        "Prehistoric primordial spring, magical glowing pool surrounded by ancient ferns, "
        "crystal-clear water with mystical mist, healing energy, enchanted stones, "
        f"{_PROMPT_SUFFIX}"
    ),
    "grail": (
        "Prehistoric Heart of Pangaea, legendary massive structure combining volcanic stone, "
        "giant fossils, and pure amber crystal, glowing with primal earth energy, "
        "the supercontinent's ancient power source, awe-inspiring monument, "
        f"{_PROMPT_SUFFIX}"
    ),
}

# Upgraded dwelling prompts — built dynamically to reference base dwellings
BUILDING_PROMPTS["upgDwelling1"] = _upg_prompt(
    "dwelling1",
    "Glider Nest",
    "add multiple elevated platforms, wind sails made of stretched hide, vine bridges between "
    "platforms, glowing amber lanterns, more elaborate nest structures for flying ozimek volans."
)
BUILDING_PROMPTS["upgDwelling2"] = _upg_prompt(
    "dwelling2",
    "Raptor Den",
    "expand into a multi-entrance cave system, add bone trophy racks at the entrance, "
    "blood-stained stones, stealth netting made of vines, a more menacing and elaborate lair "
    "for utahraptors."
)
BUILDING_PROMPTS["upgDwelling3"] = _upg_prompt(
    "dwelling3",
    "Ceratopsian Pen",
    "reinforce with heavy stone walls and embedded fossils, add an iron-banded gate, "
    "defensive spikes along the perimeter, sturdier construction for torosaurus."
)
BUILDING_PROMPTS["upgDwelling4"] = _upg_prompt(
    "dwelling4",
    "Plated Enclosure",
    "add crystal-studded walls, obsidian spike decorations, glowing crystal formations, "
    "reinforced and more imposing walls for kentrosaurus."
)
BUILDING_PROMPTS["upgDwelling5"] = _upg_prompt(
    "dwelling5",
    "Pterosaur Roost",
    "expand into a taller tower with multiple flight decks, wind-catching sails, "
    "a cloud-touching spire, more nest platforms at various heights for quetzalcoatlus."
)
BUILDING_PROMPTS["upgDwelling6"] = _upg_prompt(
    "dwelling6",
    "Tidal Grotto",
    "deepen into a dark abyssal pool entrance, add bioluminescent coral formations, "
    "ancient sea fossils embedded in walls, a whirlpool effect in the water for mosasaurus."
)
BUILDING_PROMPTS["upgDwelling7"] = _upg_prompt(
    "dwelling7",
    "Primeval Throne",
    "expand into a massive colosseum-like arena structure, add lava channels running through "
    "the walls, skull trophies lining the perimeter, the ultimate gladiatorial arena "
    "for giganotosaurus."
)

# Chroma key colors to remove (green screen, magenta screen)
CHROMA_KEYS = [
    ((0, 200, 0), 80),      # Green screen
    ((0, 255, 0), 80),      # Bright green
    ((255, 0, 255), 80),    # Magenta
]

# Gold border color for hover outline
BORDER_COLOR = (255, 223, 127, 255)  # #FFDF7F


def remove_background(img):
    """Remove green/magenta background via chroma keying, or use existing alpha."""
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size

    # Check if image already has meaningful transparency
    alpha_values = [pixels[x, y][3] for x in range(0, w, max(1, w // 20))
                    for y in range(0, h, max(1, h // 20))]
    transparent_pct = sum(1 for a in alpha_values if a < 128) / len(alpha_values)
    if transparent_pct > 0.1:
        # Already has transparency, skip chroma keying
        return img

    # Try chroma key removal for each key color
    for key_color, tolerance in CHROMA_KEYS:
        kr, kg, kb = key_color
        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                dist = ((r - kr) ** 2 + (g - kg) ** 2 + (b - kb) ** 2) ** 0.5
                if dist < tolerance:
                    pixels[x, y] = (r, g, b, 0)

    # Check if chroma keying did anything
    alpha_after = [pixels[x, y][3] for x in range(0, w, max(1, w // 20))
                   for y in range(0, h, max(1, h // 20))]
    transparent_after = sum(1 for a in alpha_after if a < 128) / len(alpha_after)
    if transparent_after > 0.1:
        return img

    # Fallback: threshold-based removal on corner-sampled background color
    # Sample corners to detect background
    corners = []
    sample = 5
    for cx, cy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        for dx in range(sample):
            for dy in range(sample):
                sx = min(max(cx + dx - sample // 2, 0), w - 1)
                sy = min(max(cy + dy - sample // 2, 0), h - 1)
                corners.append(pixels[sx, sy][:3])

    if corners:
        avg_r = sum(c[0] for c in corners) // len(corners)
        avg_g = sum(c[1] for c in corners) // len(corners)
        avg_b = sum(c[2] for c in corners) // len(corners)
        bg_color = (avg_r, avg_g, avg_b)
        tolerance = 60

        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                dist = ((r - bg_color[0]) ** 2 + (g - bg_color[1]) ** 2 +
                        (b - bg_color[2]) ** 2) ** 0.5
                if dist < tolerance:
                    pixels[x, y] = (r, g, b, 0)

    return img


def resize_building(img, target_w, target_h):
    """Resize image to target dimensions, anchored bottom-center.

    The building is scaled to fit within the target box (preserving aspect ratio),
    then placed so the bottom-center of the result aligns with the bottom-center
    of the target canvas.
    """
    img_w, img_h = img.size

    # Scale to fit within target, preserving aspect ratio
    scale = min(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    resized = img.resize((new_w, new_h), Image.LANCZOS)

    # Create target canvas and paste bottom-center
    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    paste_x = (target_w - new_w) // 2
    paste_y = target_h - new_h  # Anchor to bottom
    canvas.paste(resized, (paste_x, paste_y), resized)

    return canvas


def generate_area_mask(img):
    """Generate area mask from alpha channel.

    White (255) where opaque (clickable), black (0) where transparent.
    Heavily dilated and hole-filled for a generous, solid click target.
    """
    alpha = img.split()[3]  # Get alpha channel

    # Threshold: opaque enough = clickable
    area = alpha.point(lambda p: 255 if p > 64 else 0)

    # Aggressively dilate to merge nearby regions and close gaps
    area = area.filter(ImageFilter.MaxFilter(9))

    # Erode back slightly to keep roughly the original shape but with holes filled
    area = area.filter(ImageFilter.MinFilter(5))

    # Final dilation for generous click target (4px padding)
    area = area.filter(ImageFilter.MaxFilter(9))

    # Convert to RGBA (VCMI expects RGBA masks)
    mask = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pixels = mask.load()
    area_pixels = area.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if area_pixels[x, y] > 128:
                pixels[x, y] = (255, 255, 255, 255)

    return mask


def generate_border_mask(img):
    """Generate border mask (gold outline from alpha edge, 2px thick).

    Creates a gold (#FFDF7F) outline that follows the shape of the building,
    shown on hover in the town screen.
    """
    alpha = img.split()[3]

    # Create binary mask from alpha
    binary = alpha.point(lambda p: 255 if p > 64 else 0)

    # Erode and dilate to find edge
    dilated = binary.filter(ImageFilter.MaxFilter(5))
    eroded = binary.filter(ImageFilter.MinFilter(3))

    # Edge = dilated - eroded
    border = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pixels = border.load()
    dil_pixels = dilated.load()
    ero_pixels = eroded.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            if dil_pixels[x, y] > 128 and ero_pixels[x, y] < 128:
                pixels[x, y] = BORDER_COLOR

    return border


def generate_icon(img, size=44):
    """Generate a 44x44 hall icon by scaling down and centering."""
    # Find bounding box of non-transparent content
    bbox = img.getbbox()
    if bbox is None:
        # Fully transparent, return empty icon
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))

    cropped = img.crop(bbox)
    cw, ch = cropped.size

    # Scale to fit within icon with 2px margin
    inner = size - 4
    scale = min(inner / cw, inner / ch)
    new_w = max(1, int(cw * scale))
    new_h = max(1, int(ch * scale))

    scaled = cropped.resize((new_w, new_h), Image.LANCZOS)

    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    paste_x = (size - new_w) // 2
    paste_y = (size - new_h) // 2
    icon.paste(scaled, (paste_x, paste_y), scaled)

    return icon


def compute_adjusted_position(building_key):
    """Compute adjusted x,y position when building grows from 100x80.

    Center anchor: the building grows equally in all directions from
    the center of the original 100x80 placeholder.
    Returns (new_x, new_y, dx, dy).
    """
    orig_x, orig_y = BUILDING_POSITIONS[building_key]
    new_w, new_h = BUILDING_SIZES[building_key]

    dx = -(new_w - ORIG_W) // 2
    dy = -(new_h - ORIG_H) // 2

    new_x = orig_x + dx
    new_y = orig_y + dy

    return new_x, new_y, dx, dy


def create_preview(building_key, building_img):
    """Composite building over town background at its position."""
    if not os.path.exists(TOWN_BG_PATH):
        print(f"  Warning: Town background not found at {TOWN_BG_PATH}, skipping preview")
        return None

    bg = Image.open(TOWN_BG_PATH).convert("RGBA")
    new_x, new_y, _, _ = compute_adjusted_position(building_key)

    # Clamp to valid range
    new_x = max(0, new_x)
    new_y = max(0, new_y)

    bg.paste(building_img, (new_x, new_y), building_img)
    return bg


def process_building(building_key, input_path, update_config=False):
    """Process a single building image through the full pipeline."""
    if building_key not in BUILDING_SIZES:
        print(f"Error: Unknown building key '{building_key}'")
        print(f"Valid keys: {', '.join(sorted(BUILDING_SIZES.keys()))}")
        return False

    target_w, target_h = BUILDING_SIZES[building_key]

    print(f"\nProcessing: {building_key} ({BUILDING_NAMES.get(building_key, '?')})")
    print(f"  Input:  {input_path}")
    print(f"  Target: {target_w}x{target_h}")

    # Load and process
    try:
        raw = Image.open(input_path)
    except Exception as e:
        print(f"  Error loading image: {e}")
        return False

    print(f"  Raw size: {raw.size[0]}x{raw.size[1]}, mode: {raw.mode}")

    # Step 1: Remove background
    img = remove_background(raw)
    print("  Background removal: done")

    # Step 2: Resize to target dimensions
    img = resize_building(img, target_w, target_h)
    print(f"  Resized to: {target_w}x{target_h}")

    # Step 3: Generate area mask
    area = generate_area_mask(img)

    # Step 4: Generate border mask
    border = generate_border_mask(img)

    # Step 5: Generate icon
    icon = generate_icon(img)

    # Step 6: Save all files
    os.makedirs(BUILDINGS_DIR, exist_ok=True)

    sprite_path = os.path.join(BUILDINGS_DIR, f"{building_key}.png")
    area_path = os.path.join(BUILDINGS_DIR, f"{building_key}_area.png")
    border_path = os.path.join(BUILDINGS_DIR, f"{building_key}_border.png")
    icon_path = os.path.join(BUILDINGS_DIR, f"{building_key}_icon.png")

    img.save(sprite_path)
    area.save(area_path)
    border.save(border_path)
    icon.save(icon_path)

    print(f"  Saved: {building_key}.png, {building_key}_area.png, "
          f"{building_key}_border.png, {building_key}_icon.png")

    # Step 7: Create preview
    os.makedirs(PREVIEWS_DIR, exist_ok=True)
    preview = create_preview(building_key, img)
    if preview:
        preview_path = os.path.join(PREVIEWS_DIR, f"{building_key}_preview.png")
        preview.save(preview_path)
        print(f"  Preview: {preview_path}")

    # Step 8: Report position adjustments
    new_x, new_y, dx, dy = compute_adjusted_position(building_key)
    if dx != 0 or dy != 0:
        orig_x, orig_y = BUILDING_POSITIONS[building_key]
        print(f"  Position: ({orig_x},{orig_y}) -> ({new_x},{new_y})  "
              f"(dx={dx:+d}, dy={dy:+d})")

        if update_config:
            update_building_config(building_key, new_x, new_y)
    else:
        print(f"  Position: unchanged ({new_x},{new_y})")

    return True


def update_building_config(building_key, new_x, new_y):
    """Update the x,y position in jurassica.json for a building."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)

        structures = config["jurassica"]["town"]["structures"]
        if building_key in structures:
            old_x = structures[building_key]["x"]
            old_y = structures[building_key]["y"]
            structures[building_key]["x"] = new_x
            structures[building_key]["y"] = new_y

            with open(CONFIG_PATH, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"  Config updated: {building_key} ({old_x},{old_y}) -> ({new_x},{new_y})")
        else:
            print(f"  Warning: {building_key} not found in config structures")

    except Exception as e:
        print(f"  Error updating config: {e}")


def show_prompt(building_key):
    """Print the AI generation prompt for a building."""
    if building_key not in BUILDING_PROMPTS:
        print(f"Error: Unknown building key '{building_key}'")
        return

    name = BUILDING_NAMES.get(building_key, building_key)
    size = BUILDING_SIZES.get(building_key, (100, 80))

    print(f"\n=== {building_key} ({name}) — target {size[0]}x{size[1]} ===")
    print()
    print(BUILDING_PROMPTS[building_key])
    print()

    # For upgrade dwellings, remind user to attach the base dwelling image
    if building_key.startswith("upgDwelling"):
        base_key = building_key.replace("upg", "").replace("D", "d")
        base_name = BUILDING_NAMES.get(base_key, base_key)
        print(f"*** IMPORTANT: Attach the image of '{base_name}' (raw/{base_key}.png) ***")
        print(f"*** as input/reference when generating this upgrade. ***")
        print()

    print(f"Suggested input resolution: {size[0] * 4}x{size[1] * 4} or higher")
    print(f"Save as: raw/{building_key}.png")


def show_all_prompts():
    """Print prompts for all buildings, grouped by phase."""
    phases = {
        "Phase 1 (most visible, start here)": [
            "villageHall", "fort", "dwelling7", "mageGuild1", "tavern"
        ],
        "Phase 2 (dwellings — faction identity)": [
            "dwelling1", "dwelling2", "dwelling3", "dwelling4", "dwelling5", "dwelling6",
            "upgDwelling1", "upgDwelling2", "upgDwelling3", "upgDwelling4", "upgDwelling5", "upgDwelling6",
        ],
        "Phase 3 (progression tiers)": [
            "townHall", "cityHall", "capitol", "citadel", "castle",
            "mageGuild2", "mageGuild3", "mageGuild4",
        ],
        "Phase 4 (remaining)": [
            "marketplace", "blacksmith", "resourceSilo", "horde1", "upgDwelling7",
            "special1", "special2", "special3", "special4", "grail",
        ],
    }

    for phase_name, keys in phases.items():
        print(f"\n{'=' * 60}")
        print(f"  {phase_name}")
        print(f"{'=' * 60}")
        for key in keys:
            show_prompt(key)


def batch_process(raw_dir, update_config=False):
    """Process all <key>.png files found in raw_dir."""
    if not os.path.isdir(raw_dir):
        print(f"Error: Directory not found: {raw_dir}")
        return

    processed = 0
    skipped = 0

    for filename in sorted(os.listdir(raw_dir)):
        if not filename.lower().endswith(".png"):
            continue

        key = os.path.splitext(filename)[0]
        if key not in BUILDING_SIZES:
            print(f"  Skipping {filename} ('{key}' is not a valid building key)")
            skipped += 1
            continue

        input_path = os.path.join(raw_dir, filename)
        if process_building(key, input_path, update_config):
            processed += 1
        else:
            skipped += 1

    print(f"\nBatch complete: {processed} processed, {skipped} skipped")


def main():
    parser = argparse.ArgumentParser(
        description="Process AI-generated building art for Jurassica VCMI mod",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s dwelling7 raw/dwelling7.png          Process single building
  %(prog)s --batch raw/                          Process all <key>.png in raw/
  %(prog)s --show-prompt dwelling7               Show AI prompt for one building
  %(prog)s --show-prompt --all                   Show all AI prompts by phase
  %(prog)s dwelling7 raw/dwelling7.png --update-config  Process and update config
        """,
    )

    parser.add_argument("building_key", nargs="?", help="Building key (e.g. dwelling7)")
    parser.add_argument("input_image", nargs="?", help="Path to raw input PNG")
    parser.add_argument("--batch", metavar="DIR", help="Batch process all <key>.png in DIR")
    parser.add_argument("--show-prompt", action="store_true", help="Show AI generation prompt")
    parser.add_argument("--all", action="store_true", help="With --show-prompt, show all prompts")
    parser.add_argument("--update-config", action="store_true",
                        help="Update jurassica.json with adjusted positions")

    args = parser.parse_args()

    # --show-prompt mode
    if args.show_prompt:
        if args.all:
            show_all_prompts()
        elif args.building_key:
            show_prompt(args.building_key)
        else:
            parser.error("--show-prompt requires a building_key or --all")
        return

    # --batch mode
    if args.batch:
        batch_process(args.batch, args.update_config)
        return

    # Single building mode
    if args.building_key and args.input_image:
        success = process_building(args.building_key, args.input_image, args.update_config)
        sys.exit(0 if success else 1)

    parser.print_help()


if __name__ == "__main__":
    main()
