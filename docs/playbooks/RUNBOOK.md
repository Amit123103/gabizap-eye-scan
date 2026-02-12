# GABIZAP Incident Response Playbook (IRP)

**Severity Level:** SEV-1 (Critical System Failure)
**Trigger:** < 99.5% Success Rate on Biometric Auth, or Primary Region Unreachable.

## 🚨 IMMEDIATE ACTIONS (Automated)
1. **Bot**: PagerDuty alerts On-Call Engineer.
2. **Bot**: Route53 performs health-check failure protocol (removes US-EAST-1 IP).
3. **Bot**: Aurora Global DB initiates "Failover" to EU-WEST-1 (RPO < 1s).

## 👨‍💻 ENGINEER ACTIONS (Manual Override)
### Phase 1: Containment (0-5 Mins)
- [ ] Connect to `bastion-host-eu`.
- [ ] Verify `kubectl get pods` in EU region shows scaling activity.
- [ ] If DB failover stuck: Run `aws rds failover-global-cluster --region eu-west-1`.

### Phase 2: Mitigation (5-30 Mins)
- [ ] Enable "Degraded Mode" in API Gateway (Disable non-essential features like Risk Scoring historical analytics).
- [ ] Clear Redis Cache if session corruption suspected: `redis-cli FLUSHALL`.

### Phase 3: Restoration
- [ ] Once US region stabilizes, do **not** failback immediately.
- [ ] Wait for 1 hour of stability.
- [ ] Sync data back to original primary (Re-replication).

## 📞 ESCALATION CONTACTS
- **SRE Lead**: +1-555-0100
- **CISO**: +1-555-0199
- **AWS Support**: Case Priority "Production Down"

---
*Last Updated: 2026-02-13*
