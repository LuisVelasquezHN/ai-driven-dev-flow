# PRD — Pedidos Ferretería

**Versión:** 1.0 · **Fecha:** 2026-11-02 · **Fuente:** `examples/brief-ejemplo.md`

> Generado con la skill `prd-generator`. Ronda de preguntas: la skill identificó 4 huecos
> críticos (ver *Supuestos*). Siguiendo la consigna de la prueba, nadie las respondió y
> se tomaron las suposiciones anunciadas.

## 1. Problema
Los vendedores de las 3 sucursales toman pedidos de clientes empresa por WhatsApp y los
copian a un Excel. Se pierden pedidos, bodega no tiene una lista confiable de qué preparar
y nadie puede responder "¿en qué estado está mi pedido?" sin preguntar en cadena. El
gerente no tiene cifras del mes sin consolidar el Excel a mano.

## 2. Objetivo y métricas de éxito
| Métrica | Hoy | Meta | Plazo |
|---|---|---|---|
| Pedidos de clientes empresa registrados en la app | 0 % | 100 % | 60 días tras el lanzamiento |
| Pedidos reportados como perdidos por clientes | Sin registro (ocurre) | 0 por mes | 90 días tras el lanzamiento |
| Tiempo para responder el estado de un pedido | Minutos (llamadas entre sucursal y bodega) | < 30 s (consulta en la app) | Desde el lanzamiento |
| Tiempo del gerente para obtener el resumen mensual | Horas (consolidar Excel) | < 1 min | Desde el lanzamiento |

## 3. Personas
| Persona | Qué necesita | Frecuencia de uso |
|---|---|---|
| Vendedor | Registrar clientes empresa y crear pedidos rápido, y saber en qué estado están | Diaria, varias veces |
| Encargado de bodega | Ver qué pedidos de su sucursal preparar y marcar el avance | Diaria, continua |
| Gerente | Ver pedidos y monto movido por sucursal en el mes | Semanal |
| Administrador | Cargar y actualizar el catálogo, gestionar usuarios | Mensual |

## 4. Requerimientos funcionales
| ID | Como… | Quiero… | Para… | Fase |
|---|---|---|---|---|
| RF-01 | Administrador | Importar el catálogo desde el Excel actual (código, nombre, categoría, precio), creando o actualizando por código | No digitar 2.000 productos ni mantener dos fuentes | MVP |
| RF-02 | Vendedor | Buscar productos por nombre o código | Armar pedidos rápido | MVP |
| RF-03 | Vendedor | Registrar y editar clientes empresa | Asociarles pedidos sin repetir sus datos | MVP |
| RF-04 | Vendedor | Crear un pedido para un cliente, en una sucursal, con productos y cantidades | Que el pedido quede registrado y no se pierda | MVP |
| RF-05 | Vendedor | Cancelar un pedido mientras está pendiente | Corregir pedidos mal tomados | MVP |
| RF-06 | Vendedor | Ver mis pedidos y su estado actual | Responder al cliente sin llamar a bodega | MVP |
| RF-07 | Encargado de bodega | Ver los pedidos pendientes de mi sucursal, del más antiguo al más nuevo | Saber qué preparar y en qué orden | MVP |
| RF-08 | Encargado de bodega | Marcar un pedido como preparado y luego como despachado | Que todos vean el avance real | MVP |
| RF-09 | Gerente | Ver, por mes y por sucursal, cantidad de pedidos despachados y monto total | Seguir el negocio sin consolidar Excel | MVP |
| RF-10 | Administrador | Crear usuarios, asignarles rol y sucursal, y desactivarlos | Que cada persona vea solo lo que le corresponde | MVP |
| RF-11 | Administrador | Crear y editar productos uno por uno | Ajustes puntuales sin reimportar el Excel | Fase 2 |
| RF-12 | Vendedor | Que el cliente reciba un aviso cuando su pedido se despacha | Reducir consultas de estado | Fase 2 |
| RF-13 | Gerente | Ver tendencias y comparar meses en gráficos | Análisis más allá del mes en curso | Fase 2 |

## 5. Requerimientos no funcionales
| ID | Requerimiento (verificable) | Fase |
|---|---|---|
| RNF-01 | Todas las pantallas del vendedor y de bodega se pueden usar en un celular desde 360 px de ancho | MVP |
| RNF-02 | La búsqueda de productos responde en menos de 1 s con 5.000 productos cargados | MVP |
| RNF-03 | Cada cambio de estado de un pedido guarda quién lo hizo y cuándo, y no se puede borrar | MVP |
| RNF-04 | Se accede con usuario y contraseña; cada rol ve solo lo suyo (bodega y vendedor, solo su sucursal) | MVP |
| RNF-05 | El precio de cada línea queda fijo al crear el pedido: reimportar el catálogo no cambia pedidos existentes | MVP |

## 6. Alcance
### MVP (Fase 1)
- RF-01 a RF-10, RNF-01 a RNF-05.
### Fase 2
- RF-11 — la reimportación del Excel cubre los cambios en el MVP.
- RF-12 — requiere elegir canal (WhatsApp Business / correo) y tiene costo por mensaje.
- RF-13 — el MVP ya responde la pregunta principal del gerente con una tabla.
### Fuera del MVP (no se hará por ahora)
- Pagos en línea — explícito en el brief: los clientes pagan por transferencia.
- Conciliación contable — la hace contabilidad fuera del sistema.
- Control de stock / inventario — no es el problema que duele hoy y duplica el alcance.
- Portal para que el cliente haga pedidos solo — primero hay que ordenar el proceso interno.
- App móvil nativa — RNF-01 cubre el uso en celular con la web.

## 7. Restricciones
- Plazo: 3 meses; quieren algo usable antes.
- El catálogo inicial vive en un Excel de ~2.000 filas con código, nombre, categoría y precio.
- Sin pagos en línea.

## 8. Supuestos
- S-01: **Un solo precio de lista por producto** (el del Excel), sin precios por cliente ni descuentos. *Pregunta que se habría hecho: ¿hay precios especiales por cliente?* Si los hay, cambia el modelo de pedido.
- S-02: **El pedido pertenece a una sucursal** que elige el vendedor, por defecto la suya; la bodega de esa sucursal lo prepara.
- S-03: **Despacho completo**: un pedido se prepara y despacha entero, sin despachos parciales.
- S-04: **Los precios del Excel son finales** (impuestos incluidos); el sistema no calcula impuestos.
- S-05: El monto del reporte del gerente cuenta solo pedidos **despachados** (lo pendiente aún puede cancelarse).
- S-06: El Administrador es un rol aparte; puede asignarse a la misma persona que el gerente.

## 9. Riesgos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| El Excel del catálogo tiene filas sucias (códigos repetidos, precios vacíos) | Importación bloqueada | La importación reporta filas inválidas e importa el resto (RF-01) |
| Vendedores siguen usando WhatsApp por costumbre | No se cumple la métrica de 100 % | Alta de pedido en < 1 min en celular (RNF-01); el gerente mide con RF-09 |
| S-01 es falso (hay precios por cliente) | Rehacer el modelo de pedido | Validar S-01 con el cliente antes de empezar el módulo de pedidos |

## 10. Preguntas abiertas
- ¿Qué canal prefieren para avisar al cliente (RF-12)? Bloquea la Fase 2, no el MVP.
- ¿Necesitan exportar el resumen del gerente a Excel? Se puede sumar a RF-09 si es simple.
