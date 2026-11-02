#!/usr/bin/env bash
# Instala el flujo en un repo de proyecto:
#   - skills dev-flow y pr-flow en <repo>/.claude/skills/ (versionadas con el repo)
#   - .claude/flow.config.json, scripts/flow-checks.mjs, CLAUDE.md, CI del PR y
#     plantilla de PR — solo si no existen (nunca sobrescribe)
#   - .flow/ en .gitignore y docs/tasks/
#
# Uso: scripts/install.sh <ruta-al-repo>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:?Uso: scripts/install.sh <ruta-al-repo>}"
TARGET="$(cd "$TARGET" && pwd)"

git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || { echo "$TARGET no es un repo git"; exit 1; }

"$ROOT/scripts/build.sh" >/dev/null

copy_if_missing() {
  local src="$1" dst="$2"
  if [[ -e "$dst" ]]; then
    echo "  = $dst (ya existe, no se toca)"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo "  + $dst"
  fi
}

echo "Skills de Claude Code:"
mkdir -p "$TARGET/.claude/skills"
for s in dev-flow pr-flow; do
  rm -rf "$TARGET/.claude/skills/$s"
  cp -R "$ROOT/dist/skills/$s" "$TARGET/.claude/skills/$s"
  echo "  + .claude/skills/$s"
done

echo "Plantillas del repo:"
copy_if_missing "$ROOT/templates/repo/CLAUDE.md" "$TARGET/CLAUDE.md"
copy_if_missing "$ROOT/templates/repo/scripts/flow-checks.mjs" "$TARGET/scripts/flow-checks.mjs"
copy_if_missing "$ROOT/templates/repo/.github/workflows/pr-control.yml" "$TARGET/.github/workflows/pr-control.yml"
copy_if_missing "$ROOT/templates/repo/.github/pull_request_template.md" "$TARGET/.github/pull_request_template.md"

CONFIG="$TARGET/.claude/flow.config.json"
if [[ -e "$CONFIG" ]]; then
  echo "  = .claude/flow.config.json (ya existe, no se toca)"
else
  # owner/name desde origin (https o ssh); si no hay origin, queda el del ejemplo
  ORIGIN="$(git -C "$TARGET" remote get-url origin 2>/dev/null || true)"
  REPO="$(sed -E 's#(\.git)?$##; s#^.*github\.com[:/]##' <<<"$ORIGIN")"
  if [[ -n "$REPO" ]]; then
    sed "s#\"mi-org/mi-backend\"#\"$REPO\"#" \
      "$ROOT/skills/dev-flow/references/flow.config.example.json" > "$CONFIG"
  else
    cp "$ROOT/skills/dev-flow/references/flow.config.example.json" "$CONFIG"
  fi
  echo "  + .claude/flow.config.json (revisa repo, lista de ClickUp y checks)"
fi

mkdir -p "$TARGET/docs/tasks"
touch "$TARGET/docs/tasks/.gitkeep"
if ! grep -qx '.flow/' "$TARGET/.gitignore" 2>/dev/null; then
  echo '.flow/' >> "$TARGET/.gitignore"
  echo "  + .flow/ en .gitignore"
fi

cat <<EOF

Listo. Pendiente a mano:
  1. Ajusta .claude/flow.config.json (checks reales del repo y lista de ClickUp).
  2. Conecta el MCP de ClickUp en Claude Code (ver docs/clickup-setup.md).
  3. Crea la rama 'dev' si no existe y protégela (PR obligatorio + checks de PR control).
EOF
