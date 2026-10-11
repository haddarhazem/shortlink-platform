# ADR 0002: GitOps with Argo CD instead of push-based deploys

- Status: proposed
- Date: 2026-10-11

## Context
Deployments must be auditable, repeatable, and revertible without giving CI direct cluster-admin access.

## Options considered
1. **Push-based** (CI runs `kubectl`/`helm upgrade`): simple, but CI needs cluster credentials and state drifts.
2. **GitOps with Argo CD**: Git is the source of truth, cluster pulls changes, rollback = revert a commit.

## Decision
Use Argo CD. CI only builds, scans, and pushes the image, then updates the image tag in `gitops/`.

## Consequences
Extra component to run and secure. Clear audit trail and simple rollbacks.
