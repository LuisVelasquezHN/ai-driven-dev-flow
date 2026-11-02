# Registro de decisiones

La consigna fue: *"No hay ronda de preguntas. Toda decisión queda en tus manos: tómala,
anótala y explícanos tu porqué."* Este archivo es eso. Cada decisión tiene el contexto,
lo que decidí, el porqué y lo que descarté. Están en el orden en que las tomé.

---

## D-00 · Qué entregar

**Contexto.** El documento describe un flujo (6 skills, 3 momentos, estados de
ClickUp, controles del PR) pero no dice explícitamente qué construir.
**Decisión.** Implementar el flujo tal como está descrito: las seis skills funcionales,
lo que necesitan para correr en un repo real (configuración, CI del PR, plantillas,
instalador) y un ejemplo para probarlo de punta a punta.
**Porqué.** Es la lectura que más se puede verificar: cada lámina se convierte en
algo que se puede ejecutar y revisar. Diseñar un flujo distinto, o solo opinar sobre
este, demostraría menos.
**Descartado.** Una app de ejemplo construida con el flujo (depende de que exista el
flujo; queda como demo, ver README §Demo). Un ensayo crítico sin código.

## D-01 · Formato: Agent Skills estándar (`SKILL.md`)

**Decisión.** Cada skill es una carpeta con `SKILL.md` (frontmatter `name` +
`description`), y aparte `templates/`, `references/` y `scripts/`.
**Porqué.** Es el mismo formato en Claude Chat (subida como .zip) y en Claude Code
(`.claude/skills/`). Una sola fuente para los dos entornos que pide el documento.
La `description` es lo que decide cuándo se activa la skill, así que lleva frases
reales de activación ("abre el PR", "carga el backlog a ClickUp").

## D-02 · Idioma: español

**Decisión.** Skills, plantillas y documentación en español; identificadores técnicos
(estados de ClickUp, nombres de skill, Conventional Commits) en inglés como en el
documento.
**Porqué.** El equipo y sus clientes trabajan en español; las tareas, los PRD y la
documentación que generan las skills los leen personas en español. Los modelos actuales
siguen instrucciones en español igual de bien.

## D-03 · Las referencias compartidas tienen una sola fuente

**Contexto.** Tres skills necesitan el estándar de definición y las convenciones de
ClickUp. En Claude Chat cada skill se sube por separado y tiene que ser autocontenida.
**Decisión.** Fuente única en `shared/`; `scripts/build.sh` las copia a cada skill en
`dist/`.
**Porqué.** Si el estándar cambia, cambia en un lugar. Copiar a mano en tres carpetas
termina en tres versiones distintas.
**Descartado.** Symlinks (no sobreviven al .zip de Claude Chat).

## D-04 · Contrato explícito entre backlog-generator y clickup-tasks: `backlog.json`

**Decisión.** backlog-generator produce un JSON con esquema
(`backlog.schema.json`) y clickup-tasks lo consume. El Excel se genera **desde** ese
JSON con un script, no a mano.
**Porqué.** "Cada skill entrega el resultado a la siguiente": si la entrega es prosa,
la siguiente tiene que interpretarla y aparecen diferencias. Con un esquema, la entrega
se valida. Y el Excel nunca contradice al backlog porque sale del mismo archivo.

## D-05 · La validación del backlog es código, no instrucciones

**Decisión.** `build_plan.py` valida el estándar de definición (criterios ≥ 2, fuera de
alcance, pruebas, repo único, pruebas al final del módulo, bug con una sola prueba de
regresión), comprueba que cada requerimiento del MVP tenga al menos una tarea (`mvp_rf`),
detecta ciclos y calcula olas paralelas y camino crítico. La verificación de cobertura se
agregó después de que la demo dejara RNF-01 sin tarea (ver `examples/demo`).
**Porqué.** Las reglas que se pueden comprobar no se le dejan al modelo. Que el script
falle hace que el error se corrija antes de llegar a ClickUp. Las olas y el camino
crítico son cálculos de grafo: en código salen siempre igual.

## D-06 · Unidad de paralelismo: el módulo por repo, no la subtarea

**Contexto.** El documento dice que un módulo es una rama y un PR, con las subtareas
hechas en orden, y que una tarea ejecutable toca un solo repo.
**Decisión.** Un módulo de la spec que toca back y front se convierte en **dos tareas
`module`** (una por repo), y el frontend depende del backend. Las olas paralelas se
calculan entre estas unidades, no entre subtareas.
**Porqué.** Es la única forma de cumplir las dos reglas a la vez (una rama vive en un
repo). Y dentro de un módulo no hay paralelismo real: es una rama secuencial, así que
contarlo como paralelo daría un plan engañoso.

## D-07 · El diseño es una tarea suelta y no ejecutable

**Decisión.** Las tareas de diseño van con `repo: null`, fuera de los módulos, y el
módulo de frontend depende de ellas. dev-flow no las ejecuta.
**Porqué.** Si el diseño fuera una subtarea dentro de la rama del módulo, bloquearía a
dev-flow en una fase que no es código. Como dependencia, el tech lead ve en el plan
cuándo tiene que estar listo.

## D-08 · Estado local de la tarea en `.flow/CU-<id>.json`

**Decisión.** dev-flow guarda el plan, las fases, los commits y el tipo de rebote en un
archivo local ignorado por git. pr-flow lo lee.
**Porqué.** dev-flow y pr-flow corren en sesiones distintas, a veces con días de
diferencia. ClickUp es la memoria compartida entre personas y repos (como dice el
documento), pero "qué fases están commiteadas en esta rama" es un dato de esta máquina,
y pr-flow lo necesita para comprobar que el trabajo está cerrado antes de publicarlo.

## D-09 · Configuración por repo en `.claude/flow.config.json`

**Decisión.** Repo esperado, rama base, carpeta de documentación, lista de ClickUp y
**los comandos de los checks** se declaran por repo.
**Porqué.** Las skills son genéricas, pero cada repo tiene sus propios comandos. Así
nadie edita una skill para adaptarla a un repo.

## D-10 · Los checks locales y los del CI son los mismos

**Decisión.** `scripts/flow-checks.mjs` corre los checks del config. Lo ejecutan
dev-flow (en cada fase), pr-flow (después de actualizar con dev) **y** el workflow del PR.
**Porqué.** El documento dice que el PR es la red de seguridad y no el lugar donde se
descubren los problemas. Eso solo es cierto si el CI no corre nada que el dev no haya
corrido ya. Con una sola definición, no hay diferencias.
El CI agrega lo que no tiene sentido en cada fase: escaneo de secretos (gitleaks),
revisión de dependencias y verificación del formato del título.

## D-11 · `merge`, no `rebase`, para actualizar con dev

**Decisión.** pr-flow hace `git merge origin/dev`. Si hay conflicto, deja el merge en
curso, lista los archivos y se detiene.
**Porqué.** Después de un rebote la rama ya está publicada, y un rebase obligaría a
hacer `push --force`. El historial queda menos lineal, pero la regla "pr-flow hace el
único push y nunca reescribe" queda garantizada. El conflicto lo resuelve una persona
porque resolverlo bien requiere saber qué quería cada lado.

## D-12 · Nombres: `CU-<id>` en la rama, los commits y el título del PR

**Decisión.** Rama `feat|fix|module/CU-<id>-<slug>`, commits
`feat(CU-<id>): fase n — …`, PR `[CU-<id>] <título>`.
**Porqué.** La integración GitHub ↔ ClickUp enlaza automáticamente todo lo que lleva
`CU-<id>`: la trazabilidad (tarea ↔ rama ↔ PR) sale sin trabajo manual. El CI rechaza
PRs sin el prefijo.

## D-13 · Costo de IA calculado desde los transcripts de Claude Code

**Contexto.** El documento pide registrar el costo de IA "sin esfuerzo manual".
**Decisión.** `ai-cost.mjs` lee `~/.claude/projects/<repo>*/**/*.jsonl`, filtra las
respuestas cuyo `gitBranch` es la rama de la tarea, elimina duplicados por id de
mensaje y aplica la tabla de precios (`pricing.json`, con escritura y lectura de caché
y modo fast). pr-flow **sobrescribe** el campo con el total.
**Porqué.** Claude Code ya guarda `gitBranch`, modelo y uso de tokens en cada respuesta:
es la fuente más exacta que existe sin instrumentar nada. Filtrar por rama atribuye el
costo a la tarea aunque se haya trabajado en varias sesiones, worktrees o subagentes.
Sobrescribir (en vez de sumar) hace que repetir pr-flow no cuente dos veces.
**Límite conocido.** Solo ve las sesiones de la máquina de quien entrega. Con un plan de
suscripción, la cifra es costo equivalente a precio de API, no lo facturado. Sirve igual
para comparar tareas entre sí, que es para lo que se usa.
**Probado** con transcripts reales (una rama de 7 sesiones, 1.265 respuestas).

## D-14 · Tiempo con el time tracking nativo de ClickUp

**Decisión.** dev-flow inicia el timer al empezar (y en cada rebote) y pr-flow lo detiene.
**Porqué.** Es lo que ya usan los reportes de ClickUp. Un campo propio obligaría a
construir los reportes de nuevo.

## D-15 · Rebotes: tag de quien devuelve + contador de pr-flow

**Contexto.** Las skills no mueven los estados `DEV`/`QA` (son decisiones humanas), y no
está claro que el MCP de ClickUp exponga el historial de estados.
**Decisión.** Quien devuelve la tarea le pone `rebote:pr` o `rebote:qa`. dev-flow lo
detecta, lo guarda en el estado local y quita el tag. pr-flow incrementa el contador al
entregar. Si no hay tag pero la tarea ya tenía un PR registrado, dev-flow pregunta una
sola vez.
**Porqué.** Pedir un tag es lo menos que se le puede pedir a la persona que devuelve la
tarea, y deja el dato correcto en el momento en que se produce. Contar en pr-flow (y no
en dev-flow) hace que un rebote que se abandona a la mitad no cuente.

## D-16 · Confirmaciones humanas donde algo es difícil de deshacer

**Decisión.** OK explícito para: el plan (dev-flow), cada fase antes del commit
(dev-flow) y la escritura en ClickUp (clickup-tasks). pr-flow **no** pide confirmación
para hacer push: invocarlo ya es la orden.
**Porqué.** Son los puntos que marca el documento, y coinciden con los efectos que
cuesta revertir: código en el historial y tareas creadas en una herramienta compartida.
Pedir confirmación en todos los pasos acostumbra a la gente a aprobar sin leer.

## D-17 · Skills de Chat: una sola ronda de preguntas, y con una respuesta por defecto

**Decisión.** prd-generator y techlead-spec preguntan solo lo crítico, una vez, y cada
pregunta va con la suposición que tomarán si nadie responde. Lo que se decide sin
confirmar queda en *Supuestos* o en *Decisiones del módulo*.
**Porqué.** Es la misma consigna que recibí para esta prueba, y funciona: el trabajo
avanza y cada decisión queda escrita, se puede revisar y se puede cambiar.

## D-18 · Instalación por repo, versionada

**Decisión.** `scripts/install.sh <repo>` copia dev-flow y pr-flow a
`<repo>/.claude/skills/` y agrega las plantillas **sin sobrescribir** nada que ya exista.
Las skills de Chat se empaquetan como .zip (`scripts/build.sh`).
**Porqué.** En el repo, la versión de la skill viaja con el código y todo el equipo usa
la misma. En `~/.claude/skills` cada dev tendría la suya.

## D-19 · Nombres de herramientas del MCP de ClickUp: por capacidad, no literales

**Decisión.** Las skills dicen qué hacer ("inicia el timer", "crea la subtarea con
dependencia") sin fijar nombres de herramientas del MCP.
**Porqué.** Hay varios servidores MCP de ClickUp (el oficial y los de la comunidad) con
nombres distintos, y cambian entre versiones. El modelo encuentra la herramienta por su
descripción. Lo que sí está fijado es el comportamiento cuando falta una capacidad:
detenerse y decirlo.

---

## Qué dejé fuera a propósito

- **Hooks que impidan editar antes de que se apruebe el plan.** Se puede hacer con un
  `PreToolUse` y un marcador en `.flow/`, pero agrega fricción y una pieza más que
  mantener. Por ahora es una regla de la skill; lo propondría si se ve que no se respeta.
- **Mover estados después de `PR REVIEW`** (por ejemplo, con un webhook al hacer merge).
  El documento dice que son decisiones humanas.
- **Estimaciones como compromiso.** Las horas del plan sirven para ordenar el trabajo y
  detectar tareas demasiado grandes, y así lo dice la skill.
