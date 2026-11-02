---
name: backlog-generator
description: Convierte el PRD y la spec técnica en un backlog ejecutable — tareas de base de datos, backend, frontend, diseño y pruebas con dependencias reales, olas paralelas y estándar de definición completo — y entrega backlog.json más un plan en Excel. Úsala cuando pidan "generar el backlog", "partir los módulos en tareas", "planificar el sprint/proyecto" o "qué se puede hacer en paralelo". La creación en ClickUp la delega a clickup-tasks.
---

# backlog-generator

Tercer paso. Entrada: PRD + spec técnica. Salida:
1. `backlog.json` (valida contra `references/backlog.schema.json`) — es el **contrato de
   entrega** a `clickup-tasks`.
2. `plan.xlsx` generado por `scripts/build_plan.py` — dependencias, olas paralelas y horas.

Lee antes `references/definition-standard.md`: cada tarea sale cumpliéndolo.

## Cómo se parte un módulo

- **Un módulo de la spec que toca N repos se convierte en N tareas `module`**, una por
  repo (p. ej. `Catálogos — backend` y `Catálogos — frontend`). Motivo: dev-flow trabaja
  un módulo en una sola rama y un solo PR, y una rama vive en un solo repo.
- Subtareas de un módulo, en este orden y solo las que apliquen:
  `db` → `backend` (una por contrato o grupo pequeño de contratos) → `frontend`
  (una por pantalla o grupo pequeño) → `tests` (siempre la última).
- El **diseño** no es subtarea: es una tarea `feature` suelta con `area: design` y
  `repo: null`, de la que depende el módulo de frontend. dev-flow no la ejecuta.
- Subtarea > ~8 h → pártela. Subtarea < ~1 h → fúndela con la vecina.
- Si un repo todavía no existe, agrega una tarea suelta de arranque por repo (base del
  proyecto, CI y `install.sh` del flujo) de la que dependen sus primeros módulos.

## Dependencias

- Solo dependencias **reales**: B depende de A si B no se puede terminar sin el
  resultado de A (una tabla, un contrato, un diseño). "Sería mejor hacerlo antes" no es
  dependencia.
- El orden dentro de un módulo es implícito (las subtareas se hacen en orden en la
  misma rama); **no** declares dependencias entre subtareas del mismo módulo.
- Declara en `depends_on` las dependencias hacia **otras** unidades de trabajo
  (otro módulo o una tarea suelta), por su `key`.
- El frontend de un módulo depende del backend del mismo módulo cuando consume sus
  contratos: escribe el contrato en ambas tareas (la de front lo referencia).

## Proceso

1. Lee PRD y spec. Lista las unidades de trabajo (módulos por repo + tareas sueltas)
   en una tabla corta y confirma que no falta ninguna `RF` del MVP.
2. Genera `backlog.json` completo siguiendo el esquema. `key` legibles y estables:
   `M01-BE`, `M01-BE-03`, `D-02`… Incluye `mvp_rf` con todos los `RF`/`RNF` del MVP
   del PRD y marca en `rf` de cada tarea los que cubre: el script falla si alguno
   queda sin tarea.
3. Ejecuta:
   `python3 scripts/build_plan.py backlog.json plan.xlsx`
   El script valida (esquema, ciclos, estándar de definición, repo único, `tests` al
   final) y calcula las olas. Si reporta errores, corrige el JSON y repite hasta que
   salga limpio. Las advertencias se revisan y se explican al usuario si se mantienen.
4. Entrega al usuario: resumen (unidades, horas, nº de olas, camino crítico), el
   `plan.xlsx` y el `backlog.json`.
5. Pregunta: "¿Lo creo en ClickUp?" Con el OK, invoca `clickup-tasks` pasándole el
   `backlog.json` en modo **lote**. Nunca escribas en ClickUp directamente desde esta
   skill.

## Estimaciones
Horas ideales de una persona con IA, por subtarea. Son para ordenar y detectar tareas
demasiado grandes, no un compromiso; dilo en el resumen.
