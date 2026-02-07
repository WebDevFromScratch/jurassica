# Jurassica Asset Generation Guide

Step-by-step guide for replacing placeholder graphics with real artwork using AI tools. No art skills required — just prompts and cleanup.

## Tool Setup

| Tool | Cost | Purpose |
|------|------|---------|
| [PixelLab](https://www.pixellab.ai/) | $9-22/mo | Sprite animation generation |
| [Aseprite](https://www.aseprite.org/) | $20 (one-time) | Sprite cleanup & editing |
| [ElevenLabs](https://elevenlabs.io/sound-effects) | Free tier | Dinosaur sound effects |
| [Flux](https://flux.ai/) / Midjourney | $0-30/mo | Reference images & town screen |
| [Audacity](https://www.audacityteam.org/) | Free | Sound editing |
| GIMP | Free | Image editing fallback |

**Total: ~$50-80 for the first month, ~$10/mo ongoing**

---

## 1. Creature Battle Sprites

### Overview

Each creature needs animated sprite frames for battle. The minimum viable set per creature:

| Animation | Group ID | Frames | Description |
|-----------|----------|--------|-------------|
| Moving | 0 | 4-12 | Walk/fly cycle |
| Idle | 1 | 3-6 | Standing breathing |
| Getting hit | 2 | 3-6 | Flinch/stagger |
| Defend | 3 | 2-4 | Blocking stance |
| Death | 4 | 4-8 | Falling/collapse |
| Attack up | 11 | 4-8 | Strike upward |
| Attack forward | 12 | 4-8 | Strike forward |
| Attack down | 13 | 4-8 | Strike downward |
| Start moving | 20 | 2-3 | Begin to walk |
| End moving | 21 | 2-3 | Stop walking |

For ranged creatures (Pterodactyl, Quetzalcoatlus), also add groups 14-16 (ranged attack up/forward/down).

### Step-by-Step: PixelLab Workflow

#### 1. Generate a reference image

Use Flux or Midjourney to create the creature's "base look":

```
Prompt: "[Creature name], side view facing right, fantasy battle sprite,
Heroes of Might and Magic 3 art style, detailed pixel art, 3/4 isometric
perspective, transparent background, medieval fantasy, warm lighting"
```

Creature-specific prompt additions:
- **Ozimek**: "small gliding reptile, wing membranes on hind limbs, ~90cm, Triassic era"
- **Raptor**: "velociraptor, sickle claws, pack hunter, feathered"
- **Triceratops**: "three horns, massive bony frill, armored"
- **Stegosaurus**: "back plates, thagomizer tail spikes"
- **Pterodactyl**: "flying reptile, large wingspan, beak, airborne"
- **Quetzalcoatlus**: "enormous pterosaur, 12m wingspan, giraffe-sized"
- **Elasmosaurus**: "long-necked marine reptile, plesiosaur"
- **Mosasaurus**: "massive sea predator, powerful jaws"
- **T-Rex**: "tyrannosaurus rex, massive jaws, tiny arms, muscular"
- **Giganotosaurus**: "larger than T-Rex, slashing teeth, massive head"

#### 2. Feed reference to PixelLab

1. Open [PixelLab](https://www.pixellab.ai/)
2. Upload your reference image as a "style reference"
3. Set canvas size to match creature (see sizes below)
4. Use text-to-sprite to generate each animation

**Recommended sprite sizes:**

| Creature | Canvas Size | Notes |
|----------|------------|-------|
| Ozimek / Ozimek Volans | 80x90 / 90x100 | Small creatures |
| Raptor / Utahraptor | 100x110 / 120x130 | Medium |
| Triceratops / Torosaurus | 150x130 / 160x140 | Large, double-wide |
| Stegosaurus / Kentrosaurus | 160x120 / 170x130 | Large, double-wide |
| Pterodactyl | 140x100 | Medium, flying |
| Quetzalcoatlus | 180x120 | Large, flying |
| Elasmosaurus / Mosasaurus | 180x130 / 200x140 | Large |
| T-Rex | 200x180 | Very large |
| Giganotosaurus | 220x200 | Largest |

#### 3. Generate animation frames

For each animation group, prompt PixelLab:

- **Idle**: "[Creature] standing idle, breathing, side view facing right"
- **Walk**: "[Creature] walking cycle, side view facing right"
- **Attack forward**: "[Creature] attacking/biting forward, side view"
- **Attack up**: "[Creature] attacking/biting upward, side view"
- **Attack down**: "[Creature] attacking/biting downward, side view"
- **Hit**: "[Creature] getting hit, flinching, side view"
- **Death**: "[Creature] falling down dead, side view"
- **Defend**: "[Creature] defensive stance, bracing, side view"

#### 4. Export and clean up

1. Export each frame as transparent PNG
2. Open in Aseprite or GIMP
3. Ensure all frames have the same canvas size
4. Check that the creature is consistently positioned (feet at same Y position)
5. Fix any AI inconsistencies (extra limbs, color shifts, etc.)
6. Save as `[animation]_00.png`, `[animation]_01.png`, etc.

#### 5. Place files

Put frames in `Content/sprites/creatures/[name]/`:
```
idle_00.png, idle_01.png, idle_02.png
move_00.png, move_01.png, move_02.png, move_03.png
atkFwd_00.png, atkFwd_01.png, atkFwd_02.png, atkFwd_03.png
...
```

The animation JSON descriptors are already set up to reference these filenames.

### Tips for Consistency

- **Always use the same style reference** across all creatures
- **Keep the same perspective** — 3/4 isometric, creature facing RIGHT
- **Ground line** should be consistent — creatures' feet at the bottom of the canvas
- **Color palette** — aim for the warm, slightly muted tones of original HoMM3
- Generate all frames for one creature before moving to the next

---

## 2. Creature Icons

Two sizes needed per creature:
- **Small icon**: 32x32px (army bar, exchange screen)
- **Large icon**: 58x64px (town screen, creature info)

### Prompt

```
"[Creature name] portrait, head/bust view, fantasy art style, Heroes of
Might and Magic 3, detailed, ornate frame, [size]px, transparent background"
```

Save to `Content/sprites/icons/[name]Small.png` and `[name]Large.png`.

---

## 3. Sound Effects

### ElevenLabs Workflow

1. Go to [ElevenLabs Sound Effects](https://elevenlabs.io/sound-effects)
2. Generate each sound with descriptive prompts:

| Sound | Prompt Template |
|-------|----------------|
| Attack | "[Creature] aggressive bite/slash attack sound, fantasy game" |
| Defend | "[Creature] defensive grunt, bracing for impact" |
| Killed | "[Creature] death cry, falling, dramatic" |
| Move | "[Creature] footsteps walking, [light/heavy]" |
| Wince | "[Creature] pain cry, getting hit" |
| Start Moving | "[Creature] beginning to move, single step" |
| End Moving | "[Creature] stopping, final step" |
| Shoot | "Bone projectile whoosh, fantasy ranged attack" (ranged only) |

### Sound prompt modifiers by creature

- **Ozimek**: "small reptile, chirping, light flapping"
- **Raptor**: "velociraptor, snarling, hissing, quick"
- **Triceratops**: "large herbivore, deep bellow, heavy stomping"
- **Stegosaurus**: "armored dinosaur, deep rumble, tail swish"
- **Pterodactyl**: "flying reptile, screech, wing flapping"
- **Elasmosaurus**: "sea monster, underwater roar, splash"
- **T-Rex**: "tyrannosaurus, earth-shaking roar, thunderous"
- **Giganotosaurus**: "massive theropod, deeper than T-Rex, devastating roar"

### Post-processing

1. Download as WAV
2. Open in Audacity
3. Trim to appropriate length (0.5-2 seconds for most, up to 3s for death)
4. Normalize volume
5. Export as WAV (22050 Hz, 16-bit, mono — HoMM3 standard)
6. Save to `Content/sounds/creatures/[name][Sound].wav`

---

## 4. Town Screen

### Background (800x374)

Generate with Flux/Midjourney:

```
"Prehistoric jungle town with volcano in background, Heroes of Might and
Magic 3 town screen art style, 800x374 pixels, medieval fantasy buildings
made of stone and bone, lush ferns and palm trees, lava streams, amber
deposits, warm lighting, detailed painted style, no text"
```

Save to `Content/sprites/towns/jurassica/townBackground.png`.

### Buildings

For each building, generate a small sprite and position it on the town screen:
- Use inpainting (BRIA Inpaint or Stable Diffusion) to add buildings to the background
- Or generate buildings separately with transparent backgrounds and composite them

### Hall/Guild Backgrounds

Similar to town background but focused on indoor scenes:
- Hall: "prehistoric stone hall interior, bone decorations, torch-lit"
- Guild: "shamanistic magic chamber, amber crystals, fern decorations"

---

## 5. Hero Portraits

Two sizes: 32x32 (small) and 58x64 (large).

### Prompt Template

```
"Fantasy hero portrait, [gender] [class description], prehistoric/tribal
aesthetic, Heroes of Might and Magic 3 art style, head and shoulders,
ornate border, [size]px"
```

Class descriptions:
- **Warchief**: "muscular warrior in dinosaur bone armor, tribal war paint"
- **Sauromancer**: "mystical shaman with amber staff, fern headdress, glowing eyes"

---

## 6. Adventure Map Sprites

Town needs sprites for village/fort/citadel/castle stages. Generate as 32x32 pixel art:

```
"Tiny isometric prehistoric town, pixel art, 32x32, transparent background,
[stage: small huts / wooden walls / stone walls / full castle]"
```

---

## 7. Town Music

Use [Udio](https://www.udio.com/) or [Suno](https://suno.ai/):

```
"Ambient prehistoric jungle music, tribal drums, wooden flutes, bird calls,
distant volcano rumble, mysterious and ancient, fantasy game soundtrack,
looping, 2 minutes"
```

Export as OGG, save to `Content/music/jurassicaTown.ogg`.

---

## Workflow Summary

**Recommended order** (get playable ASAP):

1. **T-Rex first** — the star creature, most exciting for playtesting
2. **All 7 base creatures** — one at a time, using the same PixelLab style reference
3. **Sound effects** — batch generate on ElevenLabs in one session
4. **Town background** — single image generation
5. **Hero portraits** — batch generate
6. **7 upgrade creatures** — similar to base but larger/more detailed
7. **Town buildings** — most time-consuming, save for last

**Time estimate**: ~2-4 hours per creature, ~30-60 hours total for all assets.
