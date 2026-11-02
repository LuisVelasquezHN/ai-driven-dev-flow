## Módulo <N> — <Nombre> (`mod:<slug>`)

**Capa:** catálogo | identidad | entidad | transacción
**Depende de:** <módulos previos o "ninguno">
**Cubre:** RF-xx, RF-yy
**Repos:** <owner/backend>, <owner/frontend>

### Datos
| Tabla / colección | Campo | Tipo | Reglas (nulo, único, FK, default) |
|---|---|---|---|

### Contratos
| Operación | Método y ruta / firma | Entrada | Salida | Errores |
|---|---|---|---|---|
| Listar | `GET /api/<recurso>?page=&q=` | — | `{ items: [...], total }` | 401 |

### Pantallas
| Pantalla | Para quién | Qué muestra | Acciones | Estados (vacío / carga / error) |
|---|---|---|---|---|

### Comportamiento y reglas de negocio
- <Regla verificable, p. ej. "un producto con pedidos no se borra, se desactiva">

### Casos borde
- <Qué pasa si…>

### Decisiones del módulo
- <Decisión> — <porqué>
