---
name: prd-generator
description: Convierte una idea, un brief o una conversación en un documento de requerimientos de producto (PRD) con usuarios, alcance del MVP y fases. Úsala cuando alguien quiera "arrancar un proyecto", "escribir el PRD", "definir el MVP", "bajar a requerimientos esta idea" o pegue un brief de cliente. No diseña endpoints, tablas ni arquitectura; eso es techlead-spec.
---

# prd-generator

Primer paso del flujo. Entrada: una idea, un brief o una conversación. Salida: el PRD
que consume `techlead-spec`.

## Reglas

1. **Lee todo antes de preguntar.** La conversación completa y cada documento adjunto.
   Extrae lo que ya está dicho; no lo vuelvas a preguntar.
2. **Una sola ronda de preguntas, y solo si falta algo crítico.** Crítico = sin esa
   respuesta el PRD sería distinto en su alcance (quién es el usuario principal, cuál es
   el problema, alguna restricción dura de negocio o regulatoria). Máximo 5 preguntas,
   numeradas, cada una con la suposición que tomarás si no responden.
   Si nada es crítico, no preguntes: decide y deja la decisión en *Supuestos*.
3. **Nivel producto, nunca técnico.** Prohibido: endpoints, tablas, frameworks,
   lenguajes, nombres de servicios. Si el brief los trae como restricción del cliente
   ("debe usar Postgres"), van en *Restricciones* tal cual, sin desarrollarlos.
4. **Todo requerimiento es verificable.** Si no se puede comprobar, reescríbelo o
   muévelo a *Preguntas abiertas*.
5. **El MVP es pequeño a propósito.** Ante la duda, una funcionalidad va a Fase 2.
   Cada exclusión del MVP lleva su porqué en una línea.

## Proceso

1. Resume en 3 líneas lo que entendiste (problema, para quién, resultado esperado).
2. Si hay huecos críticos → la ronda única de preguntas (regla 2) y espera.
   Si el usuario dice "decide tú" o no responde algo → aplica la suposición anunciada.
3. Redacta el PRD con `templates/prd.md`. Numera los requerimientos (`RF-01`, `RNF-01`)
   porque `techlead-spec` y `backlog-generator` los referencian por ese ID.
4. Revisa contra la checklist de abajo y entrega el documento completo en un solo
   bloque Markdown (o como archivo `.md` si el entorno lo permite), titulado
   `PRD — <nombre del proyecto>`.
5. Cierra con una línea: "Siguiente paso: `techlead-spec` con este PRD."

## Checklist antes de entregar

- [ ] Cada persona tiene al menos un requerimiento que la sirve.
- [ ] Cada `RF` está en exactamente una fase.
- [ ] Hay al menos un punto en *Fuera del MVP* con su porqué.
- [ ] Las métricas de éxito tienen número y plazo.
- [ ] Cero lenguaje técnico fuera de *Restricciones*.
- [ ] Toda decisión tomada sin confirmar está en *Supuestos*.
