# Roadmap del kit de agentes

Objetivo: un equipo de agentes que diseña e implementa infraestructura AWS con el criterio de Adrián, que se
pueda ofrecer a Dathum como servicio y después a otros clientes.

Las fechas son estimaciones con 2 h/día de dedicación. Cada fase termina con un punto de control: no se pasa a
la siguiente sin revisar lo aprendido.

---

## Fase 0 · Kit inicial ✅ (12-13 oct)

- [x] v0.5: el kit no depende de ningún repo; las reglas de cada tarea salen del encargo y del repo.

- [x] Principios de diseño extraídos de garage-backend, Nauty y coop-investment-fund, y revisados con Adrián.
- [x] Skills de investigación, diseño (arquitectura, API, DynamoDB), implementación y revisión de CDK.
- [x] Orquestador con 13 agentes y registro de tareas en `docs/tareas/`.
- [x] Servidores MCP de AWS en solo lectura.

## Fase 1 · Repo y puesta en marcha (13-16 oct)

- [x] Adrián crea el repo `kit-agentes` y se sube el contenido de esta carpeta (13 oct).
- [x] Instalar `uv` y comprobar que los servidores MCP conectan (`/mcp` dentro de Claude Code) (13 oct).
- [ ] Crear un perfil de AWS de **solo lectura** para los agentes (ej. `ReadOnlyAccess` más Cost Explorer)
      en la cuenta de coop-investment-fund.
- [x] Probar que el plugin carga: `claude --plugin-dir ~/work/kit-agentes` desde coop-investment-fund y
      comprobar que aparecen las skills y los agentes.

**Punto de control:** el kit se carga sin errores y los MCP responden.

## Fase 2 · Piloto en coop-investment-fund (19-30 oct)

Se usa la fase 6 del propio proyecto (agentes LLM): trabajo real que el proyecto necesita, con diseño ya escrito.

- [x] **Tarea A, solo diseño:** "Research con LLM" (§4 y fila 4 del §14 de `docs/diseno/fase6_agentes_llm.md`),
      con el encargo que preparó el propio proyecto. El orquestador fija las reglas de la tarea y el pensador
      contrasta el diseño con el código y propone el plan; se para en la aprobación. Pone a prueba al pensador
      y la aprobación, que es la parte que más vale. Adrián compara el plan con lo que habría hecho él.
- [x] **Tarea B, flujo completo:** si el plan de la Tarea A se aprueba, la misma tarea sigue desde la
      implementación hasta el PR, pasando por tester, revisor y documentador. El push y el PR, con el sí de
      Adrián. Hecho el 13 oct: PR #86 (36,43 USD). Datos en `pilotos/coop-research-llm/`.
- [x] **Segunda tarea:** `research_debate`, ya con incidencia (#87) y métricas: PR #88 fusionado (17,31 USD).
      Datos en `pilotos/coop-research-debate/`.
- [ ] **Agentes periódicos:** una pasada de `seguridad` y otra de `costes` sobre la cuenta de coop (ya tiene
      etiquetas de coste y presupuesto).
- [ ] Apuntar en cada tarea (sección Métricas del registro):
  - Tiempo que ha dedicado Adrián y tiempo total.
  - Vueltas entre implementador y revisor.
  - Qué ha tenido que corregir Adrián y por qué.
  - Coste en tokens.

**Punto de control:** lista de ajustes al kit. Pregunta clave: ¿el pensador razona como Adrián?

Nota: coop es Python, Aurora y FastAPI, mientras que el kit nació de proyectos en TypeScript y DynamoDB. Es una
buena prueba de que los principios no están atados a un stack. Las convenciones del `CLAUDE.md` de cada repo
mandan sobre las generales del kit.

## Fase 3 · Ajustes y segundo piloto (2-6 nov)

- [ ] Corregir principios, skills y agentes con lo aprendido (kit v0.5).
- [ ] Revisar la elección de modelo de cada agente según calidad y coste.
- [ ] Segundo piloto corto en garage-backend (TypeScript y DynamoDB), para cubrir el stack de Dathum.
- [ ] Resolver los **[CONFIRMAR]** que queden en los principios.
- [ ] **Una tarea web con el kit** (por ejemplo en coop-investment-fund-web). La comparativa con Kimi y Grok
      (13 oct) no sabe cuánto de los buenos resultados es del kit y cuánto de la suite de tests del backend.
- [ ] **El kit como revisor de PR ajenas:** que `revisor` revise una PR de Claude (por ejemplo, el PR 10 de la
      película). En la #86 encontró un fallo en código de Claude que nadie había visto.
- [x] **Menos consumo, grupo A** (14 oct, `kit-agentes-consumo/propuestas.md`): un implementador nuevo por
      vuelta, informes de cada agente en fichero, principios partidos por tema y solo la sección del diseño que
      toca, salidas cortas, esfuerzo por agente, retomar con `/clear` tras esperas largas y sin MCP en los
      agentes que no lo usan.
- [ ] **Menos consumo, grupo B, en prueba en la próxima tarea:** orquestador en Sonnet
      (`claude --model sonnet --plugin-dir ...`), revisor sin repetir las suites largas y re-revisión sobre el
      delta. Comparar coste por agente, contexto medio por llamada y calidad con los dos pilotos (sección 3 de
      `propuestas.md`). Si la calidad baja, se quita lo que la baje.
- [x] **Menos esperas:** en la #88, la mitad de la sesión fue esperar a Adrián. Decidido el 14 oct: los agentes
      siguen preguntando siempre que algo los bloquee.

**Punto de control:** dos tareas seguidas sin correcciones de fondo de Adrián.

## Fase 4 · Preparación para Dathum (9-20 nov)

- [ ] **Legal (bloqueante para cobrar):** revisar el contrato de Keepler/Accenture cuando llegue
      (exclusividad, no competencia, conflicto de interés, propiedad intelectual).
- [ ] Llevar el flujo a GitLab: merge requests con el MCP de GitLab o con `glab`, y pipeline de GitLab CI.
- [ ] Rol de solo lectura en la cuenta de Dathum, entre cuentas y con ExternalId.
- [ ] `CLAUDE.md` del kit en un repo de Dathum.
- [ ] **Perfil de cliente por ficheros** (ver `ideas/producto.md`): `~/work/clientes/dathum/` con las
      herramientas de cada agente (documentación en Outline con API key, tareas en su tablero de GitLab con
      `glab`, incidencias en su app propia) y su `.mcp.json`. El orquestador lo lee en el paso 0. Secretos solo
      en variables de entorno o en el llavero.
- [ ] Poder usar el kit desde el portátil de la empresa.
- [ ] Definir con Dathum los casos de uso, la forma de trabajo y el precio (cuota mensual o bolsa de horas).
      Las herramientas van a cargo de Dathum.

**Punto de control:** acuerdo firmado con Dathum y vía libre legal.

## Fase 5 · Piloto con Dathum (23 nov - 18 dic)

- [ ] Un mes con 2 o 3 casos de uso, incluido al menos un diseño completo.
- [ ] Informes periódicos de seguridad, costes y novedades.
- [ ] Medir horas ahorradas, hallazgos y correcciones, y ajustar el precio.

**Punto de control:** Dathum decide si continúa y con qué alcance.

## Fase 6 · Producto para otros clientes (enero 2027)

- [ ] Perfil por cliente (el de la fase 4) con stack, cuentas, repos, contactos y herramientas.
- [ ] Oferta tipo y caso de éxito de Dathum (con su permiso). Primer dato que se puede usar: la comparativa
      del 13 oct (0 fallos en 2 PR, 1,65 líneas de test por línea de código, 100 % Conventional Commits, el
      único que da su coste), con la reserva de que son solo 2 PR.
- [ ] Elegir herramienta y producir vídeos con el agente `video`.
- [ ] Guía de alta de un cliente nuevo.

## Fase 7 · Plataforma multiempresa (2027, solo si hay más clientes)

Detalle y términos de uso en `ideas/producto.md`.

- [ ] **Legal antes de empezar:** que el contrato con Keepler/Accenture permita un producto propio.
- [ ] Backend serverless: organizaciones, configuración por agente y secretos de cada cliente en Secrets
      Manager con KMS, más auditoría.
- [ ] **Ejecución remota:** un contenedor por tarea que clona los repos del cliente con un token de alcance
      mínimo y corre el kit. El modelo lo paga el cliente con su API key o con Bedrock en su cuenta (rol entre
      cuentas). **Nunca con su suscripción de Claude: los términos de Anthropic lo prohíben.**
- [ ] Aprobaciones desde la web o el chat.
- [ ] **Métricas e insights centralizados:** cada tarea guarda sola su coste exacto (sale de la respuesta de la
      API), tiempos, vueltas de revisión y correcciones de Adrián. Panel por cliente y por agente para ajustar
      modelos, precios y principios.

## Fase 8 · Frontend y pagos (después de la fase 7)

- [ ] Frontend para el alta, la configuración, las tareas y las aprobaciones.
- [ ] Stripe Billing con cuota por organización o por tarea. Se cobra el servicio, nunca los tokens.

---

## Riesgos

| Riesgo | Mitigación |
|---|---|
| El contrato con Keepler/Accenture lo impide o lo limita | Revisarlo antes de cobrar; mientras tanto, el trabajo es sobre proyectos propios. |
| Los agentes no razonan como Adrián | Los pilotos de las fases 2 y 3 sirven para medirlo antes de llegar a Dathum. |
| 2 h/día no alcanzan para revisar todo | El orquestador concentra las decisiones en dos aprobaciones por tarea; medir el tiempo real en los pilotos. |
| Coste de tokens alto | Medirlo en los pilotos y ajustar el modelo de cada agente; lo paga Dathum. |
| Términos de Anthropic al ejecutar para clientes | Solo la API key o el proveedor de nube del cliente; nunca su suscripción de Claude. |
| Custodiar credenciales y código de clientes en una plataforma | Credenciales de alcance mínimo y que caducan, KMS por cliente, contenedores efímeros y auditoría. |
| Datos sensibles del cliente | Acceso de solo lectura, nada se despliega sin Adrián, y sin secretos en prompts ni logs. |
