# Customization Guide

Your profile is live with **dummy/placeholder data**. When you have your real info, update these files and ask me to regenerate — or edit manually.

---

## Quick checklist

| What to change | Where |
|----------------|-------|
| Name, role, tagline, about, skills | `generate_profile.py` → `PROFILE` dict, then run `python3 generate_profile.py` |
| Stats numbers (stars, commits, etc.) | `generate_profile.py` → `PROFILE["stats"]` |
| Language percentages | `generate_profile.py` → `PROFILE["langs"]` |
| Trophy grades | `generate_profile.py` → `PROFILE["trophies"]` |
| Projects table | `generate_profile.py` → `PROFILE["projects"]` |
| Social links | `generate_profile.py` → `PROFILE["social"]` |
| Email | `generate_profile.py` → `PROFILE["email"]` |
| Character image | Replace `character-placeholder.png`, re-run avatar export (see below) |
| Cache bust after edits | Bump `PROFILE["cache_v"]` from `"1"` to `"2"`, etc. |

---

## Step 1 — Replace character image

1. Generate an anime-style image (white background) using the prompt in the PDF guide.
2. Save it as `character-placeholder.png` in this folder.
3. Run:
   ```bash
   python3 -c "
   import base64
   from pathlib import Path
   b64 = base64.b64encode(Path('character-placeholder.png').read_bytes()).decode()
   Path('avatar.b64.txt').write_text(b64)
   "
   python3 generate_profile.py
   ```

---

## Step 2 — Update profile text

Open `generate_profile.py` and edit the `PROFILE` dictionary at the top:

```python
PROFILE = {
    "name": "Your Name",
    "full_name": "Your Full Name",
    "role": "AI Native Engineer",
    "roles_cycle": ["AI Native Engineer", "Full Stack Developer"],
    "username": "ayyappa3232",
    "email": "you@email.com",
    ...
}
```

Then regenerate:
```bash
python3 generate_profile.py
```

---

## Step 3 — Create the GitHub profile repo

1. Go to https://github.com/new
2. Repository name: **`ayyappa3232`** (must match username exactly)
3. Public, tick **Add a README file**
4. Upload all generated files to the repo root:
   - `banner.svg`, `banner-light.svg`, `lanyard.svg`
   - `stats.svg`, `langs.svg`, `trophies.svg`
   - `README.md`
   - `.github/workflows/github-snake.yml`

---

## Step 4 — Activate the snake

1. Open repo → **Actions** tab → enable workflows
2. Run **Generate Snake** workflow manually
3. Snake appears on profile after ~1 minute

---

## Step 5 — Cache trick

GitHub caches README images. If you edit an SVG and nothing changes:

1. Bump `?v=1` to `?v=2` in `README.md` for that image
2. Commit SVG first, then README with bumped version

---

## Files in this package

| File | Purpose |
|------|---------|
| `banner.svg` | Dark mode animated hero banner |
| `banner-light.svg` | Light mode banner (auto-switches) |
| `lanyard.svg` | Swinging ID badge |
| `stats.svg` | Local GitHub stats card |
| `langs.svg` | Top languages bars |
| `trophies.svg` | Trophy grid |
| `README.md` | Profile README (paste into repo) |
| `.github/workflows/github-snake.yml` | Daily snake generator |
| `generate_profile.py` | Regenerator script — edit PROFILE dict and re-run |
| `character-placeholder.png` | Your character art (replace later) |
| `avatar.b64.txt` | Base64 of character (auto-generated) |

---

## When ready for a full update

Send me:
- Your anime character image
- Real name, email, LinkedIn, portfolio URL
- Updated skills, tagline, about me
- Real stats (or I can pull from GitHub API)
- Projects you want featured

Say **"update my profile"** and I will regenerate everything with your real data.
