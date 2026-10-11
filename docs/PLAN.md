# Project plan

## Requirements

### Functional
- [ ] Shorten a URL and redirect to the original
- [ ] Record clicks; analytics endpoint (clicks per link per day)
- [ ] Health and readiness endpoints

### Non-functional (success criteria)
| Area | Target | Verified by |
|---|---|---|
| Reproducibility | Whole infra from code; destroy + rebuild < 25 min | Timed rebuild, logged in `COST.md` |
| Security | No long-lived creds; private data tier; encryption; scans clean | `SECURITY.md`, pipeline results |
| Reliability | Multi-AZ, probes, automated rollback | Failure drill |
| Observability | Dashboards, alerts, centralized logs, runbook | Screenshots, runbook |
| Cost | Documented per-session and monthly estimate; budget alarms | `COST.md` |
| Delivery | Merge to `main` deploys `dev`; approval promotes `prod` | Pipeline runs |

## Cost rule
Develop on a local `kind` cluster. Create EKS only for short verification sessions, then `terraform destroy`.
Delete Kubernetes-created load balancers/volumes (Argo CD apps) BEFORE destroying the cluster, then verify nothing is left.

## Phases
Status: `[ ]` todo · `[~]` in progress · `[x]` done

- [~] **0. Plan**: requirements, repo layout, ADRs, architecture diagram, cost estimate
- [ ] **1. Foundations**: Terraform remote state, VPC module, IAM baseline, budget alarms
- [ ] **2. Application**: FastAPI app, Dockerfile, tests, Docker Compose
- [ ] **3. Local Kubernetes**: kind cluster, Helm chart, ingress, probes, limits, HPA
- [ ] **4. EKS**: Terraform EKS module, managed node group, OIDC provider, IRSA roles
- [ ] **5. Add-ons**: AWS Load Balancer Controller, External Secrets, metrics-server, Argo CD
- [ ] **6. GitOps pipeline**: CI (lint, test, scan, build, push to ECR) + Argo CD sync, dev auto / prod approval
- [ ] **7. Observability**: Prometheus, Grafana, alerts, logs
- [ ] **8. Hardening**: network policies, pod security, Kyverno, image/IaC scans, RBAC review
- [ ] **9. Failure drills**: bad deploy + rollback, node drain, load test with HPA
- [ ] **10. Publish**: README polish, diagram, demo video, LinkedIn post

## Evidence to collect (for the final write-up)
Diagram · pipeline screenshots · dashboard screenshots · rebuild time · cost numbers · scan results before/after ·
failure-drill write-up · short demo video
