#!/bin/sh
# Links ~/.claude/skills to this repo's skills/ folder, so Claude Code on this
# machine uses (and edits) the skills in git. An existing folder is kept as a backup.
set -e

repo="$(cd "$(dirname "$0")/.." && pwd)"
target="$HOME/.claude/skills"

mkdir -p "$HOME/.claude"

if [ -L "$target" ]; then
  rm "$target"
elif [ -e "$target" ]; then
  backup="$target.bak-$(date +%Y%m%d-%H%M%S)"
  mv "$target" "$backup"
  echo "old skills kept in $backup"
fi

ln -s "$repo/skills" "$target"
echo "linked $target -> $repo/skills"
