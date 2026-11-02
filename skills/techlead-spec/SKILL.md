---
name: techlead-spec
description: Convierte un PRD en módulos técnicos ordenados por dependencia de datos, con modelo de datos, pantallas, comportamiento y contratos por módulo. Úsala después de prd-generator, o cuando pidan "la spec técnica", "partir el proyecto en módulos", "definir el modelo de datos" o "el orden de desarrollo". Deja la entrada lista para diseño visual y para backlog-generator.
---

# techlead-spec

Segundo paso. Entrada: el PRD (con IDs `RF-xx`). Salida: una spec técnica por módulo,
en orden de desarrollo.

## Reglas

1. **Orden por dependencia de datos**, siempre en estas capas:
   1. **Catálogos** — datos de referencia que casi no cambian (países, categorías, estados).
   2. **Identidad** — usuarios, roles, permisos, autenticación.
   3. **Entidades** — los objetos principales del negocio (clientes, productos, proyectos).
   4. **Transacciones** — lo que relaciona entidades en el tiempo (pedidos, pagos, reservas).
   Un módulo nunca depende de uno posterior. Si aparece un ciclo, el módulo está mal
   partido: sepáralo. Si un módulo anterior necesita algo transversal de uno posterior
   (p. ej. proteger con autenticación las rutas del catálogo), lo aplica el posterior
   sobre lo existente, y se anota en las decisiones de ambos módulos.
2. **No repitas lo que ya está escrito.** Si el PRD ya dice algo, se referencia por su
   ID (`RF-03`), no se reescribe.
3. **Entrevista módulo por módulo, no todo de golpe.** Por cada módulo, presenta tu
   propuesta y pregunta solo lo que cambie pantallas o comportamiento
   (máximo 3 preguntas por módulo, cada una con tu propuesta por defecto).
   Si el usuario dice "sigue" o "decide tú", aplica tus propuestas y anótalas como
   decisiones del módulo.
4. **Modelo de datos solo si no lo dan.** Si el usuario trae un modelo (DDL, diagrama,
   tabla), se respeta y solo se señalan huecos. Si no, se propone uno.
5. **Cada `RF` del MVP queda cubierto por al menos un módulo.** Lo verificas en la
   matriz de trazabilidad al final.
6. Stack: si el PRD o el usuario lo fijan, se usa. Si no, propón uno en la sección
   *Decisiones técnicas* con su porqué y sigue; no lo conviertas en pregunta.

## Proceso

1. Lee el PRD. Lista los módulos candidatos agrupados por capa y muéstralos con el orden
   propuesto y las dependencias (una tabla). Pide OK o ajustes a esa lista — es la única
   validación global.
2. Para cada módulo en orden: propuesta → (preguntas, si hay) → spec final con
   `templates/module-spec.md`.
3. Al terminar todos, entrega el documento consolidado `Spec técnica — <proyecto>`:
   - Decisiones técnicas (stack, repos, convenciones) con su porqué.
   - Modelo de datos global (diagrama Mermaid `erDiagram`).
   - Specs de módulos en orden.
   - Matriz de trazabilidad `RF → módulo(s)`.
4. Cierra con: "Siguiente paso: diseño visual de las pantallas listadas y
   `backlog-generator` con PRD + esta spec."

## Qué NO hace
- No crea tareas ni estima horas (eso es backlog-generator).
- No escribe código ni migraciones; describe columnas y contratos, no implementación.
