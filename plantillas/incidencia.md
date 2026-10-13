# Plantilla de la incidencia de cada tarea

Toda tarea queda registrada en el gestor de incidencias del cliente con esta ficha. El orquestador la abre, la
mantiene al día en cada hito y la cierra con los datos reales. El idioma es el de la documentación del repo.

## Título

`{tipo}: {qué se consigue}`, en el idioma de los commits. Ej.: `feat: Research con LLM e informe de mercado`.

## Cuerpo

```markdown
## Petición
{Qué se pidió, con las palabras del solicitante, y por qué.}

## Ficha

| Campo | Valor |
|---|---|
| Cliente y proyecto | {cliente} · {repo} |
| Tipo | {funcionalidad, error, infraestructura, seguridad, coste, documentación, diseño} |
| Urgencia | {crítica, alta, media, baja}, y por qué |
| Impacto | {a quién afecta y cuánto} |
| Solicitante | {persona} |
| Responsable | {Adrián} |
| Personas implicadas | {quién revisa, quién aprueba, a quién hay que avisar} |
| Fecha de inicio | {AAAA-MM-DD} |
| Fecha límite | {AAAA-MM-DD o "sin fecha"} |
| Estimación | {horas totales} (de ellas, {horas de Adrián}) |
| Tiempo real | {se rellena al cerrar} |
| Coste estimado | {herramientas en USD; impacto mensual en la nube si cambia infraestructura} |
| Coste real | {se rellena al cerrar} |
| Recursos afectados | {servicios, stacks, tablas, endpoints, ficheros principales} |
| Riesgos | {lo que puede salir mal y qué no tiene marcha atrás} |

## Documentos y enlaces
- Diseño: {enlace}
- ADR: {enlace o "no aplica"}
- Rama: {rama}
- PR o MR: {enlace}
- Plan de despliegue: {enlace o "no aplica"}
- Otros: {diagramas, tickets relacionados, documentación externa}

## Criterios de aceptación
- [ ] {lo que tiene que ser verdad para dar la tarea por hecha}

## Cierre
{Se rellena al cerrar: qué se hizo, tiempo y coste reales, desviaciones respecto a la estimación y por qué,
vueltas de revisión y lo que queda pendiente.}
```

## Cómo se guarda cada campo según el gestor

| Campo | GitHub Issues | GitLab Issues | Jira o Linear |
|---|---|---|---|
| Tipo, urgencia, área | Etiquetas `tipo:…`, `urgencia:…`, `area:…` | Etiquetas con ámbito `tipo::…`, `urgencia::…`, `area::…` | Tipo de incidencia, prioridad y componentes |
| Responsable | Asignado | Asignado | Responsable |
| Fecha límite | Hito, o la ficha si no hay hitos | `/due` | Fecha de vencimiento |
| Estimación | Ficha y, si el repo tiene un Project, su campo numérico | `/estimate` | Estimación original |
| Tiempo real | Ficha y comentario de cierre | `/spend` en cada hito | Registro de trabajo |
| Hitos de la tarea | Un comentario por hito | Un comentario por hito | Un comentario por hito |
| Enlace con el PR o MR | `Closes #N` en la descripción del PR | `Closes #N` en la descripción del MR | Clave de la incidencia en la rama y el título |

Si una etiqueta no existe, se crea con el mismo esquema (`gh label create` o `glab label create`). Si no hay
gestor accesible, la ficha se queda en el registro de la tarea y se avisa a Adrián.
