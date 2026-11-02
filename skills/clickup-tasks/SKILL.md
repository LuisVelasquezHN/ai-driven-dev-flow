---
name: clickup-tasks
description: Crea tareas en ClickUp completamente definidas (bug, feature o módulo con subtareas encadenadas), validadas contra el estándar de definición y con vista previa y confirmación antes de escribir. Úsala cuando pidan "crea la tarea en ClickUp", "sube este bug", "carga el backlog a ClickUp", o cuando backlog-generator entregue un backlog.json. Requiere el MCP de ClickUp.
---

# clickup-tasks

Cuarto paso, y la **única** skill que crea tareas en ClickUp. Objetivo: quien ejecute
la tarea nunca tiene que adivinar.

Lee antes `references/definition-standard.md` y `references/clickup-conventions.md`.

## Modos de entrada

- **Individual** — un requerimiento suelto descrito en la conversación (un bug que
  reporta alguien, una feature planificada).
- **Lote** — un `backlog.json` entregado por backlog-generator (esquema en
  `references/backlog.schema.json`). Ya viene clasificado y
  completo; igual se valida.

## Proceso

1. **Prerrequisito.** Comprueba que hay herramientas del MCP de ClickUp disponibles y
   localiza la lista destino (pregunta el nombre de la lista si no está en la
   conversación; búscala, no inventes IDs). Comprueba que la lista tiene los estados y
   campos de las convenciones; si falta alguno, dilo y para — no crees tareas a medias.
2. **Clasifica** cada tarea: `bug`, `feature` o `module`. En modo individual, si no es
   obvio, elige y explica en una línea por qué.
3. **Completa con la plantilla del tipo** (`templates/bug.md`, `feature.md`,
   `module.md`). En modo individual, lo que no esté en la conversación y sea
   obligatorio se pregunta en **una sola** ronda; nunca se rellena con suposiciones
   silenciosas.
4. **Valida** cada tarea contra el estándar: criterios (≥ 2), fuera de alcance (≥ 1),
   pruebas, **un solo repo**. Si una tarea toca dos repos, propón partirla en dos y
   no sigas hasta que se acepte.
5. **Vista previa.** Muestra una tabla con: key/título, tipo, repo, tags, depende de,
   padre. Para lote, además el conteo por tipo. Para individual, el cuerpo completo.
   Pregunta: "¿Creo estas N tareas en `<lista>`?" y **espera un sí explícito**.
6. **Crea**, en este orden para que las referencias existan:
   1. Tareas sueltas y padres `module` (estado `BACKLOG`).
   2. Subtareas de cada módulo, en su orden, como subtareas del padre, con la
      dependencia "espera a" la subtarea anterior (encadenadas en orden de desarrollo).
   3. Dependencias entre unidades (`depends_on` del backlog) como "espera a" en ClickUp.
   Por cada tarea: descripción desde la plantilla, campos `Tipo` y `Repo`, tags de
   área y `mod:<slug>`. Guarda el mapa `key → ID de ClickUp` a medida que creas.
7. **Si algo falla a mitad**, para, muestra qué se creó (con links) y qué no, y
   ofrece reintentar solo lo pendiente. Nunca dupliques: antes de reintentar busca en
   la lista por título.
8. **Entrega** la tabla final `key → CU-<id> → link`. En modo lote, devuélvela también
   como JSON para que el tech lead la guarde junto al backlog.

## Lo que esta skill no hace
- No mueve tareas a `TO DO` (eso es del tech lead).
- No asigna personas ni fechas, salvo que el usuario lo pida explícitamente.
