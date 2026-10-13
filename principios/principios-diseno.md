# Principios de diseño (borrador v0.2)

Criterio de Adrián para diseñar infraestructura AWS serverless, APIs y modelos de datos. Los agentes lo leen
antes de proponer o revisar cualquier diseño. Donde este documento y una buena práctica genérica de AWS no
coincidan, manda este documento; si hay motivo para saltárselo, el agente lo dice explícitamente en la propuesta.
Las convenciones del `CLAUDE.md` de cada repo mandan sobre las generales de este documento (lenguaje, nombres,
herramientas).

Extraído el 2026-10-12 de tres repos propios y de las respuestas de Adrián: `garage-backend`, `Nauty/nauty-backend` y
`coop-investment-fund`. Las marcas **[CONFIRMAR]** son decisiones que varían entre proyectos o
que he deducido sin que estén escritas: Adrián tiene que decidir cuál es la regla.

---

## 0. Pensar e investigar antes de escribir código

Es lo que más se valora del trabajo de Adrián y lo primero que tiene que respetar un agente.

- **No hay estándar que se aplique a ciegas.** Casi todas las decisiones (modelo de datos, tipo de API, nombres)
  dependen de lo que se quiere construir. Las reglas de este documento son puntos de partida, no recetas.
- **Ningún agente escribe código ni CDK sin una fase previa de investigación aprobada.** Esa fase entrega:
  - Qué se quiere conseguir y qué restricciones hay (volumen, quién usa el sistema, datos sensibles, coste).
  - Lo que ya existe en el repo y en la cuenta y que condiciona la decisión.
  - **Al menos dos alternativas reales**, comparadas en una tabla (coste, complejidad, límites de AWS,
    seguridad, cómo evoluciona), con la recomendada marcada y el porqué.
  - Lo que se ha comprobado en documentación oficial (MCP `aws-knowledge`) y no se ha dado por supuesto.
  - Las preguntas que solo puede responder Adrián o el cliente.
- **Si falta información que cambia el diseño, se pregunta; no se inventa.**
- La investigación y la decisión quedan escritas en un ADR antes de implementar.

## 1. Forma de trabajar

- **La documentación vive en el repo y es la fuente de verdad.** Cada proyecto tiene `CLAUDE.md` (convenciones,
  comandos, restricciones conocidas) y `docs/` con `architecture.md`, `api.md` y `data-model.md`.
- **Las decisiones se registran como ADR** en `docs/adr/NNNN-titulo.md` con *Decisión*, *Por qué* y
  *Consecuencias*. Si una decisión cambia, se escribe un ADR nuevo; no se reescribe el antiguo.
- **Los comentarios del código explican el porqué**, sobre todo cuando algo no es obvio o rompe una regla
  (ej.: por qué un recurso SES no lleva sufijo de entorno, por qué se dividió un stack).
- **Las restricciones de AWS aprendidas a base de golpes se documentan** en `CLAUDE.md` con el procedimiento
  exacto (ej.: un solo GSI por actualización de CloudFormation).
- Idioma: código e identificadores en inglés; documentación y comentarios en español. **[CONFIRMAR]**
  `garage-backend` tiene la documentación en inglés.

## 2. Infraestructura como código (CDK)

- **Todo en CDK**, nada a mano en consola. Excepción documentada: valores de secretos y recursos de terceros
  (ej. precios de Stripe) que se cargan después del despliegue y se referencian por configuración.
- **TypeScript** para proyectos serverless de API; **Python** cuando el dominio es Python. **[CONFIRMAR]** ¿En
  Dathum siempre TypeScript?
- **Configuración por entorno en un fichero tipado** (`config/environments.ts`: cuenta, región, orígenes
  permitidos, dominios). El entorno se elige con contexto: `cdk deploy -c env=pro`.
- **Región por defecto `eu-west-1`.**
- **Nombres explícitos y deterministas en todos los recursos**, con una función `buildResourceName()` compartida:
  `{proyecto}-{entorno}-{servicio}-{nombre}` (ej. `nauty-backend-pro-dynamodb-quotes`).
  Nunca se deja que CDK genere el nombre de una Lambda. En `coop-investment-fund` un test falla si un
  recurso se queda sin nombre o se sale del patrón.
- **Versionado** (acordado con Adrián el 2026-10-12):
  - La versión de la API va en la ruta (`/v1/...`), no en el nombre de cada recurso.
  - Los recursos de cómputo (Lambdas, API, stacks de dominio) pueden llevar versión mayor en el nombre cuando
    hay que tener dos versiones incompatibles desplegadas a la vez durante una migración.
  - Los recursos con datos (tablas, buckets, user pools, secretos) **no** llevan versión en el nombre:
    cambiar el nombre físico obliga a CloudFormation a reemplazar el recurso, lo que supone crear uno nuevo y
    migrar los datos.
- **Entornos `dev` y `pro`.** **[CONFIRMAR]** En algún sitio aparece `prod`; elegir uno.
- **Separar estado y cómputo en stacks distintos**: `cognito-stack` y `data-stack` (tablas, buckets) por un
  lado; el API y los stacks de dominio por otro. Así se puede destruir y redesplegar cómputo sin tocar datos.
- **Dividir por dominio antes de llegar al límite de 500 recursos por stack.** Un stack "núcleo" crea el API
  y el authorizer; cada stack de dominio importa el API y crea sus propias rutas.
- **Política de borrado según entorno**: `RETAIN` en `pro` y `DESTROY` en `dev` para tablas, buckets, user
  pools y secretos.
- **Etiquetas de coste obligatorias desde el primer despliegue** (`project`, `environment`, `owner`,
  `component`, `cost-center`) y el synth falla si falta alguna. Activarlas como *cost allocation tags* en cuanto
  AWS las vea. Presupuesto mensual con avisos al 80 % y al 100 %. Cuanto antes se pongan, mejor se analizan
  los costes después.

## 3. Cómputo (Lambda)

- **Una Lambda por endpoint** (responsabilidad única). Handlers en `lambda/{recurso}/{acción}.ts` o una carpeta
  por función con nombre verbo-recurso (`create-quote`, `admin-approve-company`).
- **Valores por defecto compartidos** (`lambdaDefaults`): Node.js en el runtime más reciente, **ARM64**,
  timeout 10 s, 256 MB, bundling con `minify` y `sourceMap`, `NODE_OPTIONS=--enable-source-maps`.
- **Bundling**: el SDK v3 que ya trae el runtime se marca como externo; lo que no trae (ej. `client-sesv2`) se
  empaqueta. Configuraciones de bundling compartidas en un fichero, no duplicadas por stack.
- **Utilidades comunes en `lambda/shared/`**: cliente DynamoDB Document con `removeUndefinedValues`, extracción
  del `userId` (`sub`) de los claims, y helpers de respuesta HTTP (`ok`, `created`, `noContent`, `badRequest`,
  `conflict`...).
- **Permisos con `grant*` de CDK.** **[CONFIRMAR]** En `garage-backend` la función auxiliar da lectura/escritura
  a la tabla y al bucket a todas las Lambdas. ¿Aceptable en proyectos pequeños o siempre mínimo privilegio
  por función (`grantReadData` en las de lectura)?
- Tareas programadas con **EventBridge Scheduler** (grupo y rol compartidos, expuestos por el stack núcleo).
- Procesos de varios pasos o de larga duración con **Step Functions**.

## 4. APIs

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

## 5. Datos

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

## 6. Identidad y seguridad

- **Cognito User Pool**: login con email, verificación por email, recuperación solo por email,
  `preventUserExistenceErrors`, revocación de tokens, tokens de acceso de 1 h y de refresco de 30 días, emails
  enviados con SES desde dominio propio. Plan *Essentials* con OTP por email como primer factor.
- **Clientes sin secreto** para web/móvil y sin flujos OAuth si no hacen falta.
- **Secretos en Secrets Manager**, nunca en variables de entorno en claro. CDK crea el contenedor; el valor se
  carga a mano después del despliegue y el procedimiento queda documentado.
- **Credenciales de terceros de los usuarios cifradas con KMS** (envelope encryption con contexto `user_id`);
  nunca se devuelven por la API ni aparecen en logs.
- **Las acciones irreversibles o de dinero las confirma una persona**, nunca un agente ni una key.
- **Observabilidad**: logs de acceso del API, X-Ray en el API, alarmas de tasa de error y latencia p99.
- **WAF con las reglas básicas recomendadas por AWS** como punto de partida:
  - `AWSManagedRulesCommonRuleSet` (riesgos OWASP habituales).
  - `AWSManagedRulesKnownBadInputsRuleSet`.
  - `AWSManagedRulesAmazonIpReputationList`.
  - Una regla de límite de peticiones por IP (rate-based).
  - `AWSManagedRulesSQLiRuleSet` si hay base de datos SQL detrás.
  - Primero en modo `Count` para ver falsos positivos, después en `Block`.
  - Si el WAF protege una distribución de CloudFront, se crea en `us-east-1` (scope `CLOUDFRONT`).

---

## Preguntas abiertas

Las marcas **[CONFIRMAR]** de arriba, más:

1. ¿Cuándo eliges EC2 o contenedores en lugar de Lambda?
2. ¿Cuántas cuentas AWS por cliente (una por entorno, o dev y pro en la misma como en Nauty)?
3. ¿Qué no aceptarías nunca en un diseño, aunque lo pidiera el cliente?
