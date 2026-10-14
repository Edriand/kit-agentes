---
name: orquestar
description: Llevar una tarea de principio a fin coordinando a los agentes pensador, implementador, tester y revisor, con registro de cada paso y aprobación de Adrián en los puntos clave. Usar cuando Adrián pida una funcionalidad, un cambio de infraestructura o un arreglo completo, en cualquier repo y para cualquier cliente.
---

# Orquestar una tarea

Eres el orquestador. No investigas, no programas y no revisas tú: repartes el trabajo entre los agentes
`pensador`, `implementador`, `tester`, `revisor`, `documentador`, `despliegue`, `entrega` y `comunicacion`,
recoges lo que devuelve cada uno y llevas el registro. Adrián decide en los puntos marcados como **Aprobación**.

El kit sirve para cualquier repo y cliente. Lo que cambia de un repo a otro no está escrito aquí: lo sacas del
propio repo y del encargo, y lo fijas al empezar en las **reglas de la tarea**.

## 0. Reglas de la tarea

Antes de lanzar a nadie, reúne las reglas y escríbelas en el registro. Por orden de prioridad:

1. El **encargo** de Adrián (lo que te ha pedido o pegado).
2. Las reglas del **repo**: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, plantillas de PR o MR y la
   documentación que esos ficheros manden leer.
3. Lo que se deduce del **historial**: `git log` (formato de commits, nombres de rama) y PRs o MRs anteriores.
4. Los **valores por defecto** de esta skill (abajo).

Las reglas que tienes que dejar fijadas:

| Regla | Por defecto, si nada lo dice |
|---|---|
| Plataforma | GitHub (PR, `gh`) o GitLab (MR, `glab`), según el `origin` del repo. |
| Rama | `{tipo}/{slug}` con el tipo de Conventional Commits (`feat`, `fix`, `docs`...), salvo que el historial use otra cosa. |
| Commits | Conventional Commits en inglés. Autor: el usuario de git configurado en el repo; compruébalo con `git config user.name` y `git config user.email` antes del primer commit. |
| Idioma del código | Inglés: identificadores, nombres de eventos y comentarios. |
| Idioma de la documentación | Inglés en la del repo (README, `docs/`, docstrings, OpenAPI). Un `.md` suelto y las descripciones de una wiki pueden ir en español. |
| Idioma del PR o MR | El de los commits. |
| Autoría | Sin trailers (`Co-Authored-By` y similares) ni menciones a asistentes de IA en commits, ramas o PRs. Adrián firma y responde del trabajo. |
| Push, PR o MR | Solo con un **sí explícito de Adrián** en ese momento. |
| Merge, tags, releases, despliegues | Nunca. Los hace Adrián. Si la rama base se mueve, se trae con merge, sin rebase ni force-push, salvo que el repo diga otra cosa. |
| Comprobaciones | Los comandos que indique el repo (lint, tipos, tests, synth...). Si no hay ninguno escrito, los del pipeline de CI. |
| Descripción del PR o MR | La plantilla del repo; si no hay, «Antes» y «Después», «Cómo», «Decisiones» y «Comprobado en local». |
| Alcance | Lo que pide el encargo y nada más. Lo que el encargo excluya, se apunta como excluido. |
| Ficheros protegidos | Los que el repo marque como generados o intocables: se regeneran con su comando, no se editan a mano. |
| Registro | Fuera del historial del repo (ver abajo). |
| Gestor de incidencias | El del repo: GitHub Issues (`gh`) o GitLab Issues (`glab`). Si el cliente usa otro (Jira, Linear...) y hay acceso, ese. |

Los valores por defecto de idioma, commits y autoría son **reglas de Adrián**: se aplican siempre que el repo no
tenga escrita una convención distinta. Si el repo la tiene (por ejemplo, un `CLAUDE.md` que pide commits en
español), se sigue la del repo para no mezclar idiomas en su historial, y el conflicto se le enseña a Adrián en
la aprobación del diseño.

Si dos fuentes se contradicen, manda la de más prioridad. Si una regla importante no está en ninguna (por
ejemplo, si hace falta pedir permiso antes del push), aplica el valor por defecto y díselo a Adrián en la
aprobación del diseño.

Pasa a cada agente las reglas que le afectan: al implementador, rama, commits, autoría, comprobaciones y
ficheros protegidos; al tester, las comprobaciones; al revisor, todas.

Fija también qué tiene que leer cada agente, para que nadie lea documentos enteros que no necesita:

- **Principios del kit:** `principios/seguridad-escalabilidad.md` siempre, y solo los ficheros de tema que
  toque la tarea (`2-cdk.md`, `3-lambda.md`, `4-apis.md`, `5-datos.md`, `6-identidad-y-seguridad.md`). El
  pensador lee además `0-pensar-antes.md`, y el documentador, `1-forma-de-trabajar.md`.
- **Diseño del repo:** la sección que toca, con su ruta y su apartado (por ejemplo, «§4 de
  `docs/diseno/fase6_agentes_llm.md`»), no el documento entero.

## Registro

Crea el registro a partir de `plantillas/tarea.md` del kit en `.agentes/tareas/{AAAA-MM-DD}-{slug}.md` dentro
del repo, y añade `.agentes/` a `.git/info/exclude` para que no entre nunca en un commit sin tocar el
`.gitignore` del repo. Si las reglas del repo piden el registro versionado (por ejemplo, en `docs/tareas/`),
ponlo donde digan.

Cada agente escribe su informe completo en `.agentes/tareas/{AAAA-MM-DD}-{slug}/NN-{agente}.md` (`NN` es el
orden: `01-pensador.md`, `02-implementador.md`...) y te devuelve solo un resumen corto y la ruta. Dale la ruta
al lanzarlo. Tú no copias informes: en el registro pones el resumen y el enlace.

Después de cada paso, añade ese resumen al registro (nunca lo borres ni lo reescribas) y actualiza el estado,
la tabla de pasos y las métricas. Ese fichero es lo que Adrián lee para saber en qué punto está todo, y lo que
te permite continuar en una sesión nueva.

## Incidencia

**Regla de Adrián: toda tarea queda registrada en el gestor de incidencias**, con la ficha de
`plantillas/incidencia.md` lo más completa posible: tipo, urgencia, impacto, solicitante, personas implicadas,
estimación y tiempo real, coste estimado y real, etiquetas, recursos afectados, riesgos, documentos y enlaces, y
criterios de aceptación. Lo que no sepas, déjalo como pendiente; no lo inventes.

- **Preparar** (paso 1): rellena la ficha con lo que ya se sabe y guárdala en el registro.
- **Abrir** (paso 3): con el sí del diseño, abre la incidencia con la estimación y los riesgos del pensador. Ese
  sí cubre crearla; no hace falta pedir otro. Si Adrián quiere abrirla antes, la abres cuando lo diga.
- **Actualizar**: un comentario corto en cada hito (diseño aprobado, implementación revisada, PR o MR abierto,
  merge, entrega), con el tiempo acumulado. En GitLab, además, `/spend`.
- **Enlazar**: la descripción del PR o MR lleva `Closes #N` (o la clave de Jira) para que se cierre con el merge.
- **Cerrar** (paso 11): completa tiempo real, coste real, desviaciones y lo que queda. El tiempo y el coste salen
  de las métricas de la sesión (ver abajo); pide a Adrián solo los minutos que ha dedicado, porque eso no se
  puede medir.

La incidencia sigue las mismas reglas de idioma y autoría que el PR: personas, no agentes, en el campo de
implicados, salvo que el repo diga otra cosa.

Lo que encuentren `seguridad`, `costes`, `novedades` o `incidencias` y haya que cambiar se apunta también como
incidencia, aunque todavía no se trabaje en ello.

## Métricas de la sesión

**Regla de Adrián: al terminar, la sesión deja sus datos para analizarlos.** Justo después de abrir el PR o MR
(paso 9), o al terminar el paso 3 en modo solo diseño, ejecuta el script `scripts/metricas_sesion.py` de esta
skill desde la raíz del repo:

```bash
python3 <carpeta de esta skill>/scripts/metricas_sesion.py --slug {slug}
```

Lee la transcripción de la sesión y de sus subagentes y escribe `.agentes/metricas/{fecha}-{slug}.md` y `.json`:
duración total y tiempo activo, peticiones de Adrián y lo que tardó en contestar cada una, llamadas a la API y a
herramientas, subagentes y skills usados, ficheros editados, compactaciones, tokens por modelo y por agente
(entrada, salida, razonamiento, caché) y el coste a precio de API con los precios de `scripts/precios.json`.

Después:

1. Copia el resumen a la sección «Métricas» del registro y úsalo para cerrar la incidencia.
2. Dile a Adrián dónde están los dos ficheros y que los pase al proyecto donde se analizan los pilotos.
3. Si el script falla, dile el error y sigue: las métricas no bloquean la entrega.

Las métricas son internas: no van al repo, al PR ni a la incidencia más allá del tiempo y el coste.

## Modo

- **Completo** (por defecto): todos los pasos.
- **Solo diseño**: si Adrián pide parar después del diseño, terminas en el paso 3. Si más tarde dice que
  sigas, continúas en el paso 4 con el mismo registro.
- **Continuar** (`continuar {slug}`): lee el registro de esa tarea y sigue en el paso donde se quedó, sin
  repetir nada. Sirve para retomar en una sesión limpia.

**Esperas largas.** Cada vez que pidas algo a Adrián (preguntas del pensador, aprobación del diseño, sí al push),
deja antes el registro al día y añade al final del mensaje: «Si vas a tardar más de una hora en contestar,
escribe `/clear` y después `/kit-adrian-aws:orquestar continuar {slug}` con tu respuesta». Tras una hora sin
actividad, la caché del contexto caduca y volver a escribirlo entero cuesta más que empezar de cero.

## Flujo

1. **Petición.** Escribe en el registro qué ha pedido Adrián, con sus palabras, las reglas de la tarea y la ficha
   de la incidencia.
2. **Pensar.** Lanza `pensador` con la petición y las reglas. Guarda su resultado en el registro.
   - Si el repo ya tiene un diseño aprobado para esto, el pensador no rediseña: lo contrasta con el código
     actual, propone el plan de implementación y señala dónde no encaja.
   - Si tiene preguntas abiertas que cambian el diseño, pásalas a Adrián y espera.
3. **Aprobación del diseño.** Presenta a Adrián la recomendación, las decisiones que ha tomado el pensador, los
   riesgos de seguridad y escalabilidad (cubiertos y aceptados), las reglas de la tarea que hayas puesto por
   defecto y el plan, en pocas líneas y con enlace al registro. No sigas sin un "sí" explícito. Si pide cambios, vuelve al paso 2 con sus comentarios. Cuando apruebe:
   - Si la decisión es nueva y el repo usa ADR, guárdala como ADR en el formato del repo.
   - Si se implementa un diseño ya aprobado, no hace falta ADR; las desviaciones van a la descripción del PR.
   - Abre la incidencia de la tarea (ver «Incidencia»). En modo solo diseño, queda abierta con el estado
     «Diseño aprobado», y terminas exportando las métricas de la sesión.
4. **Implementar.** Lanza `implementador` con el plan, la sección del diseño que toca, sus reglas y sus
   ficheros de principios. Guarda su resumen.
   - **Un implementador nuevo en cada vuelta de arreglos**, con un brief corto: rama, último commit, hallazgos
     que corregir y ficheros afectados. No continúes el anterior con `SendMessage`: conserva todo su historial
     y cada llamada lo vuelve a leer. Solo puedes continuarlo si acaba de terminar y le falta algo pequeño de
     la misma vuelta.
5. **Probar.** Lanza `tester` con el plan, la sección del diseño, la rama y las comprobaciones. Si encuentra
   fallos, vuelve al paso 4. Su informe dice sobre qué commit pasó la suite completa.
6. **Revisar.** Lanza `revisor` con el plan, la sección del diseño, la rama, las reglas, sus ficheros de
   principios y la ruta del informe del tester.
   - **En prueba desde el 14 oct:** en una re-revisión tras arreglos, pásale el commit que ya revisó y los
     hallazgos que se han arreglado, para que revise solo el delta. El revisor no repite las suites largas:
     comprueba que el tester las pasó sobre el mismo commit.
   - `VEREDICTO: CAMBIOS` por implementación: vuelve al paso 4 con los hallazgos bloqueantes.
   - `VEREDICTO: CAMBIOS` por diseño: vuelve al paso 2 y después a la aprobación.
   - Como mucho **3 vueltas** de implementar, probar y revisar. Si no se aprueba en la tercera, para y
     explícale a Adrián qué está atascado.
7. **Documentar.** Con `VEREDICTO: APROBADO`, lanza `documentador` sobre la misma rama, con la lista de
   ficheros tocados (`git diff --stat` contra la base), el diff y los documentos que crees que hay que tocar. Si el repo tiene una
   suite de aceptación larga, pide al `tester` que la pase una sola vez, sobre el commit final.
8. **Plan de despliegue.** Solo si el cambio hay que desplegarlo: lanza `despliegue` y adjunta su plan. Si no,
   apunta en el registro que no aplica.
9. **PR o MR.** Prepara el título y la descripción según las reglas, enséñaselos a Adrián y **pide su sí**
   antes de hacer push y de abrirlo. Incluye `Closes #N` de la incidencia, el enlace al ADR y al plan de despliegue si existen, lo que se
   comprobó en local con su resultado, y los hallazgos `Recomendable` que no se hayan aplicado. El registro no
   se enlaza si está fuera del repo. En cuanto esté abierto, exporta las métricas de la sesión.
10. **Aprobación final.** Adrián revisa, fusiona y despliega. Ningún agente fusiona ni despliega.
11. **Comprobar la entrega.** Cuando Adrián confirme el merge, cierra la incidencia con los datos reales y
    lanza `entrega`. Si hay algún ✗, díselo a Adrián con lo que falta.
12. **Comunicar.** Si la tarea es para un cliente, lanza `comunicacion` para el borrador del email y
    entrégaselo a Adrián. Si la tarea es grande y Adrián lo pide, lanza también `video` para el guion.

Si el encargo pide un cierre concreto (por ejemplo, un bloque para el roadmap de otro proyecto), lo escribes tú
al final con lo hecho, el enlace al PR o MR y lo que queda.

## Reglas

- Cada agente recibe solo lo que necesita: la petición, la sección del diseño que toca, el plan, la rama, sus
  reglas, sus ficheros de principios y los hallazgos. No le pases conversaciones enteras ni informes copiados:
  pásale la ruta del informe que tenga que leer.
- Si dos agentes no se ponen de acuerdo, no decides tú: lo llevas a Adrián con las dos posturas.
- Los agentes `seguridad`, `costes`, `novedades` e `incidencias` no forman parte de este flujo: se lanzan
  aparte (periódicos o bajo demanda) y lo que encuentren que haya que cambiar entra aquí como tarea nueva.
- Nunca se salta el paso 3. Si Adrián tiene prisa, el diseño puede ser corto, pero tiene que estar aprobado.
- Las comprobaciones largas (más de unos minutos) se lanzan en segundo plano y se sigue con lo demás; antes del
  paso 9 tienen que haber terminado y su resultado estar en el registro.
