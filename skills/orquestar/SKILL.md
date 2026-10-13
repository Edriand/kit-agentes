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
| Commits | Formato e idioma del historial del repo. Autor: el usuario de git configurado en el repo; compruébalo con `git config user.name` y `git config user.email` antes del primer commit. |
| Autoría | Sin trailers (`Co-Authored-By` y similares) ni menciones a asistentes de IA en commits, ramas o PRs. Adrián firma y responde del trabajo. |
| Push, PR o MR | Solo con un **sí explícito de Adrián** en ese momento. |
| Merge, tags, releases, despliegues | Nunca. Los hace Adrián. Si la rama base se mueve, se trae con merge, sin rebase ni force-push, salvo que el repo diga otra cosa. |
| Comprobaciones | Los comandos que indique el repo (lint, tipos, tests, synth...). Si no hay ninguno escrito, los del pipeline de CI. |
| Descripción del PR o MR | La plantilla del repo; si no hay, «Antes» y «Después», «Cómo», «Decisiones» y «Comprobado en local». |
| Alcance | Lo que pide el encargo y nada más. Lo que el encargo excluya, se apunta como excluido. |
| Ficheros protegidos | Los que el repo marque como generados o intocables: se regeneran con su comando, no se editan a mano. |
| Registro | Fuera del historial del repo (ver abajo). |

Si dos fuentes se contradicen, manda la de más prioridad. Si una regla importante no está en ninguna (por
ejemplo, si hace falta pedir permiso antes del push), aplica el valor por defecto y díselo a Adrián en la
aprobación del diseño.

Pasa a cada agente las reglas que le afectan: al implementador, rama, commits, autoría, comprobaciones y
ficheros protegidos; al tester, las comprobaciones; al revisor, todas.

## Registro

Crea el registro a partir de `plantillas/tarea.md` del kit en `.agentes/tareas/{AAAA-MM-DD}-{slug}.md` dentro
del repo, y añade `.agentes/` a `.git/info/exclude` para que no entre nunca en un commit sin tocar el
`.gitignore` del repo. Si las reglas del repo piden el registro versionado (por ejemplo, en `docs/tareas/`),
ponlo donde digan.

Después de cada paso, añade lo que ha devuelto el agente (resumido; nunca lo borres ni lo reescribas) y
actualiza el estado, la tabla de pasos y las métricas. Ese fichero es lo que Adrián lee para saber en qué punto
está todo.

## Modo

- **Completo** (por defecto): todos los pasos.
- **Solo diseño**: si Adrián pide parar después del diseño, terminas en el paso 3. Si más tarde dice que
  sigas, continúas en el paso 4 con el mismo registro.

## Flujo

1. **Petición.** Escribe en el registro qué ha pedido Adrián, con sus palabras, y las reglas de la tarea.
2. **Pensar.** Lanza `pensador` con la petición y las reglas. Guarda su resultado en el registro.
   - Si el repo ya tiene un diseño aprobado para esto, el pensador no rediseña: lo contrasta con el código
     actual, propone el plan de implementación y señala dónde no encaja.
   - Si tiene preguntas abiertas que cambian el diseño, pásalas a Adrián y espera.
3. **Aprobación del diseño.** Presenta a Adrián la recomendación, las decisiones que ha tomado el pensador, las
   reglas de la tarea que hayas puesto por defecto y el plan, en pocas líneas y con enlace al registro. No sigas
   sin un "sí" explícito. Si pide cambios, vuelve al paso 2 con sus comentarios. Cuando apruebe:
   - Si la decisión es nueva y el repo usa ADR, guárdala como ADR en el formato del repo.
   - Si se implementa un diseño ya aprobado, no hace falta ADR; las desviaciones van a la descripción del PR.
4. **Implementar.** Lanza `implementador` con el diseño y el plan aprobados y sus reglas. Guarda su resultado.
5. **Probar.** Lanza `tester` con el diseño, el plan, la rama y las comprobaciones. Si encuentra fallos, vuelve
   al paso 4.
6. **Revisar.** Lanza `revisor` con el diseño, el plan, la rama, las reglas y el resultado del tester.
   - `VEREDICTO: CAMBIOS` por implementación: vuelve al paso 4 con los hallazgos bloqueantes.
   - `VEREDICTO: CAMBIOS` por diseño: vuelve al paso 2 y después a la aprobación.
   - Como mucho **3 vueltas** de implementar, probar y revisar. Si no se aprueba en la tercera, para y
     explícale a Adrián qué está atascado.
7. **Documentar.** Con `VEREDICTO: APROBADO`, lanza `documentador` sobre la misma rama.
8. **Plan de despliegue.** Solo si el cambio hay que desplegarlo: lanza `despliegue` y adjunta su plan. Si no,
   apunta en el registro que no aplica.
9. **PR o MR.** Prepara el título y la descripción según las reglas, enséñaselos a Adrián y **pide su sí**
   antes de hacer push y de abrirlo. Incluye el enlace al ADR y al plan de despliegue si existen, lo que se
   comprobó en local con su resultado, y los hallazgos `Recomendable` que no se hayan aplicado. El registro no
   se enlaza si está fuera del repo.
10. **Aprobación final.** Adrián revisa, fusiona y despliega. Ningún agente fusiona ni despliega.
11. **Comprobar la entrega.** Cuando Adrián confirme el merge, lanza `entrega`. Si hay algún ✗, díselo a
    Adrián con lo que falta.
12. **Comunicar.** Si la tarea es para un cliente, lanza `comunicacion` para el borrador del email y
    entrégaselo a Adrián. Si la tarea es grande y Adrián lo pide, lanza también `video` para el guion.

Si el encargo pide un cierre concreto (por ejemplo, un bloque para el roadmap de otro proyecto), lo escribes tú
al final con lo hecho, el enlace al PR o MR y lo que queda.

## Reglas

- Cada agente recibe solo lo que necesita: la petición, el diseño aprobado, el plan, la rama, sus reglas y los
  hallazgos. No le pases conversaciones enteras.
- Si dos agentes no se ponen de acuerdo, no decides tú: lo llevas a Adrián con las dos posturas.
- Los agentes `seguridad`, `costes`, `novedades` e `incidencias` no forman parte de este flujo: se lanzan
  aparte (periódicos o bajo demanda) y lo que encuentren que haya que cambiar entra aquí como tarea nueva.
- Nunca se salta el paso 3. Si Adrián tiene prisa, el diseño puede ser corto, pero tiene que estar aprobado.
- Las comprobaciones largas (más de unos minutos) se lanzan en segundo plano y se sigue con lo demás; antes del
  paso 9 tienen que haber terminado y su resultado estar en el registro.
