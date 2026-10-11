# Shortlink Platform

A URL shortener with click analytics, deployed to AWS through a secure, GitOps-driven Kubernetes platform.
The app is intentionally simple. The project is about how it is built, shipped, secured, and operated.

> Status: Phase 0 (planning). See [docs/PLAN.md](docs/PLAN.md) for progress.

## Problem statement
Deliver a containerized web application to AWS with zero manual deployment, reproducible infrastructure,
least-privilege security, observable behavior, and controlled cost, across separate `dev` and `prod` environments.

## Highlights (to be filled with measured results)
- Infrastructure 100% Terraform, rebuilt from scratch in: _TBD_ minutes
- No long-lived credentials: GitHub OIDC for CI, IRSA / Pod Identity for pods
- GitOps delivery with Argo CD, rollback by reverting a commit
- Autoscaling (HPA + node scaling) verified under load
- Documented cost per session / per month: _TBD_

## Stack
AWS (VPC, EKS, ECR, RDS, Secrets Manager, KMS, CloudWatch) · Terraform · Docker · Kubernetes · Helm ·
Argo CD · GitHub Actions · Prometheus / Grafana · Trivy / Checkov / Kyverno · Python (FastAPI)

## Repository layout
| Path | Purpose |
|---|---|
| `app/` | Application source, Dockerfile, tests |
| `helm/shortlink/` | Helm chart for the app |
| `gitops/{dev,prod}/` | Desired state watched by Argo CD |
| `infra/terraform/` | Bootstrap (remote state), reusable modules, per-environment stacks |
| `.github/workflows/` | CI and promotion pipelines |
| `docs/` | Plan, architecture, ADRs, cost, security, runbooks |
| `scripts/` | Helper scripts (local cluster, teardown, cost checks) |

## How to run / destroy
_To be written as phases complete._ Every phase must keep a working `destroy` path.

## Documentation
- [Plan and phases](docs/PLAN.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Decision records](docs/adr/)
- [Cost](docs/COST.md) · [Security](docs/SECURITY.md) · [Runbooks](docs/runbooks/)
