#!/usr/bin/env bash
#
# Install MTG set design skills into a project directory.
#
# Usage:
#   ./install.sh /path/to/your/project
#
# Creates .claude/skills/ in the target directory (if it doesn't exist)
# and symlinks every skill from this repo into it. Claude Code will
# automatically discover the skills when working in that project.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

SKILLS=(
  mtg-exploratory-designer
  mtg-worldbuilder
  mtg-ip-researcher
  mtg-vision-designer
  mtg-set-designer
  mtg-color-pie-reviewer
  mtg-play-designer
  mtg-editor
  mtg-creative-writer
  mtg-art-director
  mtg-product-architect
  mtg-set-pipeline
)

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <target-project-directory>"
  exit 1
fi

TARGET="$1"

if [[ ! -d "$TARGET" ]]; then
  echo "Error: $TARGET is not a directory"
  exit 1
fi

SKILLS_DIR="$TARGET/.claude/skills"
mkdir -p "$SKILLS_DIR"

for skill in "${SKILLS[@]}"; do
  src="$SCRIPT_DIR/$skill"
  dest="$SKILLS_DIR/$skill"

  if [[ ! -d "$src" ]]; then
    echo "Warning: $src not found, skipping"
    continue
  fi

  if [[ -e "$dest" ]]; then
    echo "  exists: $skill"
  else
    ln -s "$src" "$dest"
    echo "  linked: $skill"
  fi
done

echo ""
echo "Installed ${#SKILLS[@]} skills into $SKILLS_DIR"
echo "Start Claude Code in $TARGET to use them."
