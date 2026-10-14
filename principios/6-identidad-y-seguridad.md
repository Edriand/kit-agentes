# 6. Identidad y seguridad

- **Cognito User Pool**: login con email, verificación por email, recuperación solo por email,
  `preventUserExistenceErrors`, revocación de tokens, tokens de acceso de 1 h y de refresco de 30 días, emails
  enviados con SES desde dominio propio. Plan *Essentials* con OTP por email como primer factor.
- **Clientes sin secreto** para web/móvil y sin flujos OAuth si no hacen falta.
- **Secretos en Secrets Manager**, nunca en variables de entorno en claro. CDK crea el contenedor; el valor se
  carga a mano después del despliegue y el procedimiento queda documentado.
- **Credenciales de terceros de los usuarios cifradas con KMS** (envelope encryption con contexto `user_id`);
  nunca se devuelven por la API ni aparecen en logs.
- **Las acciones irreversibles o de dinero las confirma una persona**, nunca un agente ni una key.
- **Observabilidad**: logs de acceso del API, X-Ray en el API, alarmas de tasa de error y latencia p99.
- **WAF con las reglas básicas recomendadas por AWS** como punto de partida:
  - `AWSManagedRulesCommonRuleSet` (riesgos OWASP habituales).
  - `AWSManagedRulesKnownBadInputsRuleSet`.
  - `AWSManagedRulesAmazonIpReputationList`.
  - Una regla de límite de peticiones por IP (rate-based).
  - `AWSManagedRulesSQLiRuleSet` si hay base de datos SQL detrás.
  - Primero en modo `Count` para ver falsos positivos, después en `Block`.
  - Si el WAF protege una distribución de CloudFront, se crea en `us-east-1` (scope `CLOUDFRONT`).
