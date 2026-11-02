---
name: dev-flow
description: Planifica e implementa de punta a punta una tarea de ClickUp dentro del repo — plan con OK del dev, rama, estado In Progress, timer, implementación por fases con checks en verde y commit por fase, y documentación del porqué al cerrar. No hace push ni abre el PR (eso es pr-flow). Úsala cuando el dev pase un link o ID de ClickUp, o diga "empecemos la tarea CU-…", "implementa esta tarea", "retomo la tarea que rebotó".
---

# dev-flow

Entrada: link o ID de una tarea de ClickUp. Salida: rama local con un commit por fase
+ documentación, **sin push**. Corre en Claude Code, dentro del repo.

Lee `references/clickup-conventions.md` y `references/definition-standard.md`.
La configuración del repo está en `.claude/flow.config.json` (ver
`references/flow.config.example.json`).

## Reglas que no se rompen

1. **Cero código sin el OK explícito del dev al plan.** Leer e investigar sí; editar no.
2. **Una fase no se commitea sin checks en verde y sin el OK del dev a esa fase.**
3. **Nunca `git push`**, nunca abrir PR, nunca tocar `dev`/`main` directamente.
4. **Un repo por ejecución.** Si la tarea es de otro repo, para y dilo.
5. Si la tarea no cumple el estándar de definición, **no adivines**: comenta en
   ClickUp qué falta, díselo al dev y para.

## 0. Preparación

1. Lee `.claude/flow.config.json`. Si no existe, para y sugiere ejecutar el instalador.
2. Obtén la tarea con el MCP de ClickUp: descripción, campos, tags, estado,
   dependencias, padre y subtareas, comentarios.
3. Verifica, y si algo falla para y explícalo:
   - `Repo` de la tarea == `repo` del config == `origin` (`git remote get-url origin`).
   - Árbol limpio (`git status --porcelain` vacío).
   - Dependencias ("espera a") en `DEV` o posterior.
   - Estado `TO DO` (tarea nueva) o `IN PROGRESS` (rebote; ver §5).
   - Tipo distinto de diseño (`repo` vacío → no es ejecutable aquí).
4. Crea/lee el estado local `.flow/CU-<id>.json` (gitignored; esquema en
   `references/state.example.json`). Es la memoria entre sesiones de esta máquina;
   ClickUp es la memoria compartida.

## 1. Plan

Según el `Tipo`:

- **feature** — explora el código relevante y propone fases.
- **bug** — primero **causa raíz**: reproduce (idealmente escribe la prueba de
  regresión y comprueba que falla), localiza el origen y muestra la evidencia
  (archivo:línea). Luego propone el fix. Si la causa está **en otro repo**: comenta en
  ClickUp la evidencia y el repo responsable, díselo al dev y **termina sin rama ni
  PR**. Un bug lleva exactamente una prueba de regresión.
- **module** — lee el padre y sus subtareas en orden. Una fase por subtarea (o más si
  una es grande). Las pruebas del módulo son la última fase.

El plan que presentas tiene: resumen de la tarea en 2 líneas, archivos que tocarás,
fases (cada una con objetivo, archivos y cómo se verifica), riesgos y preguntas.
Cada criterio de aceptación queda asignado a una fase. Publica el plan como comentario
en ClickUp **después** de que el dev lo apruebe.

Espera el OK. Cambios al plan → nueva versión y nuevo OK.

## 2. Arranque (con el plan aprobado)

1. `git fetch origin && git switch <baseBranch> && git pull --ff-only`
2. Rama: `<prefijo>/CU-<id>-<slug-del-título>`; prefijo `feat` | `fix` | `module`.
   Slug: minúsculas, ASCII, guiones, ≤ 40 caracteres.
3. Mueve la tarea a `IN PROGRESS`, rellena `Rama` e inicia el timer de ClickUp.
   En módulos: el padre y la primera subtarea.
4. Guarda en el estado: rama, plan, fases, hora de inicio.

## 3. Implementación por fases

Por cada fase:
1. Implementa solo lo de la fase.
2. Ejecuta `node scripts/flow-checks.mjs` (corre los checks del config: lint, tipos,
   tests, build). Repite hasta verde. Si no logras verde tras 3 intentos razonables,
   para y explica qué falla.
3. Presenta al dev: qué cambió (archivos), salida resumida de los checks, criterios de
   aceptación que quedaron cubiertos. Pide OK.
4. Con el OK: commit de la fase.
   `<tipo>(CU-<id>): fase <n> — <qué>` (Conventional Commits; `tipo` = feat, fix, test,
   refactor, docs). En módulos, el commit menciona además el `CU-<id>` de la subtarea y
   la subtarea pasa a `IN PROGRESS` al empezar su fase.
5. Actualiza el estado local (fase hecha + hash del commit).

## 4. Cierre: documentación

Lo que el código no explica por sí solo. Escribe `docs/tasks/CU-<id>.md` con
`templates/task-doc.md`: el porqué, reglas de negocio, casos borde, decisiones y
alternativas descartadas, cómo probarlo a mano. Si la tarea introduce una convención
o un comando que cualquier dev debe conocer, actualiza también `CLAUDE.md`.
Commit: `docs(CU-<id>): documentación de la tarea`.

Termina con un resumen: rama, commits, criterios cubiertos y
"Listo para `pr-flow`". **No hagas push.**

## 5. Rebotes (la tarea vuelve a IN PROGRESS)

Se detecta porque la tarea ya tiene `PR` registrado.
1. Tipo de rebote: tag `rebote:pr` o `rebote:qa`. Si no hay tag, pregunta una vez.
   Guárdalo en el estado (`rework`) y quita el tag en ClickUp.
2. Lee los comentarios nuevos del reviewer/QA: son el insumo del plan.
3. Reutiliza la rama de `Rama`: `git switch <rama> && git merge origin/<baseBranch>`.
4. Mismo ciclo: plan (solo lo del rebote) → OK → fases → actualiza el doc de la tarea.
   Reinicia el timer.
