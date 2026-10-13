---
name: investigar
description: Fase de investigación obligatoria antes de diseñar o escribir código o CDK. Usar al empezar cualquier funcionalidad, cambio de infraestructura o decisión técnica, antes de las skills de diseño o de implementación.
---

# Investigar antes de construir

Adrián piensa e indaga mucho antes de escribir código; este paso es lo que reproduce eso. No escribas código
ni CDK hasta que Adrián apruebe el resultado de esta fase.

1. **Objetivo y restricciones.** Resume qué se quiere conseguir, para quién, con qué volumen, qué datos se
   tocan, qué presupuesto hay y qué no se puede romper. Si falta algo que cambia la decisión, pregúntalo.
2. **Contexto existente.** Lee `CLAUDE.md`, `docs/` y los ADR del repo, y el código relacionado. Si tienes
   acceso de lectura a la cuenta, mira qué recursos existen ya.
3. **Documentación oficial.** Usa el MCP `aws-knowledge` para comprobar límites, cuotas, precios, novedades y
   recomendaciones de cada servicio candidato. Cita lo que hayas comprobado; no des nada por supuesto.
4. **Alternativas.** Plantea al menos dos opciones reales y compáralas en una tabla: coste (MCP
   `aws-pricing`), complejidad, límites de AWS, seguridad, operación y cómo evolucionan.
5. **Recomendación.** Marca la opción recomendada y explica por qué, incluidos los riesgos que asumes.
6. **Preguntas abiertas** para Adrián o el cliente.
7. Entrega todo en un documento corto y, cuando Adrián lo apruebe, conviértelo en ADR (`docs/adr/`).

Aplica `principios/principios-diseno.md` del kit, en especial la sección 0.
