---
name: revisar-cdk
description: Revisar código CDK o un merge request de infraestructura contra los principios de Adrián (nombres, entornos, seguridad, coste, límites de AWS). Usar antes de aprobar cambios de infraestructura o cuando pidan auditar un stack.
---

# Revisar CDK

Revisa el diff o los stacks indicados y comprueba, citando fichero y línea:

1. **Nombres**: todo recurso que lo admita tiene nombre explícito con el patrón del proyecto; ninguna Lambda
   sin `functionName`.
2. **Entornos**: la configuración sale del fichero de entornos; `RETAIN` en `pro` para datos; nada fijado a
   mano que dependa del entorno.
3. **Estado y cómputo**: tablas, buckets y user pools no están en un stack que se destruya con el cómputo.
4. **Permisos**: `grant*` con el mínimo necesario por función; ningún `*` en acciones o recursos sin
   justificar.
5. **Secretos**: nada sensible en variables de entorno ni en el código.
6. **Exposición**: buckets privados, CORS por entorno, autenticación en todos los endpoints salvo excepciones
   documentadas, throttling definido.
7. **Datos**: bajo demanda, PITR, como mucho un GSI nuevo por despliegue en cada tabla.
8. **Límites**: el stack no se acerca a 500 recursos.
9. **Validación automática**: usa el MCP `aws-iac` para validar las plantillas sintetizadas y, si el proyecto
   tiene `cdk-nag`, ejecútalo.

Devuelve una lista ordenada por gravedad: **Bloqueante**, **Recomendable**, **Menor**. Para cada punto, el
problema, el porqué y el cambio concreto. No hagas cambios tú: la revisión la aprueba Adrián.
