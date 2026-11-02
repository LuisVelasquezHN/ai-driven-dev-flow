# Convenciones de ClickUp

Lo que las skills asumen del Space de ClickUp. La configuración paso a paso está en
`docs/clickup-setup.md`.

## Estados (en este orden)

| Estado | Lo mueve | Cuándo |
|---|---|---|
| `BACKLOG` | clickup-tasks | Al crear la tarea |
| `TO DO` | Tech lead | Entra al sprint, tarea completa |
| `IN PROGRESS` | dev-flow | Plan aprobado y rama creada |
| `PR REVIEW` | pr-flow | PR abierto |
| `DEV` | Reviewer | Merge a `dev` |
| `QA (STAGING)` | Lead | Deploy semanal a staging |
| `TO DEPLOY` → `PRODUCTION` → `DONE` | Lead / QA | Release aprobado |

**Las skills solo mueven tres estados**: `BACKLOG`, `IN PROGRESS` y `PR REVIEW`.
Todo lo demás es decisión humana. Si una skill encuentra la tarea en un estado
inesperado, se detiene y lo dice; nunca "corrige" el estado por su cuenta.

## Campos personalizados

| Campo | Tipo | Escribe | Uso |
|---|---|---|---|
| `Tipo` | Dropdown: bug / feature / module | clickup-tasks | Elige plantilla y camino de dev-flow |
| `Repo` | Texto (`owner/name`) | clickup-tasks | pr-flow verifica que coincide con `origin` |
| `Rama` | Texto | dev-flow | Trazabilidad tarea ↔ rama |
| `PR` | URL | pr-flow | Trazabilidad tarea ↔ PR |
| `Documentación` | URL | pr-flow | Link al doc de la tarea en el repo |
| `Rebotes PR` | Número | pr-flow | +1 cada vez que el reviewer la devuelve |
| `Rebotes QA` | Número | pr-flow | +1 cada vez que QA la devuelve |
| `Costo IA (USD)` | Moneda | pr-flow | Total acumulado de la rama (se sobrescribe, no se suma) |

El **tiempo de desarrollo** usa el time tracking nativo de ClickUp: dev-flow inicia el
timer, pr-flow lo detiene.

## Rebotes

Quien devuelve una tarea a `IN PROGRESS` le pone el tag `rebote:pr` o `rebote:qa`.
dev-flow lo detecta al empezar, lo guarda en el estado local y **quita el tag**;
pr-flow incrementa el contador correspondiente al entregar. Si la tarea vuelve con PR
ya registrado pero sin tag, dev-flow pregunta una sola vez de qué tipo es el rebote.

## Tags

- Área: `db`, `backend`, `frontend`, `design`, `tests`
- Módulo: `mod:<slug>` (p. ej. `mod:catalogo-productos`)
- Rebote: `rebote:pr`, `rebote:qa` (transitorios)

## Identificador

Se usa el ID corto de ClickUp con prefijo `CU-` (p. ej. `CU-86b3k2x1`). Va en la rama,
en los commits y en el título del PR: así la integración GitHub ↔ ClickUp enlaza todo
sola.
