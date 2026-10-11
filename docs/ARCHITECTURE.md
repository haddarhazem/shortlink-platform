# Architecture

> Draft. Add a diagram (`docs/architecture.png`, source in draw.io or Excalidraw) once Phase 1 is done.

## Overview
- **Network:** one VPC, 2 AZs. Public subnets (load balancer), private subnets (nodes), isolated subnets (database).
- **Compute:** EKS with a managed node group. App runs as a Deployment behind an ALB (AWS Load Balancer Controller).
- **Data:** RDS PostgreSQL in isolated subnets, credentials in Secrets Manager, synced by External Secrets Operator.
- **Identity:** GitHub Actions uses OIDC to assume an IAM role. Pods use IRSA / Pod Identity. No static AWS keys.
- **Delivery:** GitHub Actions (CI) builds, scans, and pushes to ECR, then updates the image tag in `gitops/`.
  Argo CD syncs `gitops/dev` automatically; `gitops/prod` changes only through an approved pull request.
- **Observability:** Prometheus + Grafana for metrics, Loki or CloudWatch for logs, alerts to SNS email.
- **Local dev:** `kind` cluster using the same Helm chart.

## Environments
`dev` and `prod` are separate namespaces in one cluster to control cost. Real production would use separate clusters
or accounts (see ADR).

## Terraform layout
- `bootstrap/`: S3 state bucket + locking, GitHub OIDC role
- `modules/`: `vpc`, `eks`, `ecr`, `rds` (reusable)
- `envs/dev`, `envs/prod`: compose the modules

## Open questions
- Domain name + ACM/Route 53, or use the ALB hostname only?
- Postgres on RDS vs DynamoDB for click counters?
- Prometheus stack in-cluster vs Amazon Managed Prometheus?
