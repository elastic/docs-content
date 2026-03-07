---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Tool Enumeration Detected via Defend for Containers" prebuilt detection rule.
---

# Tool Enumeration Detected via Defend for Containers

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Tool Enumeration Detected via Defend for Containers

Detects interactive use of which inside a Linux container to list installed networking, container-control, compiler, and scanning utilities. Adversaries do this to quickly assess built-in tools for living-off-the-land actions like payload download, cluster manipulation, or reconnaissance without dropping new binaries. Example: after compromising a Kubernetes pod, an operator runs which curl wget kubectl nmap python to decide how to transfer data, interact with the API, or probe the network.

### Possible investigation steps

- Correlate Kubernetes audit logs to determine whether the pod was accessed via kubectl exec, attach, or an ephemeral container and to identify the requesting user, source IP, and user agent.
- Review the container’s process tree and TTY session around the alert time to see if the same session subsequently executed the enumerated utilities or performed network reconnaissance or data transfer.
- Analyze outbound network connections and DNS queries from the pod around the event to unfamiliar destinations or cluster control-plane endpoints and compare them against expected egress policy.
- Inspect pod and container metadata (namespace, service account, image, node) and evaluate RBAC bindings and mounted secrets to gauge potential impact and access scope.
- Confirm with the service owner whether this interactive container access aligns with an approved maintenance or debugging task and gather the corresponding change ticket or runbook reference.

### False positive analysis

- An engineer opens an interactive shell in a container for approved troubleshooting and runs which on utilities like curl, wget, kubectl, and python to confirm tool availability before debugging.
- During routine post-deployment checks, an operator follows a runbook that uses which to verify paths for expected binaries such as openssl and gcc inside the container, resulting in a benign alert.

### Response and remediation

- Immediately terminate any active TTY/shell in the affected pod (namespace/name) and isolate it by applying a temporary deny-all NetworkPolicy and removing exec/attach permissions from its service account.
- Delete the pod and any attached ephemeral debug container, redeploy from a known-good image, and rotate mounted secrets, cloud credentials, and the service account token present in the container.
- Restore service from clean deployments and verify the workload behaves as expected by running smoke tests and confirming the pod’s outbound connections are limited to approved destinations and ports.
- Escalate to the incident response team if the same session executed kubectl or docker, ran scanning tools such as nmap/masscan, accessed /var/run/secrets or changed RBAC, or connected to unfamiliar external IPs or the Kubernetes API server, and preserve evidence (container filesystem snapshot, shell history, Kubernetes audit logs, and node syslogs).
- Harden by enforcing admission controls to block interactive kubectl exec/attach to production pods and requiring runAsNonRoot, a read-only root filesystem, and dropped Linux capabilities on this workload.
- Reduce living-off-the-land options by rebuilding images to distroless/minimal and omitting utilities enumerated by which (curl, wget, nc, python, kubectl), and restrict egress with NetworkPolicies and service account RBAC to prevent cluster manipulation from inside containers.

