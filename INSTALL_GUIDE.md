# Jurassica Installation Guide — Step by Step

Complete guide to getting the Jurassica dinosaur faction running in Heroes of Might and Magic 3 on macOS.

---

## Step 1: Get Heroes of Might and Magic 3

You need a legal copy of the original game data files.

**Option A — GOG (Recommended)**
1. Go to [GOG.com](https://www.gog.com/game/heroes_of_might_and_magic_3_complete_edition)
2. Buy "Heroes of Might and Magic 3: Complete" (~$10)
3. Download the **offline installer** (not the GOG Galaxy version)
4. Keep the installer `.exe` file — you'll point VCMI at it in Step 3

**Option B — Existing HoMM3 installation**
If you already have HoMM3 installed (e.g., from an old CD or Steam), you just need the `Data/`, `Maps/`, and `Mp3/` folders from that installation.

---

## Step 2: Install VCMI

VCMI is the open-source engine that replaces the original HoMM3 executable and adds mod support.

### Method A — Homebrew (Recommended)

Open Terminal and run:

```bash
brew install --cask --no-quarantine vcmi/vcmi/vcmi
```

This installs the VCMI app to `/Applications/VCMI.app`.

### Method B — Direct Download

1. Go to [https://vcmi.eu/players/Installation_macOS/](https://vcmi.eu/players/Installation_macOS/)
2. Download the latest `.dmg` file
3. Open the `.dmg` and drag VCMI to your Applications folder
4. On first launch, macOS will block it. Go to:
   - **System Settings → Privacy & Security** → scroll down → click **Open Anyway**
   - On macOS 15 (Sequoia)+, you may need to do this multiple times

---

## Step 3: Import HoMM3 Game Data

VCMI needs the original HoMM3 data files to work.

1. **Launch VCMI** from Applications
2. The launcher will show a setup wizard asking for HoMM3 data
3. **If you have the GOG offline installer** (`.exe` file):
   - Click "Import from GOG installer" or point the launcher to the `.exe` file
   - VCMI will extract the needed files automatically
4. **If you have an existing HoMM3 folder:**
   - Copy these folders into `~/Library/Application Support/vcmi/`:
     - `Data/`
     - `Maps/`
     - `Mp3/`

To find the VCMI data folder easily, open Terminal:
```bash
open ~/Library/Application\ Support/vcmi/
```

After importing, the VCMI launcher should show "Heroes III data files found" or similar.

---

## Step 4: Install the Jurassica Mod

1. Open Terminal and navigate to the Jurassica project:
   ```bash
   open ~/Library/Application\ Support/vcmi/Mods/
   ```

2. Copy the `jurassica` mod folder there. From the project directory:
   ```bash
   cp -R /Users/piotr/Desktop/work/jurassica/Mods/jurassica ~/Library/Application\ Support/vcmi/Mods/
   ```

   Your folder structure should look like:
   ```
   ~/Library/Application Support/vcmi/Mods/
   └── jurassica/
       ├── mod.json
       └── Content/
           ├── config/
           ├── sprites/
           ├── sounds/
           └── music/
   ```

3. **Verify** the mod is in the right place:
   ```bash
   ls ~/Library/Application\ Support/vcmi/Mods/jurassica/
   ```
   You should see `mod.json` and `Content/`.

---

## Step 5: Enable the Mod in VCMI Launcher

1. Launch **VCMI** from Applications
2. In the launcher, click the **Mods** tab
3. Find **Jurassica** in the mod list
4. Click the toggle/checkbox to **enable** it
5. If there are any dependency warnings, resolve them (Jurassica has no dependencies beyond base VCMI)

---

## Step 6: Play!

1. In the VCMI launcher, click **Start Game**
2. Choose **New Game** → **Standard** (or any scenario)
3. In the player setup screen, click on your faction icon
4. Scroll through the faction list — **Jurassica** should appear as an option (with the dinosaur-themed castle)
5. Select it and start the game

### What to Expect

- **Placeholder graphics**: The mod currently uses colored shapes with labels instead of real dinosaur art. This is intentional — see `ASSET_GUIDE.md` for how to replace them with AI-generated sprites.
- **All 14 creatures work**: You can recruit, upgrade, and battle with all dinosaurs.
- **Town screen**: A basic placeholder town screen with building slots.
- **No sounds yet**: Sound effects need to be generated separately (see `ASSET_GUIDE.md`).

---

## Troubleshooting

### "Jurassica doesn't appear in the mod list"
- Make sure `mod.json` is directly inside `~/Library/Application Support/vcmi/Mods/jurassica/` (not nested in another subfolder)
- Check that the file is named `mod.json` (not `mod.json.txt`)

### "Game crashes on startup with mod enabled"
- Check the log file for errors:
  ```bash
  open ~/Library/Application\ Support/vcmi/
  ```
  Look for `VCMI_Client_log.txt` — search for "ERROR" or "jurassica"

### "Faction appears but creatures show as blank/missing"
- Verify sprites exist:
  ```bash
  ls ~/Library/Application\ Support/vcmi/Mods/jurassica/Content/sprites/creatures/trex/
  ```
  You should see PNG files like `idle_00.png`, `move_00.png`, etc.

### "macOS blocks VCMI from opening"
- Go to **System Settings → Privacy & Security**
- Scroll down to find the blocked app message
- Click **Open Anyway**
- You may need to do this the first few times you launch

### Regenerating placeholder graphics
If sprites are missing or you need to regenerate them:
```bash
cd /Users/piotr/Desktop/work/jurassica
python3 -m venv .venv
source .venv/bin/activate
pip install Pillow
python3 generate_placeholders.py
python3 generate_animation_jsons.py
```
Then re-copy the mod folder to the VCMI Mods directory.

---

## Quick Reference

| What | Where |
|------|-------|
| VCMI app | `/Applications/VCMI.app` |
| VCMI data folder | `~/Library/Application Support/vcmi/` |
| HoMM3 game data | `~/Library/Application Support/vcmi/Data/` |
| Mods folder | `~/Library/Application Support/vcmi/Mods/` |
| Jurassica mod | `~/Library/Application Support/vcmi/Mods/jurassica/` |
| VCMI log file | `~/Library/Application Support/vcmi/VCMI_Client_log.txt` |
| Jurassica source | `/Users/piotr/Desktop/work/jurassica/` |

---

## Next Steps

Once you've confirmed the mod loads and plays:

1. **Replace placeholder art** — Follow `ASSET_GUIDE.md` to generate real dinosaur sprites with PixelLab
2. **Add sound effects** — Use ElevenLabs to generate dinosaur roars, footsteps, etc.
3. **Generate town music** — Use Udio or Suno for prehistoric ambient music
4. **Balance creature stats** — Play test games and adjust stats in the creature JSON files
5. **Share with the community** — Post on [VCMI Forums](https://forum.vcmi.eu) for feedback
