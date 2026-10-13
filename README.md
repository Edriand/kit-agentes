# Kit de agentes de Adrián (v0.4)

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
documentador ──► despliegue (plan) ──► merge request
   │
   ▼
APROBACIÓN DE ADRIÁN (merge y despliegue)
   │
   ▼
entrega (checklist) ──► comunicacion (borrador de email) ──► video (opcional)
```

Fuera del flujo, periódicos o bajo demanda: `seguridad`, `costes`, `novedades` e `incidencias`. Lo que
encuentren que haya que cambiar entra al orquestador como tarea nueva.

El orquestador lleva el registro de cada paso en `docs/tareas/{fecha}-{tarea}.md` del repo del cliente. Ningún
agente despliega ni fusiona.

Para lanzarlo, dentro de Claude Code: "orquesta esta tarea: ...".

## Qué contiene

| Ruta | Para qué |
|---|---|
| `skills/orquestar` | El orquestador: reparte el trabajo, pide las aprobaciones y lleva el registro. |
| `agents/pensador.md` | Investiga, compara alternativas y propone diseño y plan. No escribe código. |
| `agents/implementador.md` | Implementa el diseño aprobado en una rama, con synth y tests. No despliega. |
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
| `plantillas/tarea.md` | Plantilla del registro de cada tarea. |
| `ROADMAP.md` | Fases, pilotos y puntos de control hasta llevarlo a Dathum y a otros clientes. |
| `principios/principios-diseno.md` | El criterio de diseño. Es lo que hace que los agentes diseñen como Adrián. |
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
| `iam` | Consulta de usuarios, roles y políticas (`--readonly`) | Perfil AWS |
| `aws-pricing` | Estimación de costes de un diseño | Perfil AWS |

Requisitos: `uv` instalado (`brew install uv`) y un perfil de AWS con permisos de **solo lectura**. El perfil se
toma de `AWS_PROFILE`; si no está definido, usa `default`.

No incluye todavía el **AWS MCP Server** (en preview, consulta la cuenta real con auditoría en CloudTrail) ni
GitLab. Se añadirán cuando se defina el rol de solo lectura en la cuenta de Dathum.

## Probarlo en local

```bash
# Desde un repo de prueba
claude --plugin-dir /ruta/a/kit-agentes
```

Dentro de la sesión, `/mcp` muestra los servidores conectados y las skills se activan solas cuando pides
diseñar una arquitectura, una API o un modelo de datos, o revisar CDK.

Prueba sugerida: en `garage-backend`, pedir "revisa el stack con la skill revisar-cdk" y comparar el resultado
con lo que dirías tú.

## Pendiente

1. Que Adrián resuelva los **[CONFIRMAR]** de `principios/principios-diseno.md`.
2. Añadir sus fichas de buenas prácticas por servicio.
3. Probar el flujo completo con una tarea pequeña en `garage-backend`.
4. Diseñar cómo corren los agentes en GitLab CI para Dathum.
