# 3. Cómputo (Lambda)

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
