# Cost

## Budget guardrails
- [ ] Zero-spend / $1 AWS Budget with email alert
- [ ] Cost Anomaly Detection enabled
- [ ] All resources tagged `project=shortlink`, `env=<dev|prod>`

## Estimates (fill in with real numbers)
| Component | Rate | Notes |
|---|---|---|
| EKS control plane | ~$0.10/hour | Only during verification sessions |
| Worker nodes (2x small) | _TBD_ | Spot where possible |
| ALB | _TBD_ | Created by the LB controller |
| RDS (smallest) | _TBD_ | Stop/destroy between sessions |
| NAT / VPC endpoints | _TBD_ | Prefer endpoints, destroy NAT after use |

## Session log
| Date | Duration | What ran | Cost | Leftovers checked? |
|---|---|---|---|---|
|  |  |  |  |  |

## Teardown checklist
1. Delete Argo CD apps / Kubernetes Services of type LoadBalancer and PVCs
2. `terraform destroy` (envs, then bootstrap only if retiring the project)
3. Check EC2 > Load Balancers, Volumes, Elastic IPs, NAT Gateways, ENIs
4. Check Billing dashboard
