# 1. Forma de trabajar

- **La documentación vive en el repo y es la fuente de verdad.** Cada proyecto tiene `CLAUDE.md` (convenciones,
  comandos, restricciones conocidas) y `docs/` con `architecture.md`, `api.md` y `data-model.md`.
- **Las decisiones se registran como ADR** en `docs/adr/NNNN-titulo.md` con *Decisión*, *Por qué* y
  *Consecuencias*. Si una decisión cambia, se escribe un ADR nuevo; no se reescribe el antiguo.
- **Los comentarios del código explican el porqué**, sobre todo cuando algo no es obvio o rompe una regla
  (ej.: por qué un recurso SES no lleva sufijo de entorno, por qué se dividió un stack).
- **Las restricciones de AWS aprendidas a base de golpes se documentan** en `CLAUDE.md` con el procedimiento
  exacto (ej.: un solo GSI por actualización de CloudFormation).
- **Idioma** (regla de Adrián, 13 oct 2026):
  - Todo el código en inglés: variables, funciones, clases, nombres de eventos y comentarios.
  - Commits con Conventional Commits, en inglés (`feat(api): add pagination to orders`).
  - Documentación del repo en inglés (README, `docs/`, docstrings, OpenAPI).
  - Excepciones: un `.md` suelto (notas, propuestas, documentos de trabajo) y las descripciones en una wiki
    pueden ir en español.
