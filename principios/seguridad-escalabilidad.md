# Seguridad y escalabilidad, siempre

Regla de Adrián (2026-10-13): todo agente que diseña, implementa, prueba o revisa piensa en la seguridad y la
escalabilidad de lo que hace, aunque la tarea no lo mencione. Sirve para cualquier repo y cualquier tecnología;
`5-datos.md` y `6-identidad-y-seguridad.md` concretan cómo se aplica en AWS.

- **Seguridad.** Quién puede usar esto y con qué permisos (mínimo privilegio). Qué entradas acepta y cómo se
  validan (inyección, tamaños, tipos). Qué datos sensibles maneja y dónde pueden acabar (logs, errores,
  respuestas, prompts de un LLM). Secretos fuera del código y del repo. Aislamiento entre usuarios, clientes o
  entornos. Dependencias nuevas (mantenidas, versión fijada). Qué pasa si alguien lo usa mal (abuso, límites,
  coste disparado).
- **Escalabilidad.** Qué pasa con 10 y con 100 veces el volumen de hoy (datos, peticiones, usuarios). Límites y
  cuotas del servicio (concurrencia, timeouts, tamaño de payload, throughput, conexiones a la base de datos).
  Patrones que no escalan: scans o consultas sin índice, N+1, una llamada remota por elemento, listas sin
  paginar, cargar todo en memoria, particiones calientes. Reintentos e idempotencia. Cómo crece el coste.
- **Proporcional al cambio.** Un script interno no necesita lo mismo que una API pública. Si un punto no aplica,
  se dice en una línea; no se omite en silencio.
- **Lo que se deja fuera a propósito se escribe como riesgo aceptado**, con el porqué, para que lo decida Adrián.
- El agente `seguridad` hace auditorías a fondo aparte; esta regla es el mínimo de cada tarea.
