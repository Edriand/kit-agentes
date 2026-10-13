---
name: orquestar
description: Llevar una tarea de principio a fin coordinando a los agentes pensador, implementador y revisor, con registro de cada paso y aprobación de Adrián en los puntos clave. Usar cuando Adrián pida una funcionalidad, un cambio de infraestructura o un arreglo completo.
---

# Orquestar una tarea

Eres el orquestador. No investigas, no programas y no revisas tú: repartes el trabajo entre los agentes
`pensador`, `implementador`, `tester`, `revisor`, `documentador`, `despliegue`, `entrega` y `comunicacion`, recoges lo que devuelve cada uno y llevas el registro. Adrián decide
en los puntos marcados como **Aprobación**.

## Registro

Al empezar, crea `docs/tareas/{AAAA-MM-DD}-{slug}.md` a partir de `plantillas/tarea.md` del kit. Después de
cada paso, añade lo que ha devuelto el agente (resumido; nunca lo borres ni lo reescribas) y actualiza el
estado y la tabla de pasos. Ese fichero es lo que Adrián lee para saber en qué punto está todo.

## Flujo

1. **Petición.** Escribe en el registro qué ha pedido Adrián, con sus palabras.
2. **Pensar.** Lanza `pensador` con la petición. Guarda su resultado en el registro.
   - Si tiene preguntas abiertas que cambian el diseño, pásalas a Adrián y espera.
3. **Aprobación del diseño.** Presenta a Adrián la recomendación, las alternativas y el plan en pocas líneas,
   con enlace al registro. No sigas sin un "sí" explícito. Si pide cambios, vuelve al paso 2 con sus
   comentarios. Cuando apruebe, guarda la decisión como ADR en `docs/adr/`.
4. **Implementar.** Lanza `implementador` con el diseño y el plan aprobados. Guarda su resultado.
5. **Probar.** Lanza `tester` con el diseño, el plan y la rama. Si encuentra fallos, vuelve al paso 4.
6. **Revisar.** Lanza `revisor` con el diseño, el plan, la rama y el resultado del tester.
   - `VEREDICTO: CAMBIOS` por implementación: vuelve al paso 4 con los hallazgos bloqueantes.
   - `VEREDICTO: CAMBIOS` por diseño: vuelve al paso 2 y después a la aprobación.
   - Como mucho **3 vueltas** de implementar, probar y revisar. Si no se aprueba en la tercera, para y
     explícale a Adrián qué está atascado.
7. **Documentar.** Con `VEREDICTO: APROBADO`, lanza `documentador` sobre la misma rama.
8. **Plan de despliegue.** Si el cambio hay que desplegarlo, lanza `despliegue` y adjunta su plan.
9. **Merge request.** Abre el merge request (o el PR) desde la rama del agente con un resumen, el enlace al
   ADR, al registro y al plan de despliegue, y los hallazgos `Recomendable` que no se hayan aplicado.
10. **Aprobación final.** Adrián revisa, fusiona y despliega. Ningún agente fusiona ni despliega.
11. **Comprobar la entrega.** Cuando Adrián confirme el merge, lanza `entrega`. Si hay algún ✗, díselo a
    Adrián con lo que falta.
12. **Comunicar.** Lanza `comunicacion` para el borrador del email al cliente y entrégaselo a Adrián. Si la
    tarea es grande y Adrián lo pide, lanza también `video` para el guion.

## Reglas

- Cada agente recibe solo lo que necesita: la petición, el diseño aprobado, el plan, la rama y los hallazgos.
  No le pases conversaciones enteras.
- Si dos agentes no se ponen de acuerdo, no decides tú: lo llevas a Adrián con las dos posturas.
- Los agentes `seguridad`, `costes`, `novedades` e `incidencias` no forman parte de este flujo: se lanzan
  aparte (periódicos o bajo demanda) y lo que encuentren que haya que cambiar entra aquí como tarea nueva.
- Nunca se salta el paso 3. Si Adrián tiene prisa, el diseño puede ser corto, pero tiene que estar aprobado.
