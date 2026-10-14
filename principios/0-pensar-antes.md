# 0. Pensar e investigar antes de escribir código

Es lo que más se valora del trabajo de Adrián y lo primero que tiene que respetar un agente.

- **No hay estándar que se aplique a ciegas.** Casi todas las decisiones (modelo de datos, tipo de API, nombres)
  dependen de lo que se quiere construir. Las reglas de este documento son puntos de partida, no recetas.
- **Ningún agente escribe código ni CDK sin una fase previa de investigación aprobada.** Esa fase entrega:
  - Qué se quiere conseguir y qué restricciones hay (volumen, quién usa el sistema, datos sensibles, coste).
  - Lo que ya existe en el repo y en la cuenta y que condiciona la decisión.
  - **Al menos dos alternativas reales**, comparadas en una tabla (coste, complejidad, límites de AWS,
    seguridad, escalabilidad, cómo evoluciona), con la recomendada marcada y el porqué.
  - Lo que se ha comprobado en documentación oficial (MCP `aws-knowledge`) y no se ha dado por supuesto.
  - Las preguntas que solo puede responder Adrián o el cliente.
- **Si falta información que cambia el diseño, se pregunta; no se inventa.**
- La investigación y la decisión quedan escritas en un ADR antes de implementar.
