---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Service Account Token or Certificate Access Followed by Kubernetes API Request" prebuilt detection rule.
---

# Service Account Token or Certificate Access Followed by Kubernetes API Request

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Service Account Token or Certificate Access Followed by Kubernetes API Request

This rule correlates interactive access to a pod’s service account token or CA certificate with a near-immediate Kubernetes API request, signaling credential harvesting to query the cluster and potential lateral movement. An attacker execs into a container, reads /var/run/secrets/kubernetes.io/serviceaccount/token and ca.crt, then uses curl or kubectl with that token and CA to list pods, get secrets, or create a privileged pod to pivot across nodes.

### Possible investigation steps

- Attribute the activity by identifying the pod, container image, node, and interactive session initiator (e.g., kubectl exec) from Kubernetes events and cluster logs to determine whether a human or automation accessed the credentials.
- Retrieve the pod’s service account and enumerate its RBAC bindings to assess effective privileges, highlighting any ability to read secrets, create pods, or modify roles.
- Reconstruct the full sequence of audit log requests tied to that pod/user around the alert, noting resources, verbs, namespaces, response codes, and userAgent to distinguish legitimate controller behavior from reconnaissance.
- Examine the container for signs of token abuse or exfiltration by reviewing shell history and filesystem artifacts, and correlate with network egress from the pod to external destinations.
- Validate that the API request originated from the same pod by matching source IP, node, and TLS client identity, and check for concurrent suspicious activity on the node or other pods.

### False positive analysis

- A cluster operator troubleshooting an issue execs into a pod, inspects the service account token or CA certificate, and then uses the pod’s credentials to make a quick Kubernetes API request to verify permissions or list resources.
- A workload running with TTY/stdin enabled is marked as interactive, and the application legitimately reads the service account token (e.g., on startup or token refresh) to perform routine API operations such as leader election or informer watches, producing the observed file access followed by audit log activity.

### Response and remediation

- Immediately isolate the pod that read /var/run/secrets/kubernetes.io/serviceaccount/token or ca.crt by deleting the pod or scaling its deployment to zero, cordoning its node if similar behavior is seen on other pods, and applying a NetworkPolicy that blocks the pod’s access to the API server while you capture its filesystem.
- Revoke access by removing the implicated service account’s RBAC bindings, recreating the service account to invalidate tokens, restarting any workloads that mount /var/run/secrets/kubernetes.io/serviceaccount, and rotating the service-account signing key if compromise is suspected.
- Validate and recover by reviewing audit records for unauthorized actions (e.g., secrets reads, pod or role changes), rolling back or deleting any malicious resources, and redeploying affected workloads from trusted images with signed releases.
- Escalate to incident response immediately if you observe API requests from the pod that read secrets, create pods in other namespaces, alter Role or ClusterRoleBindings, or transmit the token/ca.crt via curl or similar tooling to external addresses.
- Harden by disabling automountServiceAccountToken on pods that don't require it, scoping service accounts to a single namespace with least‑privilege RBAC, enforcing Pod Security Admission to block privileged/interactive shells, and restricting exec/attach via RBAC or admission policies.

