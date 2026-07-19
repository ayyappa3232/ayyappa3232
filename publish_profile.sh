#!/bin/bash
# Publish profile and bust GitHub/jsDelivr cache (two-commit flow).
set -e
cd "$(dirname "$0")"
USER="ayyappa3232"
REPO="$USER/$USER"

echo "==> Generating SVG assets..."
python3 generate_profile.py

echo "==> Commit 1: SVG files..."
git add banner.svg banner-light.svg lanyard.svg stats.svg langs.svg learning.svg trophies.svg generate_profile.py publish_profile.sh .github/workflows/github-snake.yml
git diff --staged --quiet && echo "No SVG changes to commit." || git commit -m "Update profile SVG assets"

echo "==> Pushing SVG commit..."
git push origin main

SHA=$(git rev-parse HEAD)
echo "==> Pinning README to commit ${SHA:0:12}..."

python3 -c "
from generate_profile import readme_md, ROOT
ROOT.joinpath('README.md').write_text(readme_md(sha='$SHA'))
print('README pinned to', '$SHA'[:12])
"

echo "==> Commit 2: README with SHA-pinned CDN URLs..."
git add README.md
git commit -m "Pin README images to commit ${SHA:0:12} (cache bust)"
git push origin main

echo "==> Purging jsDelivr cache..."
for f in banner.svg banner-light.svg lanyard.svg stats.svg langs.svg learning.svg trophies.svg; do
  curl -s "https://purge.jsdelivr.net/gh/$REPO@main/$f" >/dev/null || true
  curl -s "https://purge.jsdelivr.net/gh/$REPO@$SHA/$f" >/dev/null || true
done

echo ""
echo "Done! Profile should update in 1–3 minutes."
echo "Preview: https://cdn.jsdelivr.net/gh/$REPO@$SHA/banner.svg"
echo "Profile: https://github.com/$USER (open in Incognito + Cmd+Shift+R)"
