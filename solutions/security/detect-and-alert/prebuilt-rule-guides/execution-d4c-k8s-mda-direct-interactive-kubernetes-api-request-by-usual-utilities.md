---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Direct Interactive Kubernetes API Request by Common Utilities" prebuilt detection rule.
---

# Direct Interactive Kubernetes API Request by Common Utilities

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Direct Interactive Kubernetes API Request by Common Utilities

This detection links an interactive invocation of common networking utilities or kubectl inside a container to a near-simultaneous Kubernetes API response, indicating hands-on-keyboard access to the API server for discovery or lateral movement. A common attacker pattern is compromising a pod, reading its mounted service account token, then running curl or kubectl interactively to query /api or /apis endpoints to list pods and secrets and map cluster scope.

### Possible investigation steps

- From Kubernetes audit logs linked to the pod, capture the authenticated principal, namespace, verbs, and request URIs to determine whether the activity focused on discovery or sensitive resources like secrets or RBAC objects.
- Correlate the interactive container activity with kubelet exec/attach or terminal session telemetry to identify who initiated the session and through which source IP or control-plane endpoint.
- Inspect the pod’s service account by validating access to the mounted token path and enumerating its RoleBindings and ClusterRoleBindings to quantify effective privileges and decide on immediate revocation or rotation.
- Review the container image provenance and available shell history or command logs to confirm use of networking utilities or kubectl and identify any reads of secrets, kubeconfig files, or /api and /apis endpoints.
- Expand the time window to find prior or subsequent API calls from the same pod, namespace, or node, and quarantine or cordon the workload if you observe sustained enumeration or cross-namespace access.

### False positive analysis

- An operator uses kubectl exec -it to enter a pod and runs kubectl or curl to list resources or verify RBAC, producing interactive process starts and near-simultaneous Kubernetes audit responses that are expected during troubleshooting.
- During routine connectivity or certificate checks, an engineer attaches to a container that includes curl/openssl/socat/ncat and interactively tests the Kubernetes API server endpoint, generating correlated audit events without malicious intent.

### Response and remediation

- Immediately isolate the implicated pod by terminating the interactive shell and curl/kubectl processes, applying a deny-all NetworkPolicy in its namespace, and temporarily blocking pod egress to the kube-apiserver address.
- Revoke and rotate the service account credentials used by the pod, invalidate the token at /var/run/secrets/kubernetes.io/serviceaccount/token, and remove excess RoleBindings or ClusterRoleBindings tied to that identity.
- Delete and restore the workload from a trusted image that excludes curl/wget/openssl/socat/ncat, with automountServiceAccountToken disabled and least-privilege RBAC enforced.
- Escalate to incident response if the pod read Secrets or ConfigMaps, modified RBAC objects, attempted create/patch/delete on cluster-scoped resources, or originated from an unapproved operator workstation or bastion.
- Harden by restricting kubectl exec/attach to a small admin group with MFA, enabling admission controls (Pod Security Admission, Gatekeeper, or Kyverno) to block shells or kubectl/netcat in images, and applying egress NetworkPolicies so only approved namespaces can reach https://kubernetes.default.svc.

