---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Service Account Namespace Read Detected via Defend for Containers" prebuilt detection rule.
---

# Service Account Namespace Read Detected via Defend for Containers

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Service Account Namespace Read Detected via Defend for Containers

This rule flags an interactive process inside a container opening /var/run/secrets/kubernetes.io/serviceaccount/namespace, which reveals the pod’s Kubernetes namespace; adversaries use this quick check to orient themselves and scope discovery. A common pattern is: after landing a shell in a pod, the attacker reads the namespace file, then issues namespace-scoped kubectl or direct API calls to list Deployments, Secrets, and ServiceAccounts, map privileges and service endpoints, and plan targeted lateral movement within that namespace.

### Possible investigation steps

- Build the process tree and shell session timeline around the event to identify the parent and child processes, interactive TTY, and exact commands executed before and after.
- Map the container to its pod, namespace, node, image, owner, and service account, and verify whether any kubectl exec/attach or debug container activity targeting this pod is expected at that time.
- Correlate Kubernetes audit logs for that service account and pod around the timestamp to spot list/get calls, Secrets or ServiceAccounts enumeration, and the user/IP that initiated any exec/attach.
- Inspect network flows and DNS from the container to the Kubernetes API server immediately after the event to confirm follow-on API access or token validation attempts.
- Review the service account’s RBAC bindings and search the container for reads of the token/ca.crt or the presence of kubectl/kubeconfig or scripts that could leverage the token.

### False positive analysis

- During legitimate troubleshooting, a user opens an interactive shell in the container and the shell’s profile or prompt customization reads /var/run/secrets/kubernetes.io/serviceaccount/namespace to display the current namespace.
- A documented operational check or training exercise instructs staff to manually open the service account namespace file inside a container to confirm the environment before changes, producing a benign detection.

### Response and remediation

- Immediately kill the interactive shell process inside the container (e.g., bash/sh attached via kubectl exec) and quarantine the pod/namespace by applying a deny-all NetworkPolicy and pausing the owning Deployment/StatefulSet.
- Escalate to a major incident and page the on-call cluster security team if you observe subsequent reads of /var/run/secrets/kubernetes.io/serviceaccount/token or ca.crt or API calls from the pod to the Kubernetes API (443) that list Secrets or ServiceAccounts.
- Rotate the service account credentials by deleting the pod to force a new projected token, set automountServiceAccountToken: false on the workload if not needed, and remove pods/exec and pods/attach privileges from users or roles that accessed this pod.
- Redeploy the workload from a trusted, signed image without embedded shells/kubectl, verify image digest on rollout, and only lift quarantine after confirming no unauthorized containers, cronjobs, or startup scripts were added.
- Enforce least-privilege RBAC for the service account (deny list/get on Secrets, ConfigMaps, and Pods in the namespace), enable Pod Security Admission restricted with readOnlyRootFilesystem and dropped Linux capabilities, and require approvals for kubectl exec using ephemeral containers for debugging.

