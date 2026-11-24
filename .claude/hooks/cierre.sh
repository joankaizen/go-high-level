#!/bin/bash
# Al terminar cada respuesta: si quedan cambios sin guardar en GitHub, Claude los guarda antes de parar.
input=$(cat)
echo "$input" | grep -q '"stop_hook_active": *true' && exit 0

cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

pendiente=""
[ -n "$(git status --porcelain)" ] && pendiente="hay cambios sin commit"
if [ -z "$pendiente" ] && git rev-parse '@{u}' >/dev/null 2>&1; then
  [ -n "$(git log '@{u}..HEAD' --oneline)" ] && pendiente="hay commits sin push"
fi

if [ -n "$pendiente" ]; then
  echo "{\"decision\":\"block\",\"reason\":\"Antes de terminar: $pendiente. Si el trabajo cambió algo importante, actualiza ESTADO.md según la regla de CLAUDE.md. Luego haz commit y push.\"}"
fi
exit 0
