# ADR 0001: Run on Kubernetes (EKS) instead of ECS Fargate

- Status: proposed
- Date: 2026-10-11

## Context
The project should demonstrate skills that transfer across employers. Cost is constrained (student, AWS Free plan credits).

## Options considered
1. **ECS Fargate**: simpler, no control-plane fee, AWS-specific.
2. **EKS**: more complex, ~$0.10/hour control plane plus nodes, portable skills (Helm, GitOps, operators).
3. **Local kind only**: free, but does not show real cloud integration.

## Decision
Develop and test on local `kind`; run on EKS only in short verification sessions. Keep the chart cloud-agnostic.

## Consequences
Higher complexity and cost than ECS, offset by transferable skills. Requires strict teardown discipline.
Revisit with measured cost/complexity numbers at the end of the project.
