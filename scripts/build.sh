#!/usr/bin/env bash
# Ensambla las skills en dist/skills/<nombre>/ copiando las referencias compartidas
# (cada skill debe ser autocontenida: en Claude Chat se suben por separado) y empaqueta
# las cuatro skills de Chat como .zip listos para subir en claude.ai → Settings → Skills.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
CHAT_SKILLS=(prd-generator techlead-spec backlog-generator clickup-tasks)
ALL_SKILLS=(prd-generator techlead-spec backlog-generator clickup-tasks dev-flow pr-flow)

rm -rf "$DIST"
mkdir -p "$DIST/skills"

# Solo estas usan el estándar de definición y las convenciones de ClickUp;
# prd-generator y techlead-spec se quedan a nivel producto/spec, sin ese ruido.
NEEDS_SHARED=(backlog-generator clickup-tasks dev-flow pr-flow)

for s in "${ALL_SKILLS[@]}"; do
  cp -R "$ROOT/skills/$s" "$DIST/skills/$s"
  if [[ " ${NEEDS_SHARED[*]} " == *" $s "* ]]; then
    mkdir -p "$DIST/skills/$s/references"
    cp "$ROOT/shared/"*.md "$DIST/skills/$s/references/"
  fi
  # Carpetas vacías fuera: no aportan nada al subir la skill
  find "$DIST/skills/$s" -type d -empty -delete
done

# clickup-tasks valida el backlog.json con el mismo esquema que lo produce
cp "$ROOT/skills/backlog-generator/references/backlog.schema.json" \
   "$DIST/skills/clickup-tasks/references/"

for s in "${CHAT_SKILLS[@]}"; do
  (cd "$DIST/skills" && zip -qr "$DIST/$s.zip" "$s" -x '*.DS_Store' '*__pycache__*')
done

echo "Skills ensambladas en $DIST/skills"
echo "Zips para Claude Chat:"
for s in "${CHAT_SKILLS[@]}"; do echo "  dist/$s.zip"; done
