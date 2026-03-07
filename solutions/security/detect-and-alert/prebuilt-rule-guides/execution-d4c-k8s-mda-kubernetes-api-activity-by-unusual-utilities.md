---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Direct Interactive Kubernetes API Request by Unusual Utilities" prebuilt detection rule.
---

# Direct Interactive Kubernetes API Request by Unusual Utilities

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Direct Interactive Kubernetes API Request by Unusual Utilities

This rule detects interactive commands executed inside containers that use atypical utilities to hit the Kubernetes API, paired with near-simultaneous API activity on pods, secrets, service accounts, roles/bindings, or pod exec/attach/log/portforward. It surfaces hands-on-keyboard discovery and lateral movement using custom scripts that evade common tool allowlists; for example, an intruder opens a shell in a pod, uses Python to query the in-cluster API to list secrets, then triggers pods/exec to pivot into another workload.

### Possible investigation steps

- Identify the implicated pod, container image, and executing service account, then quickly review its RBAC bindings and effective permissions to determine blast radius.
- Inspect the container’s interactive session context by pulling recent command lines, shell history, environment variables, and mounted service account tokens, and look for custom scripts or binaries issuing HTTP requests.
- Correlate nearby Kubernetes audit entries tied to the same principal and pod to map accessed resources and verbs, noting any exec/attach/portforward or sensitive object interactions across namespaces.
- Review network activity from the pod to the API server and any in-pod proxies, including DNS lookups and outbound connections, to spot nonstandard clients or tunneling behavior.
- If suspicious, isolate the pod or node, capture runtime artifacts (e.g., process memory or HTTP client traffic), revoke and rotate the service account credentials, and verify image provenance and integrity.

### False positive analysis

- An operator interactively attaches to a pod and uses a Python REPL or bash with /dev/tcp to call the in-cluster API for routine troubleshooting (e.g., list pods, read ConfigMaps, or run selfsubjectaccessreviews), producing normal audit entries that match the rule signature.
- A correlation artifact arises when two namespaces have pods with the same name: one pod starts an interactive shell while another independently performs get/list/watch calls, and the 1-second sequence keyed only on pod-name links the unrelated events.

### Response and remediation

- Immediately isolate the implicated pod that issued direct API calls using a nonstandard utility by applying a deny-all egress NetworkPolicy in its namespace (including to kubernetes.default.svc:443), terminating the interactive session, and scaling its owning Deployment/Job/StatefulSet to zero replicas.
- Before teardown, capture a runtime snapshot of the container and node including the binary or script used to query the API (e.g., files under /tmp or /dev/tcp usage), shell history, environment, and the mounted service account token and CA bundle at /var/run/secrets/kubernetes.io/serviceaccount/.
- Revoke access by removing the service account’s RoleBindings/ClusterRoleBindings, deleting all pods that mount that service account to force token rotation, rotating any Secrets and ConfigMaps that were read or created during the window, and deleting any unauthorized Jobs, CronJobs, or Deployments created by the same principal.
- Restore workloads from a known-good image digest, re-enable the Deployment only after image scan and integrity checks pass, and monitor subsequent Kubernetes audit logs for pods/exec, portforward, and access to secrets across the affected namespaces.
- Escalate to incident response leadership and consider cluster-wide containment if audit logs show create/patch of ClusterRoleBindings, access to secrets outside the workload’s namespace, or use of pods/exec to pivot into other nodes or system namespaces such as kube-system.
- Harden access by enforcing least-privilege RBAC that denies pods/exec and attach for application service accounts, setting automountServiceAccountToken: false on workloads that do not need it, restricting egress to the API server with NetworkPolicies, and requiring just-in-time break-glass roles for interactive access.

