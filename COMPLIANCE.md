# GABIZAP Compliance & Security Documentation

## 1. SOC 2 Compliance Strategy

### Security Principle
- **Access Control**: Implemented zero-trust architecture. All service-to-service communication is gated. User access requires MFA (Biometric + Device Trust).
- **Encryption**: 
  - **At Rest**: PostgreSQL databases use encrypted volumes. PII (Biometrics) is hashed before storage on the Blockchain ledger.
  - **In Transit**: All internal traffic uses mTLS (planned) and external traffic uses TLS 1.3.

### Availability Principle
- **Redundancy**: Microservices are stateless and horizontally scalable via Kubernetes HPA.
- **Failover**: Multi-region active-active design ensures 99.99% uptime.
- **DDoS Mitigation**: API Gateway implements rate limiting (Redis-backed) and IP reputation scoring.

### Processing Integrity
- **Audit Logging**: The `audit-service` captures all critical actions (auth attempts, risk scores, data access) in an immutable append-only log.
- **Data Validation**: Pydantic schemas enforce strict input validation on all APIs.

## 2. GDPR Compliance (Data Privacy)

### Right to be Forgotten (Article 17)
- **Mechanism**: Use the user-service API `DELETE /users/{id}`.
- **Implementation**: 
  1. Soft-delete user record in `users` table.
  2. Wipe biometric templates from Redis and Matcher index.
  3. Retain *anonymized* audit logs for security, removing PII.

### Data Minimization (Article 5)
- **Biometrics**: We do NOT store raw images. Only mathematical vectors (embeddings) are stored.
- **Retention**: Biometric vectors are rotated/re-encrypted every 90 days.

### Consent Management (Article 7)
- **User Flow**: Registration requires explicit checkbox consent for biometric processing.
- **Record Keeping**: Consent timestamp and version are stored in `user-service`.

## 3. Zero Trust Architecture

### "Never Trust, Always Verify"
- **Identity**: Every request must have a valid JWT signed by `auth-service`.
- **Context**: `api-gateway` checks `risk-engine` for every sensitive request. 
- **Device**: Requests include device fingerprint headers.

## 4. Blockchain Identity
- **Integrity**: User identity events (registration, key rotation) are anchored to a private Ethereum sidechain using `ledger-service`.
- **Verifiability**: Any third party can verify the integrity of the Identity Root hash without accessing the raw data.
