---
name: pr-flow
description: Entrega una tarea implementada por dev-flow — verifica repo y árbol limpio, actualiza la rama con dev (si hay conflicto se detiene), hace el único push del ciclo, abre el PR a dev con el ID de la tarea en el título, mueve la tarea a PR Review y registra tiempo, rebotes y costo de IA en ClickUp, y devuelve al dev a la rama dev. Úsala cuando digan "entrega la tarea", "abre el PR", "pr-flow" o al terminar dev-flow.
---

# pr-flow

Entrada: tarea implementada y documentada por dev-flow (rama local con commits).
Salida: PR abierto contra `dev` + tarea en `PR REVIEW` con métricas al día.

Lee `references/clickup-conventions.md`. Config en `.claude/flow.config.json`.

## 1. Verificaciones (si una falla: para, explica, no sigas)

1. Tarea: el `CU-<id>` sale de la rama actual (`git branch --show-current`) o del
   argumento. Lee la tarea y el estado local `.flow/CU-<id>.json`.
2. **Repo correcto**: `origin` == `repo` del config == campo `Repo` de la tarea.
3. **Nada sin commitear**: `git status --porcelain` vacío (incluye archivos sin
   seguimiento; `.flow/` está en `.gitignore`).
4. La rama no es `dev` ni `main`; tiene commits por delante de `origin/dev`.
5. Todas las fases del estado local están `done` y existe `docs/tasks/CU-<id>.md`
   (si no, la tarea no pasó por el cierre de dev-flow: dilo).
6. `gh auth status` correcto.

## 2. Actualizar con dev

```
git fetch origin
git merge --no-edit origin/<baseBranch>
```
Merge, no rebase: la rama puede haberse publicado antes (rebotes) y así nunca hace
falta `push --force`.
**Si hay conflicto**: no lo resuelvas. Deja el merge en curso, lista los archivos en
conflicto y dile al dev que lo resuelva, haga el commit del merge y vuelva a ejecutar
`pr-flow`. Termina aquí.

Si el merge trajo cambios, vuelve a correr `node scripts/flow-checks.mjs`; rojo = para.

## 3. Push y PR

1. `git push -u origin <rama>` — el **único** push del ciclo.
2. ¿Hay PR abierto para la rama? (`gh pr list --head <rama> --state open --json url`)
   - Sí (rebote de PR): no abras otro; comenta en el PR qué cambió en este rebote.
   - No: `gh pr create --base <baseBranch> --head <rama> --title "[CU-<id>] <título de la tarea>" --body-file <archivo>`
     con el cuerpo desde `templates/pr-body.md` (link a ClickUp, resumen, criterios
     cubiertos, link al doc, checks ejecutados, cómo probar).

## 4. ClickUp

1. Detén el timer de la tarea.
2. Costo de IA de la rama:
   `node <dir de esta skill>/scripts/ai-cost.mjs --branch <rama> --json`
   Suma todas las sesiones de Claude Code de este repo (incluidos worktrees y
   subagentes) en esa rama. Es acumulado: **sobrescribe** `Costo IA (USD)`.
3. Si el estado local tiene `rework` = `pr` o `qa`, incrementa `Rebotes PR` o
   `Rebotes QA` en 1 y limpia `rework`.
4. Campos `PR` y `Documentación` (link al archivo en la rama).
5. Estado → `PR REVIEW`. En módulos: el padre y las subtareas.
6. Comentario: link al PR, tiempo de esta vuelta, costo IA total, rebotes.
7. Añade la entrega a `delivered` en el estado local.

Si un paso de ClickUp falla, el PR ya está abierto: no lo deshagas. Informa qué quedó
pendiente en ClickUp para hacerlo a mano o reintentar.

## 5. Cierre

`git switch <baseBranch> && git pull --ff-only` y resume: PR, estado, tiempo, costo,
rebotes. Recuerda que lo siguiente es la revisión humana.
