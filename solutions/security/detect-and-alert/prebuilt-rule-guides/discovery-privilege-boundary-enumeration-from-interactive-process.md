---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Interactive Privilege Boundary Enumeration Detected via Defend for Containers" prebuilt detection rule.
---

# Interactive Privilege Boundary Enumeration Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Interactive Privilege Boundary Enumeration Detected via Defend for Containers

This detects an interactive session inside a Linux container running common identity and capability discovery tools (id, whoami, capsh, getcap, lsns) to map what privileges and namespace isolation the container actually has. This matters because attackers use this early in an intrusion to judge whether they can escalate within the container or pivot toward a host escape. A typical pattern is an attacker landing a shell through a vulnerable web service and immediately checking user context and Linux capabilities before attempting privilege abuse.

### Possible investigation steps

- Identify the impacted workload (pod/task/service), node, and cluster context, then correlate with Kubernetes audit logs or container runtime events to determine whether the interactive session originated from an operator action (e.g., exec) or an unexpected access path.  
- Review surrounding process activity from the same container to find follow-on commands indicating escalation or lateral movement attempts, such as spawning shells, modifying permissions, inspecting mounts, or downloading tooling.  
- Attribute the session to an identity by mapping the initiating user/service account and source to recent admin/CI activity, and flag anomalies like first-time access, unusual geolocation, or access outside change windows.  
- Evaluate escape and blast-radius risk by confirming the container’s effective privileges and isolation, including privileged mode, added capabilities, host namespace sharing, and sensitive host mounts or sockets.  
- If activity is suspicious, preserve evidence (processes, mounts, network connections, recent file changes) and consider isolating the pod/node or rotating credentials before remediation actions that would destroy artifacts.

### False positive analysis

- A platform engineer or developer attaches an interactive shell to a running container for routine troubleshooting and runs `id`/`whoami` to confirm the effective user and group context before making configuration changes.  
- During a planned hardening or validation task, an operator interactively inspects container capability and namespace settings using `capsh`/`getcap`/`lsns` to verify the workload is running with the intended privilege boundaries.

### Response and remediation

- Contain the incident by terminating the interactive session and quarantining the affected pod/container (or cordoning the node) while preserving container filesystem, running processes, mounts, and active network connections for evidence.  
- Eradicate by removing any unauthorized shells, binaries, or scripts dropped during the session, revoking/rotating credentials used to access the container (service account tokens, registry creds, app secrets), and rebuilding/redeploying the workload from a known-good image.  
- Recover by restoring the service with clean images and validated configuration, then verify no persistence remains by checking for unexpected running processes, modified entrypoints, altered file permissions, or new cron/systemd artifacts within the container image/build context.  
- Escalate to the incident response/on-call security team immediately if the container is privileged, has hostPath mounts or access to the container runtime socket, shares host namespaces, or if follow-on behavior appears (e.g., attempts to access `/proc/1`, `/var/run/docker.sock`, `nsenter`, or outbound downloads).  
- Harden by disabling or tightly restricting interactive exec/attach for production workloads, enforcing least-privilege securityContext (drop capabilities, runAsNonRoot, read-only root filesystem), and preventing host mounts/sockets via admission controls and policy (Pod Security Admission/Gatekeeper/Kyverno).  
- Improve detection and prevention by alerting on interactive shells and suspicious tooling in containers, adding egress allowlists to limit tool download/pivoting, and ensuring audit logging is enabled for Kubernetes exec events and container runtime actions.
