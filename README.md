# Jurassica — Dinosaur Faction for Heroes of Might and Magic 3 (VCMI)

A complete dinosaur faction mod for VCMI (open-source HoMM3 engine). Features 7 tiers of prehistoric creatures, from the tiny Ozimek glider to the mighty Giganotosaurus.

**Designed by a 5-year-old paleontology enthusiast!**

## Creature Lineup

| Lvl | Base | Upgrade | Key Abilities |
|-----|------|---------|--------------|
| 1 | Ozimek | Ozimek Volans | Fast, numerous. Upgrade gains Flying |
| 2 | Raptor | Utahraptor | Strikes first, upgrade has breath attack |
| 3 | Triceratops | Torosaurus | Jousting charge, tanky |
| 4 | Stegosaurus | Kentrosaurus | Extra retaliations (thagomizer!) |
| 5 | Pterodactyl | Quetzalcoatlus | Flying ranged shooter |
| 6 | Elasmosaurus | Mosasaurus | Breath attack + defense reduction |
| 7 | T-Rex | Giganotosaurus | Fear, breath, morale reduction |

## Quick Start

### Prerequisites

1. **HoMM3 Complete** — buy on [GOG](https://www.gog.com/game/heroes_of_might_and_magic_3_complete_edition) (~$10)
2. **VCMI** — download from [vcmi.eu](https://vcmi.eu/) and install on top of your HoMM3

### Installation

1. Copy the `jurassica/` folder into your VCMI `Mods/` directory:
   - **macOS**: `~/Library/Application Support/vcmi/Mods/`
   - **Windows**: `%APPDATA%/vcmi/Mods/`
   - **Linux**: `~/.local/share/vcmi/Mods/`

2. Launch VCMI, go to **Mods** in the launcher, and enable **Jurassica**

3. Start a new game — Jurassica should appear as a faction choice!

### Current State

This mod ships with **placeholder graphics** (colored shapes with labels). It is fully playable in VCMI but needs real artwork. See `ASSET_GUIDE.md` for instructions on generating proper sprites with AI tools.

## Mod Structure

```
jurassica/
├── mod.json                              # Mod descriptor
├── Content/
│   ├── config/
│   │   ├── factions/jurassica.json       # Faction + town definition
│   │   ├── creatures/                    # 14 creature configs
│   │   │   ├── ozimek.json ... trex.json
│   │   │   └── (7 base + 7 upgrades)
│   │   └── heroes/
│   │       ├── heroClasses.json          # Warchief + Sauromancer
│   │       └── heroes.json               # 16 heroes
│   ├── sprites/
│   │   ├── creatures/                    # Battle animations (PNG + JSON)
│   │   ├── towns/jurassica/              # Town screen graphics
│   │   ├── adventure/                    # Adventure map sprites
│   │   ├── icons/                        # UI icons
│   │   └── heroes/                       # Hero portraits
│   ├── sounds/creatures/                 # Sound effects (WAV)
│   └── music/                            # Town music (OGG)
├── generate_placeholders.py              # Regenerate placeholder art
├── generate_animation_jsons.py           # Regenerate animation descriptors
├── README.md
└── ASSET_GUIDE.md                        # How to create real assets
```

## Hero Classes

- **Warchief** — Might-oriented dinosaur riders (high Attack/Defense)
- **Sauromancer** — Magic-oriented primal shamans (high Spell Power/Knowledge)

## Special Buildings

- **Tar Pits** — Enhances town defense
- **Nesting Grounds** — Increases Ozimek growth by +6/week
- **Fossil Excavation** — Visiting heroes gain +1000 XP
- **Primordial Nexus** (Grail) — +5000 gold/day, +10 all stats for defenders

## Development

### Regenerating Placeholders

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install Pillow
python3 generate_placeholders.py
python3 generate_animation_jsons.py
```

### Replacing with Real Art

See `ASSET_GUIDE.md` for the complete workflow using PixelLab, ElevenLabs, and other AI tools.

When replacing a creature's placeholder:
1. Put your PNG frames in `Content/sprites/creatures/<name>/`
2. Update the animation JSON in the same folder
3. Reload the mod in VCMI

### Testing

- VCMI logs mod errors to `VCMI_Client_log.txt` — check there first
- Use the VCMI map editor to create test maps with Jurassica towns
- Test creature balance by fighting AI armies

## Credits

- Creature lineup designed by a young paleontologist
- Built for [VCMI](https://vcmi.eu/) — open-source HoMM3 engine
- Placeholder art generated with Python + Pillow

## License

Creative Commons Attribution 4.0 (CC BY 4.0)
