---
name: disenar-arquitectura
description: Proponer la arquitectura AWS de un sistema o funcionalidad nueva a partir de unos requisitos, siguiendo los principios de diseño de Adrián. Usar cuando pidan diseñar, plantear o proponer infraestructura, o evaluar un diseño existente.
---

# Diseñar arquitectura

1. Si no se ha hecho ya, empieza por la skill `investigar`. Lee `principios/principios-diseno.md` del kit y el
   `CLAUDE.md` y `docs/` del repo del cliente.
2. Si faltan requisitos que cambian el diseño (volumen, quién llama a la API, datos sensibles, presupuesto,
   cuentas y entornos), pregúntalos antes de proponer. Si no son decisivos, elige un valor razonable y dilo.
3. Consulta el MCP `aws-knowledge` para confirmar límites, precios y novedades de los servicios que propongas.
   No te fíes de lo que recuerdes.
4. Entrega una propuesta con:
   - Diagrama (Mermaid) con los servicios y el flujo de una petición.
   - Tabla de servicios: qué hace cada uno y por qué ese y no otro.
   - División en stacks (estado frente a cómputo; dominios si es grande) y nombres de recursos según el patrón.
   - Seguridad: autenticación, permisos, secretos y qué decide una persona.
   - Coste estimado mensual con el MCP `aws-pricing`, indicando los supuestos.
   - Riesgos y restricciones conocidas de AWS que afecten al despliegue.
5. Si te apartas de un principio, márcalo con **Desviación:** y explica por qué.
6. Guarda la decisión como ADR en `docs/adr/NNNN-titulo.md` (Decisión, Por qué, Consecuencias).
7. No implementes ni despliegues nada hasta que Adrián apruebe la propuesta.
