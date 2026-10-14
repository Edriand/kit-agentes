# El kit como producto (idea, 2026-10-14)

Propuesta de Adrián: un backend multiempresa donde cada cliente configura, por agente, su documentación y sus
herramientas; después, ejecución remota sobre los repos del cliente con su cuenta, para no entregar las skills y
que cada cliente pague sus tokens; más adelante, frontend y pagos con Stripe.

Caso que lo motiva, Dathum:

- Documentación en **Outline**, que pide API key para escribir.
- Tareas en un **tablero concreto de GitLab**, con `glab`.
- **Incidencias en una app propia.**

## 1. Configuración por cliente y por agente

Se puede empezar ya, sin backend, y es lo que más falta hace para trabajar en Dathum.

- **Perfil de cliente** fuera del repo del kit (tiene datos del cliente): `~/work/clientes/<cliente>/` con
  - `perfil.md`: herramientas y reglas por agente. Ejemplos: el documentador publica en Outline, en la
    colección X; el orquestador apunta la tarea en el tablero Y de GitLab; las incidencias van a la app propia.
  - `.mcp.json`: servidores MCP del cliente (Outline, GitLab, la API de su app de incidencias).
  - Secretos en variables de entorno o en el llavero, nunca en ficheros.
- El orquestador lee el perfil en el paso 0, entre el encargo y las reglas del repo.
- Herramientas:
  - Outline: comprobar si tiene servidor MCP oficial; si no, la API con `OUTLINE_API_KEY`.
  - GitLab: `glab` con el tablero indicado.
  - App de incidencias propia: hace falta conocer su API, y con ella un MCP o un script pequeño.
- **Backend después**, cuando haya más de dos o tres clientes. Es AWS serverless, lo que mejor domina Adrián:
  - Cognito con un grupo por organización.
  - API Gateway y Lambda.
  - DynamoDB con la organización como clave de partición.
  - Secrets Manager con KMS por cliente para sus API keys.
  - Auditoría de quién cambia qué.

## 2. Ejecución remota con la cuenta del cliente

**Con la suscripción de Claude del cliente no se puede.** Lo prohíben los términos de Anthropic (comprobado el
2026-10-14):

- «Anthropic does not permit third-party developers to offer Claude.ai login into their own applications, or
  to route requests through Free, Pro, or Max plan credentials on behalf of their users. Moreover, developers
  may not collect, store, or intermediate Claude.ai credentials or session tokens.»
  (https://code.claude.com/docs/en/legal-and-compliance.md)
- El Agent SDK dice lo mismo: no se puede ofrecer el login de claude.ai sin aprobación previa de Anthropic
  (https://code.claude.com/docs/en/agent-sdk/overview.md).

Lo que sí está permitido es que cada cliente use su propia credencial y que el consumo se le facture
directamente a él:

- Su **API key** de la Claude Console.
- O su proveedor de nube: **Amazon Bedrock**, Vertex o Foundry.

Para un cliente en AWS, como Dathum, lo mejor es Bedrock en su propia cuenta:

- Un rol entre cuentas, con ExternalId, que solo permite invocar los modelos de Claude.
- El gasto aparece en su factura de AWS y los datos no salen de su cuenta.
- Es el mismo patrón que el rol de solo lectura de la fase 4.

Diseño del ejecutor:

- Un contenedor aislado por tarea, por ejemplo ECS Fargate.
- Clona los repos con un token de despliegue del cliente, de alcance mínimo y que caduca.
- Corre Claude Code o el Agent SDK con el kit cargado desde nuestro disco.
- Las aprobaciones de Adrián, o del cliente, llegan por web o por chat.
- Al terminar, el contenedor se destruye.
- **Métricas e insights:** al ejecutar nosotros, cada llamada devuelve su uso exacto. Desaparecen los límites
  del script actual (salida de subagentes infravalorada, cifra oficial solo con `/exit`, métricas a mano). Con
  todas las tareas en un sitio se ve el coste por cliente y por agente, dónde corrige Adrián y qué modelo
  conviene a cada agente.
- La documentación de hosting del Agent SDK cubre el aislamiento entre clientes:
  https://code.claude.com/docs/en/agent-sdk/hosting.md

**Las skills no quedan del todo ocultas.** Ejecutar en nuestra infraestructura evita entregar los ficheros,
pero las skills entran en el contexto del modelo y en las transcripciones, y una respuesta puede citarlas. El
valor que se vende es el criterio de Adrián y su revisión, no la confidencialidad de unos prompts.

## 3. Frontend y pagos

- Frontend para dar de alta la organización, configurar los agentes y las herramientas, lanzar tareas y
  aprobarlas.
- Stripe Billing con cuota mensual por organización o por tarea. **Nunca revender tokens:** los términos
  prohíben pagar, revender o hacer de intermediario del uso de Claude de los clientes. Se cobra el servicio; el
  modelo lo paga cada cliente con su credencial.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Contrato con Keepler/Accenture: un producto propio pesa más que una consultoría (propiedad intelectual, no competencia) | Revisarlo antes de construir la plataforma, no solo antes de cobrar |
| Custodiar credenciales y código de clientes convierte la plataforma en un objetivo | Credenciales de alcance mínimo y que caducan, KMS por cliente, contenedores efímeros, auditoría; más adelante, una certificación tipo SOC 2 si la piden |
| Términos de Anthropic | Solo API key o proveedor de nube del cliente. Si se quiere otra cosa, preguntar a ventas de Anthropic |
| Construir la plataforma antes de validar el servicio | Primero el perfil por ficheros con Dathum; el backend solo si hay más clientes |
