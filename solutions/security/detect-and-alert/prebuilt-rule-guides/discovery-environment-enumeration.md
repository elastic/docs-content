---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Environment Variable Enumeration Detected via Defend for Containers" prebuilt detection rule.
---

# Environment Variable Enumeration Detected via Defend for Containers

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Environment Variable Enumeration Detected via Defend for Containers

This rule flags interactive execution of env or printenv inside a Linux container, a common discovery step to expose environment variables that frequently store credentials, tokens, and service configuration. A typical pattern: after gaining shell access to a pod, the attacker lists variables to harvest cloud keys, Kubernetes service account tokens, database URLs, and internal endpoints, enabling authenticated API calls, lateral movement within the cluster, or exfiltration via trusted services.

### Possible investigation steps

- Correlate with Kubernetes audit logs (exec/attach or debug) to identify the initiator identity, source IP, and command, and confirm whether the session was expected.
- Review the pod/container context (namespace, deployment, image digest/tag, node, and service account) and compare against baselines to catch unusual targets or ephemeral/privileged debug containers.
- Retrieve the enumerated variables to spot high-risk secrets such as cloud credentials, database passwords, or tokens, and immediately rotate/disable any discovered keys while reviewing provider audit logs for post-alert use.
- Trace subsequent activity within the container after the event for credential usage or exfiltration, including access to 169.254.169.254/metadata, calls to Kubernetes/cloud APIs, outbound network connections, or tooling like curl, wget, base64, and grep.
- Pivot to related signals on the same pod or node around the timestamp (new shells, service account token file reads, package installs, or suspicious downloads) to determine if this is part of a broader compromise.

### False positive analysis

- An operator opens an interactive shell in a container during routine troubleshooting and runs env or printenv to verify configuration, service endpoints, feature flags, or propagated secrets.
- Interactive shell initialization or entrypoint scripts in certain base images automatically invoke env or printenv upon TTY login to display or log variables, producing this event in benign sessions.

### Response and remediation

- Quarantine the affected pod where env/printenv was run by deleting the pod to drop the interactive session, applying a deny-all egress NetworkPolicy targeting its labels, and temporarily blocking kubectl exec/attach to that workload.
- Immediately rotate any secrets exposed in that container’s environment (cloud access keys, database passwords, API tokens, Kubernetes service account token), revoke active sessions at providers, and invalidate cached credentials on dependent services.
- Redeploy the application from a verified image digest with a fresh service account and newly issued secrets, and remove debug images or shell entrypoints that enabled interactive access.
- Escalate to incident response if env output contained credentials or the pod’s IP contacted 169.254.169.254, cloud/Kubernetes APIs, or external endpoints after the enumeration, indicating possible secret use or exfiltration.
- Replace environment-based secret injection with a secrets manager or projected volumes, set automountServiceAccountToken to false where not required, right-size RBAC for the workload, and block egress to the metadata service and the internet.
- Enforce preventive controls by disabling kubectl exec/attach for production (break-glass only with approval), enabling admission policies to block images with shells or package managers, and adding runtime rules to alert on interactive env/printenv followed by curl/wget/base64 or token file reads.

