---
name: disenar-api
description: Diseñar o revisar una API (recursos, rutas, autenticación, errores, paginación) sobre API Gateway con el criterio de Adrián. Usar cuando pidan endpoints nuevos, un contrato de API o revisar uno existente.
---

# Diseñar API

1. Lee `principios/4-apis.md` del kit y el `docs/api.md` del repo si existe.
2. Identifica quién llama (personas, máquinas, agentes, terceros por webhook). Si llaman personas y máquinas,
   plantea dos APIs separadas.
3. Compara HTTP API y REST API para este caso con los criterios de `principios/4-apis.md` (WAF, API
   keys, validación, caché, coste) y recomienda una. Nunca la elijas por defecto.
4. Para cada endpoint define: método y ruta orientada a recurso, autenticación (Cognito por defecto; cualquier
   excepción justificada), cuerpo de petición y de respuesta, códigos de estado y reglas de negocio que valida.
5. Aplica siempre: `404` para recursos privados ajenos, paginación con `nextToken`, throttling explícito y CORS
   con orígenes por entorno.
6. Entrega el resultado en el formato de `docs/api.md` (tabla Método | Ruta | Auth | Descripción, y detalle por
   endpoint) y lista las Lambdas que harán falta con su nombre según el patrón.
