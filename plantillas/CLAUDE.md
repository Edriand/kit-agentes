# {Nombre del proyecto}

{Una línea: qué hace este backend y para quién.}

Este repo lo trabajan agentes con el kit de Adrián. Antes de diseñar o cambiar infraestructura, aplica
`principios/principios-diseno.md` del kit y las skills `disenar-arquitectura`, `disenar-api`,
`modelar-dynamodb` y `revisar-cdk`.

## Stack

- IaC: AWS CDK v2 ({TypeScript | Python})
- Cómputo: Lambda ({runtime}, ARM64)
- API: API Gateway ({HTTP API | REST API}) con Cognito
- Datos: {DynamoDB | Aurora Serverless v2}
- Región: eu-west-1

## Documentación

- `docs/architecture.md`: servicios y flujo.
- `docs/api.md`: endpoints.
- `docs/data-model.md`: patrones de acceso e items.
- `docs/adr/`: decisiones.

## Comandos

```bash
npm run build
npx cdk synth -c env=dev
npx cdk diff -c env=dev
```

## Convenciones

- Nombres: `{proyecto}-{entorno}-{servicio}-{nombre}` con `buildResourceName()`.
- Entornos: `dev` y `pro` en `config/environments.ts`.
- Handlers: `lambda/{recurso}/{acción}.ts`.

## Reglas para agentes

- Los agentes proponen y Adrián aprueba. Nunca se despliega a `pro` desde un agente.
- Todo cambio llega como merge request con descripción y, si cambia el diseño, un ADR.
- Acceso a AWS solo con el rol de solo lectura.

## Restricciones conocidas

- {Ej.: DynamoDB solo admite crear un GSI por actualización de CloudFormation.}
