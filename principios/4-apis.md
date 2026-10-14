# 4. APIs

- **Diseño REST orientado a recursos**: `/cars`, `/cars/{carId}`, `/cars/{carId}/events/{eventId}`. Los
  agregados calculados van en subrecursos de solo lectura (`/cars/{carId}/summary`).
- **API Gateway: HTTP API o REST API se decide en cada proyecto tras analizarlo**, nunca por defecto. La
  propuesta incluye la comparación con, como mínimo, estos criterios:
  - **WAF**: se puede asociar directamente a una REST API, no a una HTTP API (con HTTP API, el WAF tiene que ir
    en un CloudFront delante).
  - **API keys y usage plans**: solo REST.
  - **Validación de peticiones y modelos en el gateway, caché y transformaciones**: solo REST.
  - **Coste y latencia**: HTTP API es más barata y más simple; authorizer JWT nativo.
  - Antecedentes: `garage-backend` (REST: validadores, throttling por stage, logs JSON, X-Ray), `Nauty` (HTTP
    API con JWT), `coop` (REST por las API keys).
- **Autenticación con Cognito JWT en todos los endpoints**, salvo excepciones documentadas una a una en
  `api.md`.
- **No filtrar existencia**: un recurso privado devuelve `404` tanto si no existe como si no tienes acceso.
- **Separar quién llama**: si llaman personas y máquinas/agentes, dos APIs. Personas con Cognito; máquinas con
  API keys que solo miden y limitan, más un authorizer Lambda que traduce la key a identidad. Las acciones que
  solo puede decidir una persona no existen en la API de máquinas.
- **Paginación** con `LastEvaluatedKey` codificado en base64 y devuelto como `nextToken`.
- **Códigos**: `201` al crear, `204` al borrar, `409` ante reglas de negocio violadas, `400` con mensaje claro.
- **Throttling** definido explícitamente (ej. ráfaga 100, 50 rps).
- **CORS**: **[CONFIRMAR]** `garage-backend` usa `*`; `Nauty` restringe a los orígenes del entorno. Propuesta:
  orígenes explícitos por entorno siempre.
