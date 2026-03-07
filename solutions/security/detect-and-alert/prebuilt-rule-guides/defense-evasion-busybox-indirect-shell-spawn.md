---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Proxy Shell Execution via Busybox" prebuilt detection rule.
---

# Proxy Shell Execution via Busybox

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Proxy Shell Execution via Busybox

This rule identifies Linux shells started via Busybox, indicating proxy execution to sidestep controls that focus on direct shell binaries. Adversaries leverage Busybox’s ubiquity and static build to blend in, obscure parentage, and run commands in constrained or minimal environments. A common pattern is copying a standalone busybox into /tmp on a container or embedded host, making it executable, then invoking busybox sh to run one-liners, pull payloads, and stage persistence.

### Possible investigation steps

- Correlate the event to a user session or container exec by pivoting to TTY/session ID, SSH auth logs, and Kubernetes/Docker exec audits to verify whether it was an authorized action.
- Determine Busybox provenance by checking its path and file metadata (non-standard location, recent write, unusual owner/capabilities or symlink), confirming package ownership, and hashing against trusted repositories and threat intelligence.
- Expand the process tree 10–15 minutes around the event to find staging steps (curl/wget/tftp, chmod, mv) and post-shell behavior (reverse shells, crypto miners, persistence writes).
- Collect live context for the shell (current working directory, environment, open sockets, controlling TTY, effective user) to quickly decide if it is interactive misuse or command staging.
- Hunt across hosts for similar Busybox-to-shell chains and review persistence artifacts and new files in writable dirs (crontab, systemd units, rc files, authorized_keys, /tmp, /dev/shm) to catch follow-on activity.

### False positive analysis

- An administrator performing recovery on a minimal host may copy a static busybox and start an interactive sh with no arguments for troubleshooting, producing a busybox-to-shell chain that is expected.
- Legitimate privilege-switch or login workflows using Busybox applets (e.g., su or login) can spawn a bare sh without -c for an authenticated session, so confirm a controlling TTY, expected user, and standard paths before treating it as malicious.

### Response and remediation

- Immediately isolate the impacted host or container at the network level, terminate any shells whose parent is busybox, and block outbound traffic initiated by those shells (e.g., nc, curl/wget, ssh to unknown IPs).
- Identify and remove rogue busybox copies or symlinks in writable locations such as /tmp, /var/tmp, and /dev/shm by revoking execute permissions or deleting them, and capture file hashes, paths, and mtimes for evidence.
- Remove persistence and droppers created by the busybox-spawned shell by cleaning newly added cron entries under /etc/cron.*, systemd units in /etc/systemd/system, rc.local edits, and suspicious authorized_keys or ~/.bashrc/.profile changes, then reboot if kernel modules or LD_PRELOAD were modified.
- Reset passwords, rotate SSH keys and tokens used in the session, rebuild affected containers from clean images or reimage hosts if system binaries were changed, and restore services only after verifying no busybox-to-shell chains launch at startup.
- Escalate to incident response if the busybox-launched shell ran as root, established a reverse connection (e.g., bash -i >& /dev/tcp/<IP>/<port>), created SUID files, or dropped payloads in /tmp, /var/tmp, or /dev/shm, or if a new busybox binary was downloaded or touched minutes before execution.
- Harden by enforcing noexec,nosuid,nodev mounts on /tmp and /var/tmp, constraining busybox with AppArmor/SELinux to block spawning interactive shells or execution from world-writable paths, locking down container runtime exec and capabilities (e.g., disable kubectl/docker exec for non-admins, remove CAP_SYS_ADMIN), and implementing file integrity monitoring on busybox and standard shells.

