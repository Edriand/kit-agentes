# 2. Infraestructura como código (CDK)

- **Todo en CDK**, nada a mano en consola. Excepción documentada: valores de secretos y recursos de terceros
  (ej. precios de Stripe) que se cargan después del despliegue y se referencian por configuración.
- **TypeScript** para proyectos serverless de API; **Python** cuando el dominio es Python. **[CONFIRMAR]** ¿En
  un cliente siempre TypeScript?
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
