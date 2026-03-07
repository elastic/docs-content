---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Forbidden Direct Interactive Kubernetes API Request" prebuilt detection rule.
---

# Forbidden Direct Interactive Kubernetes API Request

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Forbidden Direct Interactive Kubernetes API Request

This rule correlates an interactive command execution inside a container with a Kubernetes API request that is explicitly forbidden, signaling hands-on-keyboard probing and unauthorized access attempts. It matters because attackers use live shells to enumerate cluster resources and test privileges for lateral movement or escalation. Example: after compromising a pod, an operator opens a shell and runs kubectl get secrets or curls the API server with the pod’s token, repeatedly receiving 403 Forbidden.

### Possible investigation steps

- Correlate the pod, container, namespace, node, and service account from the alert, then quickly pull the matching audit entries to see the verb, resource, requestURI, and userAgent for the forbidden calls.
- Determine whether the container image normally includes utilities like kubectl/curl/openssl or if they were dropped into the pod, and review recent file writes and package installs to differentiate admin debugging from hands-on-keyboard activity.
- Inspect the pod’s service account bindings and effective RBAC in the target namespace to confirm least privilege and understand why the request was denied, then check for other successful API requests from the same identity around the same timeframe.
- Review network connections from the pod to the API server (and any proxies) during the session to validate direct access paths, source IPs, and whether a mounted service account token from /var/run/secrets was used.
- Validate whether this was an authorized SRE/debug session by contacting the workload owner and checking for recent kubectl exec or ephemeral debug activity; if not expected, expand the search for similar forbidden attempts from other pods.

### False positive analysis

- An authorized kubectl exec or ephemeral debug session inside a pod where an engineer runs kubectl or curl to probe API resources and, because the pod’s service account is intentionally least‑privileged, the requests are forbidden as expected.
- Benign interactive troubleshooting that mistakenly uses the wrong namespace or queries cluster‑scoped endpoints from within the container (e.g., curl/openssl to the API server), causing the audit logs to show forbid decisions even though no malicious access was attempted.

### Response and remediation

- Immediately terminate the interactive shell (e.g., sh/bash) in the offending container and isolate the pod by applying a deny-egress NetworkPolicy in its namespace that blocks outbound connections to https://kubernetes.default.svc and the API server IPs.
- Revoke and rotate credentials by deleting the pod and its ServiceAccount token Secret, temporarily setting automountServiceAccountToken: false on the workload, and redeploying with a new ServiceAccount after validating RBAC least privilege.
- Remove attacker tooling and persistence by rebuilding the container image to exclude kubectl/curl/openssl/socat/ncat, clearing writable volume mounts that contain dropped binaries or scripts, and redeploying from a trusted registry.
- Sweep for spread by identifying pods running the same image or on the same node and terminating any interactive processes issuing Kubernetes API requests from within containers, then restart those workloads cleanly.
- Escalate to incident response if you observe successful API operations (200/201) on secrets, configmaps, or RBAC objects, exec into other pods, or privileged container settings (privileged=true, hostNetwork, or hostPID), indicating lateral movement or credential compromise.
- Harden going forward by tightening RBAC on the new ServiceAccount, enforcing Gatekeeper/OPA policies to deny images that include kubectl/curl and block interactive shells, setting readOnlyRootFilesystem and dropping NET_ADMIN, and restricting API server access via egress controls.

