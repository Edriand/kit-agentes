---
name: implementar-cdk
description: Implementar en CDK y Lambda un diseño ya aprobado, siguiendo las convenciones de Adrián. Usar solo con un plan de implementación aprobado.
---

# Implementar en CDK

1. Ten delante el diseño y el plan aprobados. Lo que no esté en el plan no se hace.
2. Antes de crear nada, mira cómo está hecho el repo (fichero de entornos, `buildResourceName`, valores por
   defecto de Lambda, utilidades de `lambda/shared/`) y reutilízalo. No dupliques lo que ya existe.
3. Aplica los principios del kit:
   - Nombre explícito en todo recurso que lo admita, con el patrón del proyecto.
   - Recursos con datos en el stack de datos, con `RETAIN` en `pro`.
   - `grant*` con el mínimo permiso por función.
   - Secretos en Secrets Manager, nunca en variables de entorno.
   - Etiquetas de coste en todos los recursos.
   - `createdAt` y `updatedAt` en todo item nuevo de DynamoDB.
4. Comenta el porqué de lo que no sea obvio.
5. Actualiza la documentación del repo (`docs/architecture.md`, `docs/api.md`, `docs/data-model.md`) en el
   mismo cambio.
6. Comprueba: compilación, `cdk synth -c env=dev`, tests y, si el proyecto lo tiene, `cdk-nag`. Usa el MCP
   `aws-iac` para validar la plantilla sintetizada.
7. Si hay que añadir más de un GSI a una tabla existente, déjalo indicado para desplegarlos de uno en uno.
8. No despliegues nunca.
