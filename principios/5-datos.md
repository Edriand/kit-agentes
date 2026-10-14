# 5. Datos

- **DynamoDB en modo bajo demanda (`PAY_PER_REQUEST`) con Point-in-Time Recovery activado.**
- **El diseño empieza por los patrones de acceso**, escritos en tabla en `data-model.md` (patrón, PK, SK).
- **Single-table o una tabla por entidad no se decide por estándar**: depende de lo que se vaya a implementar.
  `garage-backend` es single-table (`USER#`, `CAR#`, `EVENT#`) y `Nauty` tiene una tabla por entidad; las dos
  son correctas para su caso. La propuesta justifica la elección con los patrones de acceso.
- **Siempre `createdAt` y `updatedAt`** (ISO 8601) en todos los items.
- **Las consultas tienen que poder ordenarse de más nuevo a más antiguo y al revés**: la fecha (o un ULID) va
  en la SK o en la SK de un GSI para poder usar `ScanIndexForward` en los dos sentidos.
- **PK, SK y GSI se piensan con mucho cuidado** antes de crear la tabla, porque cambiarlos después obliga a
  migrar datos. Prefijos de tipo en PK/SK; IDs con ULID.
- **GSI dispersos (sparse)** para consultas sobre un subconjunto de items.
- **No guardar lo que se puede derivar** (ej. los km actuales salen del último evento), salvo contadores que
  se mantienen de forma atómica (`likeCount`).
- **Las reglas de negocio se validan en el backend** y se documentan junto al modelo (ej. "como mucho un
  evento de compra", "los km nunca bajan").
- **Base relacional (Aurora Serverless v2 + Data API) cuando hacen falta orden global, consultas de
  proyección o aislamiento por fila (RLS)**. DynamoDB no es la respuesta a todo.
- **S3**: buckets privados (`BLOCK_ALL`, cifrado; **[CONFIRMAR]** añadir `enforceSSL`, que hoy no está); acceso solo con URLs prefirmadas; claves
  jerárquicas por propietario (`users/{userId}/cars/{carId}/photos/`). Las imágenes públicas salen por
  CloudFront con dominio propio delante de un bucket privado.
