---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Shell Command-Line History Deletion Detected via Defend for Containers" prebuilt detection rule.'
---

# Shell Command-Line History Deletion Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Shell Command-Line History Deletion Detected via Defend for Containers

This rule detects attempts during interactive sessions to delete, truncate, or disable shell command history files inside containers, a common tactic to erase evidence and impede investigations. An attacker uses kubectl exec to open an interactive bash shell in a running pod, then symlinks /root/.bash_history to /dev/null to prevent future commands from being recorded while performing reconnaissance or credential access.

### Possible investigation steps

- Correlate the container to its pod, namespace, and owning workload, and pull Kubernetes audit logs for exec/attach around the alert time to identify the caller identity, source IP, and user-agent and validate business justification.
- Reconstruct the interactive session timeline by reviewing adjacent process telemetry before and after the history suppression to surface reconnaissance, credential access, data staging, or tooling downloads the actor may be hiding.
- Examine shell configs and filesystem state for persistent history suppression (e.g., HISTFILE/HISTSIZE/HISTCONTROL in /etc/profile.d or .bashrc/.zshrc, or history files symlinked to /dev/null) and compare timestamps/owners to distinguish image defaults from live tampering.
- Assess runtime context for impact by confirming the session’s user/UID, effective capabilities, mounted secrets or tokens, and writable volumes, and checking for privilege escalation or access to sensitive data.
- If unauthorized, isolate the pod and capture volatile evidence (filesystem tarball, /proc, environment variables, shell rc files), rotate any exposed credentials, and hunt for similar events across pods/namespaces and the same source IP or identity.

### False positive analysis

- An authorized operator opens an interactive shell in a container for troubleshooting and intentionally clears or disables history (e.g., history -c, rm/truncate ~/.bash_history, or export HISTFILE=/dev/null) to avoid recording sensitive commands.
- The container image’s interactive shell startup configuration automatically disables history (e.g., HISTFILESIZE=0, unset HISTFILE, or linking ~/.bash_history to /dev/null), so a normal debug login triggers the alert.

### Response and remediation

- Isolate the affected pod by applying a temporary NetworkPolicy to block egress, remove pods/exec and pods/attach permissions from the caller, and terminate any interactive shells that executed rm, history -c, or truncate on ~/.bash_history or linked it to /dev/null.
- Eradicate changes by removing any ~/.bash_history symlink to /dev/null, recreating /root/.bash_history and /home/*/.bash_history with correct ownership and 600 permissions, and restoring HISTFILE/HISTFILESIZE/HISTCONTROL in /etc/profile.d, .bashrc, and .zshrc to expected values.
- Recover by rebuilding and redeploying the workload from a trusted image, rotating any secrets or tokens accessed during the session (service account token, cloud provider credentials, SSH keys), and validating that new shells now persist command history.
- Escalate to incident response if the exec caller identity is unknown or unauthorized, if privileged actions (kubectl with cluster-admin, sudo, or reading /var/run/secrets/kubernetes.io/serviceaccount) occurred after history deletion, or if multiple pods/namespaces show coordinated history suppression.
- Harden by restricting kubectl exec/attach to break-glass roles via RBAC, enforcing admission controls to block images or init scripts that unset HISTFILE or link ~/.bash_history to /dev/null, and adding runtime policy to deny rm/truncate of history files and alert on history -c.
