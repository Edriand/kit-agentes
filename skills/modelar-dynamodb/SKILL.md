---
name: modelar-dynamodb
description: Diseñar o revisar un modelo de datos en DynamoDB partiendo de los patrones de acceso, con el criterio de Adrián. Usar cuando pidan modelar datos, añadir entidades o índices, o decidir entre DynamoDB y una base relacional.
---

# Modelar datos en DynamoDB

1. Lee `principios/5-datos.md` del kit y el `docs/data-model.md` del repo si existe.
2. Antes de nada, decide si DynamoDB es la herramienta correcta. Si hace falta orden global, consultas de
   agregación complejas o aislamiento por fila, propón Aurora Serverless v2 y explica por qué.
3. Escribe la tabla de patrones de acceso (patrón | PK | SK | índice) antes de definir ningún item.
4. Puedes usar el MCP `dynamodb` (herramienta de modelado) como apoyo, pero la decisión final sigue los
   principios del kit.
5. Define cada tipo de item con sus atributos, qué se deriva en lugar de guardarse y qué reglas de negocio se
   validan en el backend.
6. Todos los items llevan `createdAt` y `updatedAt`. Comprueba que cada listado se puede consultar de más nuevo a
   más antiguo y al revés (fecha o ULID en la SK o en la SK de un GSI).
7. Single-table o una tabla por entidad: no hay estándar; justifica la elección con los patrones de acceso.
8. Configuración fija: bajo demanda, PITR activado, borrado `RETAIN` en `pro`.
9. Si añades más de un GSI a una tabla existente, avisa de que hay que desplegarlos de uno en uno.
10. Entrega el resultado en el formato de `docs/data-model.md`.
