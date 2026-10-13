# Catálogo de agentes (ideas)

Lista viva de agentes posibles. Prioridad: **A** (siguiente), **B** (después), **C** (más adelante).
Regla común: ningún agente despliega, fusiona ni envía nada fuera sin aprobación de Adrián.

## Estado (v0.4)

Todos los agentes de abajo están creados en `agents/`. Pendiente: probarlos con casos reales y, para `video`,
elegir herramienta de montaje y voz.

## Núcleo

| Agente | Qué hace |
|---|---|
| orquestador | Reparte el trabajo, pide aprobaciones y lleva el registro de la tarea. |
| pensador | Investiga, compara alternativas y propone el diseño y el plan. |
| implementador | Implementa el diseño aprobado en una rama. |
| revisor | Revisa contra el diseño y los principios y da un veredicto. |

## Añadidos en v0.4

| Prioridad | Agente | Qué hace | Cuándo corre | Notas |
|---|---|---|---|---|
| A | Seguridad | Audita IAM, Cognito, WAF y la exposición de buckets y APIs. Informe por gravedad. | Periódico | Solo lectura en la cuenta. |
| A | Costes | Informe por proyecto y componente con las etiquetas de coste, anomalías y ahorros. | Mensual | Depende de las etiquetas de coste. |
| A | Novedades | Novedades de AWS e IA filtradas por el stack del cliente. | Semanal | |
| B | Documentador | Mantiene al día `docs/` y los diagramas después de cada merge. | Tras cada merge | |
| B | Comprobación de entrega | Comprueba que todo se ha subido: rama fusionada, pipeline en verde, docs y ADR actualizados, registro de la tarea cerrado, nada pendiente en local. | Al cerrar una tarea | Checklist automática al final del orquestador. |
| B | Tester | Tests de CDK (assertions), de las Lambdas y de contrato de la API. | Dentro del flujo | |
| B | Comunicación | Redacta emails de resumen al cliente (qué se ha hecho, qué viene, qué necesita de ellos). | Al cerrar una tarea o cada semana | Solo borradores; los envía Adrián o se envían tras su aprobación. |
| C | Vídeo de cambios | Genera un vídeo corto que explica lo cambiado: guion, diagramas o capturas y voz. | Al cerrar una tarea grande | Hay que investigar herramientas (guion + diapositivas + voz sintética). |
| C | Incidencias | Lee logs y alarmas, diagnostica y abre una tarea en el orquestador. | Bajo demanda | |
| C | Despliegue | Prepara el plan de despliegue y rollback para que lo ejecute Adrián. | Antes de desplegar | |
