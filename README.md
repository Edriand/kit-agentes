# Kit de agentes de Adrián (v0.5)

Plugin de Claude Code para diseñar e implementar infraestructura AWS serverless con el criterio de Adrián.
Los agentes investigan antes de construir, proponen, y Adrián revisa y aprueba.

## Cómo funciona

```
Adrián pide algo
   │
   ▼
pensador ──► investigación, alternativas y plan
   │
   ▼
APROBACIÓN DE ADRIÁN (diseño) ──► ADR
   │
   ▼
implementador ──► tester ──► revisor ──┐
   ▲                                   │ cambios (máx. 3 vueltas;
   └───────────────────────────────────┘ si es de diseño, vuelve al pensador)
   │ aprobado
   ▼
documentador ──► despliegue (plan, si aplica) ──► PR o MR (con el sí de Adrián)
   │
   ▼
APROBACIÓN DE ADRIÁN (merge y despliegue)
   │
   ▼
entrega (checklist) ──► comunicacion (borrador de email) ──► video (opcional)
```

Fuera del flujo, periódicos o bajo demanda: `seguridad`, `costes`, `novedades` e `incidencias`. Lo que
encuentren que haya que cambiar entra al orquestador como tarea nueva.

El orquestador lleva el registro de cada paso en `.agentes/tareas/{fecha}-{tarea}.md` dentro del repo, excluido
de git con `.git/info/exclude` para que no acabe en ningún commit (salvo que el repo pida versionarlo). Ningún
agente hace push sin el sí de Adrián, ni fusiona, ni despliega.

Cada tarea queda además registrada en el gestor de incidencias del repo (GitHub Issues o GitLab Issues por
defecto) con una ficha completa: urgencia, estimación y tiempo real, coste, etiquetas, recursos, documentos y
personas implicadas. Se abre con el sí del diseño y se cierra con el merge.

Para lanzarlo, abre Claude Code con el kit (`claude --plugin-dir ~/work/kit-agentes`) y escribe
`/kit-adrian-aws:orquestar` seguido de la tarea. Para parar después del diseño, empieza la tarea con «Modo solo
diseño.». Una sesión abierta sin `--plugin-dir` no tiene el kit.

El orquestador corre con el modelo de la sesión. Para gastar menos, lánzalo en Sonnet (en prueba desde el
14 oct); el pensador y el revisor siguen en Opus porque lo fija cada agente:

```bash
claude --model sonnet --plugin-dir ~/work/kit-agentes
```

Si vas a tardar más de una hora en contestar al orquestador, escribe `/clear` y después
`/kit-adrian-aws:orquestar continuar {slug}` con tu respuesta: retoma desde el registro con el contexto limpio.

El implementador y el tester usan caché de 1 hora porque lanzan comandos largos (`experimental.cacheTtl`).
Necesita Claude Code 2.1.248 o posterior, y Claude Code la ignora mientras la suscripción esté gastando
créditos de uso.

Todos los agentes piensan en la **seguridad y la escalabilidad** de lo que hacen aunque la tarea no lo pida: el
pensador las analiza en el diseño, el implementador las aplica, el tester las prueba y el revisor bloquea los
riesgos sin cubrir. El criterio está en `principios/seguridad-escalabilidad.md`.

## Sirve para cualquier repo

El kit no lleva nada de un cliente concreto. Al empezar cada tarea, el orquestador fija las **reglas de la
tarea** (rama, formato y autor de los commits, autoría, cuándo se hace push, comprobaciones, plantilla del PR o
MR, alcance y ficheros generados) a partir de, por este orden: el encargo, el `CLAUDE.md` o `AGENTS.md` del repo,
el historial de git y, si nada lo dice, los valores por defecto de `skills/orquestar`. Así el mismo kit trabaja
en un repo de un cliente con GitLab y CDK en TypeScript, o en uno propio con GitHub y Python.

## Qué contiene

| Ruta | Para qué |
|---|---|
| `skills/orquestar` | El orquestador: reparte el trabajo, pide las aprobaciones y lleva el registro. |
| `agents/pensador.md` | Investiga, compara alternativas y propone diseño y plan. No escribe código. |
| `agents/implementador.md` | Implementa el diseño aprobado en una rama, con las comprobaciones del repo. No hace push ni despliega. |
| `agents/tester.md` | Escribe y ejecuta tests de CDK, Lambdas y contrato de la API. |
| `agents/revisor.md` | Revisa contra el diseño y los principios, y da un veredicto. No modifica nada. |
| `agents/documentador.md` | Mantiene `docs/` y `CLAUDE.md` al día con el cambio. |
| `agents/despliegue.md` | Prepara el plan de despliegue y rollback. No despliega. |
| `agents/entrega.md` | Checklist final: merge, pipeline, docs, ADR y registro. |
| `agents/comunicacion.md` | Borradores de email para el cliente. No envía nada. |
| `agents/video.md` | Guion por escenas y diagramas para un vídeo del cambio. |
| `agents/seguridad.md` | Auditoría de IAM, Cognito, WAF, S3, API y secretos (solo lectura). |
| `agents/costes.md` | Informe de costes por etiquetas, anomalías y ahorros (solo lectura). |
| `agents/novedades.md` | Novedades de AWS e IA filtradas por el stack del cliente. |
| `agents/incidencias.md` | Diagnóstico de errores y alarmas (solo lectura). |
| `skills/implementar-cdk` | Convenciones para implementar en CDK y Lambda. |
| `ideas/catalogo-agentes.md` | Lista priorizada de agentes futuros. |
| `plantillas/tarea.md` | Plantilla del registro de cada tarea, con sus reglas y métricas. |
| `skills/orquestar/scripts/metricas_sesion.py` | Exporta las métricas de la sesión (tiempos, mensajes, tokens, coste a precio de API) a `.agentes/metricas/`. |
| `plantillas/incidencia.md` | Ficha de la incidencia de cada tarea y cómo se guarda en GitHub, GitLab, Jira o Linear. |
| `ROADMAP.md` | Fases, pilotos y puntos de control hasta llevarlo a un cliente y a otros clientes. |
| `principios/` | El criterio de diseño, un fichero por tema (el índice está en `principios-diseno.md`). Es lo que hace que los agentes diseñen como Adrián. |
| `skills/investigar` | Fase obligatoria antes de diseñar o programar: alternativas comparadas y documentación comprobada. |
| `skills/disenar-arquitectura` | Propuesta de arquitectura con diagrama, coste y ADR. |
| `skills/disenar-api` | Contrato de API: recursos, auth, errores, paginación. |
| `skills/modelar-dynamodb` | Modelo de datos a partir de patrones de acceso. |
| `skills/revisar-cdk` | Revisión de stacks o merge requests de infraestructura. |
| `plantillas/CLAUDE.md` | Plantilla para el `CLAUDE.md` de cada repo de cliente. |
| `.mcp.json` | Servidores MCP de AWS (todos en solo lectura). |
| `.claude-plugin/plugin.json` | Manifiesto del plugin. |

## Servidores MCP

| Servidor | Para qué | Credenciales |
|---|---|---|
| `aws-knowledge` | Documentación, blogs, arquitecturas de referencia y Well-Architected al día | No necesita |
| `aws-iac` | Buenas prácticas de CDK, ejemplos de constructs, validación de plantillas | Perfil AWS |
| `aws-serverless` | Lambda, API Gateway y SAM (solo lectura por defecto) | Perfil AWS |
| `dynamodb` | Asistente de modelado y validación de modelos (`DDB-MCP-READONLY=true`) | Perfil AWS |
| `iam` | Consulta de usuarios, roles y políticas (solo lectura por defecto; nunca pasar `--allow-write`) | Perfil AWS |
| `aws-pricing` | Estimación de costes de un diseño | Perfil AWS |

Requisitos: `uv` instalado (`brew install uv`) y un perfil de AWS con permisos de **solo lectura**. El perfil se
toma de `AWS_PROFILE`; si no está definido, usa `default`.

No incluye todavía el **AWS MCP Server** (en preview, consulta la cuenta real con auditoría en CloudTrail) ni
GitLab. Se añadirán cuando se defina el rol de solo lectura en la cuenta de un cliente.

## Probarlo en local

```bash
# Desde un repo de prueba
claude --plugin-dir /ruta/a/kit-agentes
```

Claude Code añade por defecto un trailer `Co-Authored-By` a los commits y una línea a los PR. Como el kit no
firma en nombre de nadie, desactívalo en el `.claude/settings.local.json` del repo (o en `~/.claude/settings.json`
para todos):

```json
{ "attribution": { "commit": "", "pr": "", "sessionUrl": false } }
```

Dentro de la sesión, `/mcp` muestra los servidores conectados y las skills se activan solas cuando pides
diseñar una arquitectura, una API o un modelo de datos, o revisar CDK.

Prueba sugerida: en `garage-backend`, pedir "revisa el stack con la skill revisar-cdk" y comparar el resultado
con lo que dirías tú.

## Pendiente

1. Que Adrián resuelva los **[CONFIRMAR]** de los ficheros de `principios/`.
2. Añadir sus fichas de buenas prácticas por servicio.
3. Piloto en coop-investment-fund (Tarea A en marcha) y después en `garage-backend`.
4. Diseñar cómo corren los agentes en GitLab CI para un cliente.
