---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Pod or Container Creation with Suspicious Command-Line" prebuilt detection rule.'
---

# Pod or Container Creation with Suspicious Command-Line

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Pod or Container Creation with Suspicious Command-Line

This rule flags pods or containers started via orchestration or runtime tools that immediately execute a shell with commands linked to persistence, privilege changes, or covert I/O (cron, rc.local, sudoers, .ssh, base64, netcat/socat, /tmp). This matters because attackers often spin short‑lived workloads to modify startup paths or drop backdoors. Example: kubectl run --restart=Never -- sh -c 'echo ssh-rsa AAAA... >> /root/.ssh/authorized_keys && nc -lvp 4444 -e /bin/sh'.

### Possible investigation steps

- Pivot to Kubernetes audit logs to identify the actor (user or service account), namespace, source IP/workstation, and RBAC context that launched the workload, and validate whether this aligns with approved admin activity.
- Pull the pod/container spec and image metadata to quickly assess risk indicators like unapproved registry/image, privileged mode, hostNetwork/hostPID, and hostPath or sensitive volume mounts that could mutate the node.
- Parse the executed command to determine whether it attempts persistence or backdoor setup (editing cron/rc.local, sudoers or authorized_keys, base64 file drops, starting netcat/socat listeners), and verify those changes on the container or node.
- Correlate runtime and network telemetry for the workload to detect outbound connections or listening ports indicative of reverse shells, and identify destination endpoints and nodes involved.
- Trace the launcher context by reviewing kubectl client host artifacts (shell history, kubeconfig, IAM/MFA tokens) or CI/CD logs, and check for recent anomalous commits or pipeline runs that could have triggered it.

### False positive analysis

- Administrators performing network troubleshooting or node diagnostics may start ephemeral pods via kubectl run --restart=Never or ad hoc containers with docker/nerdctl that launch sh and use nc/socat/telnet, read /proc, or write to /tmp.
- Engineers may pass configs or test scripts into a shell using base64/xxd and touch cron, rc.local, /etc/ssh, ~/.ssh, or /etc/profile during validation or break-fix work, producing commands that resemble persistence behavior.

### Response and remediation

- Delete the offending pod/container, revoke the kubeconfig or runtime credentials used to launch it, and quarantine the image and namespace, cordoning the node if privileged, hostNetwork/hostPID, or hostPath were present.
- Kill any spawned shells or listeners (e.g., sh -c 'nc -lvp ...', socat, telnet) on affected nodes, remove unauthorized firewall/iptables rules, and apply temporary deny-all egress NetworkPolicies to cut C2.
- Eradicate persistence by restoring clean versions of /etc/cron*, /etc/rc.local, /etc/profile, /etc/sudoers, /etc/ssh/* and deleting unauthorized keys or scripts under /root/.ssh, ~/.ssh, /tmp, /dev/shm, /var/tmp, and hostPath-mounted directories.
- Rebuild compromised nodes or redeploy workloads with known-good images, rotate cluster secrets and SSH keys, and validate baseline integrity with file hashes and admission scans before returning to service.
- Escalate to incident response if the actor is unverified or commands touched /etc/shadow or /etc/sudoers, used privileged containers or hostPath to access the host, or opened external connections or listening ports on the node.
- Harden by enforcing admission controls to deny pods that start /bin/sh or /bin/bash as PID 1, block privileged/hostNetwork/hostPID/hostPath, apply per-namespace egress policies, and restrict RBAC so only approved admins can run kubectl run --restart=Never or docker/nerdctl run.
