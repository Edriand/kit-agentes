# Principios de diseño (borrador v0.2)

Criterio de Adrián para diseñar infraestructura AWS serverless, APIs y modelos de datos. Los agentes lo leen
antes de proponer o revisar cualquier diseño. Donde este documento y una buena práctica genérica de AWS no
coincidan, manda este documento; si hay motivo para saltárselo, el agente lo dice explícitamente en la propuesta.
Las convenciones del `CLAUDE.md` de cada repo mandan sobre las generales de este documento (lenguaje, nombres,
herramientas).

Extraído el 2026-10-12 de tres repos propios y de las respuestas de Adrián: `garage-backend`, `Nauty/nauty-backend` y
`coop-investment-fund`. Las marcas **[CONFIRMAR]** son decisiones que varían entre proyectos o
que he deducido sin que estén escritas: Adrián tiene que decidir cuál es la regla.

Cada tema está en su propio fichero para que cada agente lea solo lo que necesita: un fichero suelto pesa poco y
se paga en todas las llamadas del agente que lo lee.

| Fichero | Quién lo lee |
|---|---|
| `0-pensar-antes.md` | Pensador, siempre. Investigar y comparar alternativas antes de escribir código. |
| `seguridad-escalabilidad.md` | Pensador, implementador, tester y revisor, siempre. |
| `1-forma-de-trabajar.md` | Pensador y documentador: documentación, ADR, idioma. |
| `2-cdk.md` | Quien toque infraestructura con CDK. |
| `3-lambda.md` | Quien toque funciones Lambda. |
| `4-apis.md` | Quien diseñe o cambie una API. |
| `5-datos.md` | Quien diseñe o cambie el modelo de datos. |
| `6-identidad-y-seguridad.md` | Quien toque Cognito, IAM, secretos, WAF u observabilidad. |

El orquestador dice a cada agente qué ficheros le tocan según la tarea.

## Preguntas abiertas

Las marcas **[CONFIRMAR]** de los ficheros de cada tema, más:

1. ¿Cuándo eliges EC2 o contenedores en lugar de Lambda?
2. ¿Cuántas cuentas AWS por cliente (una por entorno, o dev y pro en la misma como en Nauty)?
3. ¿Qué no aceptarías nunca en un diseño, aunque lo pidiera el cliente?
