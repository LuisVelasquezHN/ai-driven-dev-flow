# <Nombre del repo>

<Qué es este repo en 2 líneas y qué parte del producto cubre.>

## Flujo de trabajo
Este repo usa el AI-Driven Development Flow:
- Las tareas vienen de ClickUp. Para trabajar una: skill `dev-flow` con el link o ID.
- Para entregarla: skill `pr-flow`. Es la única que hace push y abre PR (siempre a `dev`).
- Checks locales: `node scripts/flow-checks.mjs` (los mismos que corre el CI del PR).
- La documentación de cada tarea vive en `docs/tasks/CU-<id>.md`.

## Comandos
- Instalar: `npm ci`
- Desarrollo: `npm run dev`
- Checks: `node scripts/flow-checks.mjs`

## Convenciones
- Ramas: `feat|fix|module/CU-<id>-<slug>` desde `dev`.
- Commits: Conventional Commits con el ID: `feat(CU-<id>): fase 1 — …`.
- <Convenciones propias del repo: estructura de carpetas, manejo de errores, etc.>
