---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kubernetes Service Account Modified RBAC Objects" prebuilt detection rule.
---

# Kubernetes Service Account Modified RBAC Objects

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Service Account Modified RBAC Objects

This rule detects Kubernetes service accounts performing allowed write actions on RBAC resources such as Roles and RoleBindings, which is atypical because service accounts rarely administer permissions. It matters because stolen or over-privileged service account tokens can silently alter authorization to gain or retain elevated access across the cluster. An attacker commonly uses a compromised workload’s token to create or patch a binding that grants cluster-admin privileges to their service account for persistent control.

### Possible investigation steps

- Retrieve the full audit event and diff the before/after RBAC object to identify newly granted subjects, verbs, resources, and cluster-admin or wildcard permissions.
- Trace the acting service account to its owning workload (Deployment/Pod) and node, then review recent image changes, restarts, exec sessions, and container logs around the event time for compromise indicators.
- Determine whether the change is attributable to an expected controller or GitOps/CI automation by correlating with change tickets, pipeline runs, and repository commits for RBAC manifests.
- Validate whether the service account token may be abused by checking for unusual API access patterns, source IPs/user agents, and cross-namespace activity compared to its baseline behavior.
- Contain if suspicious by reverting the RBAC change, rotating the service account token (and any mounted secrets), and tightening the service account’s Role/ClusterRole to least privilege.

### False positive analysis

- A platform automation running in-cluster (e.g., a controller or CI job using a service account) legitimately applies RBAC manifests during routine deployment, upgrades, or namespace onboarding, resulting in create/patch/update of Roles or RoleBindings.  
- A Kubernetes operator or housekeeping workflow running under a service account intentionally adjusts RBAC as part of maintenance (e.g., rotating access, reconciling drift, or cleaning up obsolete bindings) and triggers allowed delete or update actions on RBAC resources.

### Response and remediation

- Immediately remove or quarantine the offending service account by deleting its RoleBindings/ClusterRoleBindings and restarting or scaling down the owning workload to stop further RBAC writes.  
- Revert the unauthorized RBAC object changes by restoring the last known-good Roles/Bindings from GitOps/manifests (or `kubectl rollout undo` where applicable) and verify no new subjects gained wildcard or cluster-admin-equivalent access.  
- Rotate credentials by recreating the service account or triggering token re-issuance, deleting any mounted legacy token secrets, and redeploying workloads to ensure old tokens cannot be reused.  
- Hunt and eradicate persistence by searching for additional recently modified RBAC objects and newly created service accounts in the same namespaces, then remove unauthorized accounts/bindings and scan the implicated container images for backdoors.  
- Escalate to incident response and cluster administrators immediately if any change grants `cluster-admin`, introduces `*` verbs/resources, or binds a service account to privileged ClusterRoles across namespaces.  
- Harden going forward by enforcing least-privilege RBAC, enabling admission controls to restrict RBAC modifications to approved identities/namespaces, and using short-lived projected service account tokens with workload identity constraints.

