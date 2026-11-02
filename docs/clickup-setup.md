# Configuración de ClickUp

Una sola vez por Space. Las convenciones completas están en
[`shared/clickup-conventions.md`](../shared/clickup-conventions.md).

## 1. Estados de la lista
Crea estos estados, en este orden:
`BACKLOG` · `TO DO` · `IN PROGRESS` · `PR REVIEW` · `DEV` · `QA (STAGING)` ·
`TO DEPLOY` · `PRODUCTION` · `DONE` (cerrado).

## 2. Campos personalizados
| Nombre exacto | Tipo |
|---|---|
| Tipo | Dropdown: `bug`, `feature`, `module` |
| Repo | Texto corto |
| Rama | Texto corto |
| PR | URL |
| Documentación | URL |
| Rebotes PR | Número (por defecto 0) |
| Rebotes QA | Número (por defecto 0) |
| Costo IA (USD) | Moneda USD |

Activa **Time tracking** y **Dependencies** (ClickApps).

## 3. Integración con GitHub
ClickApps → GitHub → conecta los repos. Desde ese momento las ramas, commits y PRs que
llevan `CU-<id>` aparecen dentro de la tarea.

## 4. MCP de ClickUp
- **Claude Chat** (clickup-tasks): Settings → Connectors → ClickUp.
- **Claude Code** (dev-flow, pr-flow):
  ```bash
  claude mcp add --transport http clickup https://mcp.clickup.com/mcp
  ```
  y autentica con `/mcp` la primera vez.

Las skills se detienen y lo dicen si no encuentran el MCP, la lista, un estado o un campo.
No crean nada a medias.

## 5. Acuerdo de equipo (lo único manual)
Quien devuelve una tarea a `IN PROGRESS` (reviewer o QA) le pone el tag `rebote:pr` o
`rebote:qa` y deja un comentario con el motivo.
