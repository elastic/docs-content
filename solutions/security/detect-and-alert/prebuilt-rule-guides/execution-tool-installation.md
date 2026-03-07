---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Tool Installation Detected via Defend for Containers" prebuilt detection rule.
---

# Tool Installation Detected via Defend for Containers

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Tool Installation Detected via Defend for Containers

This rule flags interactive package installs inside Linux containers for network utilities or interpreters, a strong signal of hands-on activity to enumerate, fetch payloads, and pivot. Example attacker pattern: after gaining a shell in a pod, they run apt/apk/pacman to add curl, netcat, or socat, pull a second stage from an external host, and open a reverse shell to move from the container into adjacent services.

### Possible investigation steps

- Attribute the interactive install by correlating Kubernetes audit events (exec/attach) and runtime logs to the pod/namespace, a specific user or service account, source IP, and client, and verify alignment with approved break-glass procedures.
- Diff the running container filesystem against the image baseline or SBOM to enumerate newly added binaries and libraries, review package manager logs/cache, and capture hashes and paths for forensics.
- Examine pod-level network telemetry and DNS logs around the event for outbound connections, downloads, or reverse shell patterns, and isolate the workload if beaconing or exfiltration is observed.
- Verify the pod’s security context and mounts for privilege escalation vectors (privileged, hostPID/IPC, hostPaths, docker.sock) and inventory exposed credentials (service account tokens, cloud metadata, env vars, ~/.ssh, .aws), rotating any secrets at risk.
- Hunt across the cluster for similar interactive installs or exec sessions using audit and Defend for Containers telemetry, and review recent image builds and deployments to detect in-cluster modifications before quarantining or restarting affected workloads.

### False positive analysis

- A developer attaches an interactive shell to a running container to debug connectivity, using apt or apk to install curl or netcat for quick tests, which matches the rule’s interactive install of network utilities.
- During an approved break-glass fix, an operator interactively installs python or openssl with yum or dnf in a minimal container to run a temporary diagnostic script, triggering the same package-install signature.

### Response and remediation

- Immediately isolate the pod/container that performed interactive installs (e.g., apt-get install curl, apk add netcat) by applying a deny-all NetworkPolicy, terminating active kubectl exec/attach sessions, and cordoning the node if the pod is privileged or has hostPath/docker.sock mounts.
- Stop and delete the compromised workload, snapshot the container filesystem, then redeploy the deployment/statefulset from a trusted image and purge added tools by removing packages and caches (/var/lib/apt, /var/cache/apk, /var/cache/yum) from any retained volumes.
- Rotate the pod’s service account token and any exposed credentials found in env vars, ~/.ssh, or cloud provider metadata, and invalidate outbound connections established by newly installed binaries like curl, wget, socat, or netcat via egress firewall rules.
- Restore normal connectivity only after confirming no unauthorized binaries remain by diffing against the image SBOM and checking package history files like /var/log/dpkg.log, /var/log/yum.log, or /etc/apk/world, then validating app readiness/liveness probes.
- Escalate to incident response if the install included tor/torsocks, openssl used to generate new keys, reverse-shell behavior (e.g., netcat -e or socat TCP:external_ip), or if activity occurred in production without a change request.
- Enforce immutability and least privilege by rebuilding images without package managers or shells (distroless), enabling read-only root filesystems, disallowing kubectl exec via RBAC, using admission controls to block privileged pods and hostPath/docker.sock mounts, and tightening egress to only approved destinations.

