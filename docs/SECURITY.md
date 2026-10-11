# Security

## Principles
- No long-lived AWS credentials anywhere: GitHub OIDC for CI, IRSA / Pod Identity for workloads
- Least-privilege IAM; database reachable only from the cluster
- Encryption at rest (KMS) and in transit
- Secrets only in Secrets Manager, synced into the cluster; never in Git
- Shift-left scanning: Trivy (images), Checkov/tfsec (Terraform), Kyverno (admission policy)

## Controls checklist
- [ ] Root account MFA, daily work through a non-root IAM identity
- [ ] GitHub OIDC role scoped to this repo and branches
- [ ] Network policies default-deny
- [ ] Pod Security Standards enforced
- [ ] Resource limits required by policy
- [ ] Image scan gate in CI
- [ ] Terraform scan gate in CI
- [ ] CloudTrail enabled

## Scan results log
| Date | Tool | Findings before | Findings after |
|---|---|---|---|
|  |  |  |  |
