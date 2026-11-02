# Estándar de definición de tarea (Definition of Ready)

Una tarea solo puede entrar a ClickUp si cumple **todo** lo de su tipo. Lo usan
`backlog-generator` (al redactar), `clickup-tasks` (al validar antes de escribir) y
`dev-flow` (al leer: si falta algo, se detiene y lo anota en ClickUp en vez de adivinar).

## Campos comunes (todo tipo)

| Campo | Regla |
|---|---|
| Título | Verbo en infinitivo + objeto. ≤ 80 caracteres. Sin IDs ni emojis. |
| Tipo | `bug` · `feature` · `module` (un módulo es padre de subtareas) |
| Repo | **Exactamente uno.** Si toca back y front, son dos tareas. |
| Contexto / por qué | 1–3 frases: problema de negocio que resuelve. |
| Criterios de aceptación | Lista verificable en formato *Dado / Cuando / Entonces*. Mínimo 2. |
| Fuera de alcance | Qué **no** hace esta tarea. Mínimo 1 punto. Evita el scope creep. |
| Pruebas | Qué pruebas deben existir al cerrar (unitarias, integración, e2e) y qué casos. |
| Dependencias | IDs de las tareas que deben estar en `Dev` antes de empezar esta. Vacío = puede empezar ya. |
| Tags | Área (`db`, `backend`, `frontend`, `design`, `tests`) + `mod:<slug-del-módulo>` |

## Adicionales por tipo

### feature / subtarea de módulo
- **Contrato**: si expone o consume una interfaz (endpoint, evento, componente público,
  tabla), se describe aquí: método + ruta + request/response, o firma, o columnas.
  Una tarea de frontend referencia el contrato de la tarea de backend de la que depende.
- **Pantallas / comportamiento** (si aplica): estados vacío, carga, error y éxito.

### bug
- **Pasos para reproducir**, **resultado actual**, **resultado esperado**, **entorno**
  (dev/staging/prod, versión o commit si se conoce).
- **Prueba de regresión**: exactamente una, que falla antes del fix y pasa después.

### module (tarea padre)
- Objetivo del módulo, link a la spec del módulo y lista ordenada de subtareas.
- Las pruebas del módulo son **la última** subtarea.
- No lleva criterios propios de código: los criterios viven en las subtareas.

## Señales de que una tarea NO está lista
- "etc.", "y lo que haga falta", "similar a X" sin decir qué es X.
- Criterios que no se pueden comprobar ("que sea rápido", "que se vea bien").
- Más de un repo, o más de ~1 día de trabajo para una subtarea (se parte).
