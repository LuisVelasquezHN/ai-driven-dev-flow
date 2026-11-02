# Demo: los tres primeros pasos del flujo, ejecutados

Entrada: [`../brief-ejemplo.md`](../brief-ejemplo.md) (una ferretería con 3 sucursales
que hoy toma pedidos por WhatsApp).

| Paso | Skill | Resultado |
|---|---|---|
| 1 | `prd-generator` | [01-prd.md](01-prd.md): 13 RF (10 en el MVP), 5 RNF, 6 supuestos |
| 2 | `techlead-spec` | [02-spec-tecnica.md](02-spec-tecnica.md): 5 módulos en orden catálogo → identidad → entidad → transacción, modelo de datos, contratos y pantallas |
| 3 | `backlog-generator` | [03-backlog.json](03-backlog.json) + [04-plan.xlsx](04-plan.xlsx): 47 tareas, 16 unidades de trabajo, 7 grupos en paralelo, 127 h |
| 4 | `clickup-tasks` | **No ejecutado**: requiere una cuenta de ClickUp con el MCP conectado |

## Cómo se ejecutó

Claude ejecutó estas skills siguiendo cada `SKILL.md` al pie de la letra, en una sesión
de Claude Code (no subidas a Claude Chat). El contenido es el mismo; lo que cambia es el
entorno.

Las skills hacen preguntas cuando falta algo crítico. Siguiendo la misma consigna de la
prueba ("no hay ronda de preguntas"), nadie las respondió y se aplicaron las suposiciones
que cada skill anuncia por defecto. Quedaron escritas:
- En el PRD, sección *Supuestos* (S-01 a S-06). La más importante es S-01: precio único
  por producto, sin precios por cliente.
- En la spec, en las *Decisiones técnicas* y en las *Decisiones del módulo*.

El plan se validó con el script de la skill:

```bash
python3 skills/backlog-generator/scripts/build_plan.py examples/demo/03-backlog.json examples/demo/04-plan.xlsx
```
```
OK — 47 tareas, 16 unidades, 7 olas, 127 h
Camino crítico: S-01 → M01-BE → M02-BE → M03-BE → M04-BE → M04-FE (74 h)
```

## Lo que muestra el plan

| Grupo | Unidades que pueden ir en paralelo | Horas de la más larga |
|---|---|---|
| 1 | D-01 (sistema visual), S-01 y S-02 (preparar los repos) | 6 |
| 2 | D-02, D-03, D-04 (diseños), M01-BE (catálogos API) | 12 |
| 3 | M02-BE (identidad API) | 14 |
| 4 | M02-FE (login web), M03-BE (clientes API) | 11 |
| 5 | M01-FE, M03-FE, M04-BE (pedidos API) | 18 |
| 6 | M04-FE (pedidos web), M05-BE (reportes API) | 20 |
| 7 | M05-FE (reportes web) | 4 |

Con dos devs (uno de backend y uno de frontend) y diseño en paralelo, la cadena más larga
es de 74 h. Las horas sirven para ordenar el trabajo, no son un compromiso.

## Hallazgos al ejecutar (y lo que se corrigió en las skills)

Ejecutar el flujo con un caso real sacó a la luz cuatro cosas. Las cuatro ya están
corregidas en este repo:

1. **Un requerimiento del MVP se quedó sin tarea.** RNF-01 (uso en celular) no estaba
   asignado a ninguna tarea; lo detecté revisando a mano. Ahora `backlog.json` lleva
   `mvp_rf` y `build_plan.py` **falla** si algún requerimiento del MVP no tiene tarea. Se
   comprobó con el backlog anterior: lo rechaza y nombra RNF-01.
2. **Orden de capas y autenticación.** La regla catálogo → identidad choca con que las
   rutas del catálogo necesitan estar protegidas. Ahora `techlead-spec` dice qué hacer:
   lo transversal lo aplica el módulo posterior sobre lo existente, y se anota en ambos.
3. **Faltaban las tareas de arranque de los repos.** El proyecto parte sin repos, y
   ninguna regla generaba la tarea de crearlos. Ahora `backlog-generator` agrega una
   tarea de arranque por repo cuando el repo no existe.
4. **prd-generator y techlead-spec recibían referencias que no usan** (el estándar de
   tareas y las convenciones de ClickUp). Ahora `build.sh` solo se las copia a las skills
   que las usan.

## Para continuar la demo con ClickUp

1. Configura ClickUp según [`docs/clickup-setup.md`](../../docs/clickup-setup.md).
2. En Claude Chat, con `clickup-tasks` subida: adjunta `03-backlog.json` y pide
   "carga este backlog a ClickUp".
3. Crea `ferreteria/pedidos-api` (o cualquier repo de prueba), corre
   `scripts/install.sh`, toma S-01 con `dev-flow` y entrégala con `pr-flow`.
