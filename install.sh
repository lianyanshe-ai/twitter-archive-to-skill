#!/bin/bash
# Installer script for twitter-archive-to-skill

set -e

SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$SKILLS_DIR"

echo "Installing twitter-archive-to-skill..."
echo "Target directory: $SKILLS_DIR"
echo ""

# Copy all skills
cp -r "skills/twitter-archive-to-kb" "$SKILLS_DIR/"
cp -r "skills/twitter-archive-to-skill" "$SKILLS_DIR/"
cp -r "skills/huashu-nuwa" "$SKILLS_DIR/"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Installed skills:"
echo "  - huashu-nuwa (女娲造人)"
echo "  - twitter-archive-to-kb"
echo "  - twitter-archive-to-skill"
echo ""
echo "Usage:"
echo "  1. Export your Twitter data from Twitter Settings"
echo "  2. Unzip to get a data/ directory"
echo "  3. In Claude Code: /skill twitter-archive-to-skill"
echo ""
