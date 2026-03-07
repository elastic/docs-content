---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Modification of Persistence Relevant Files Detected via Defend for Containers" prebuilt detection rule.
---

# Modification of Persistence Relevant Files Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Modification of Persistence Relevant Files Detected via Defend for Containers

This detection flags a process inside a Linux container creating or modifying files tied to host-style persistence and privilege control, such as cron schedules, systemd units, sudoers, or shell startup profiles. These changes rarely belong in normal container runtime behavior, so they often signal an attacker staging long-lived execution, escalating privileges, or preparing an escape path. A common pattern is dropping a new `/etc/cron.d/*` entry that periodically launches a payload or backconnects.

### Possible investigation steps

- Review the modifying process’s full command line, parent/ancestor chain, effective UID, and container entrypoint to determine whether it aligns with expected runtime behavior or indicates an interactive shell/exploit.  
- Pull the before/after contents of the changed file and look for execution hooks (cron command, systemd ExecStart, sudoers NOPASSWD, or shell profile stagers), then extract any referenced binaries, users, paths, or URLs for follow-on hunting.  
- Determine whether the container is privileged or has elevated capabilities and sensitive host mounts (e.g., `/etc`, `/var/run/docker.sock`, `/proc`, `/sys`) that would make the change meaningful for host persistence or escape attempts.  
- Correlate the modification time with nearby activity from the same container (process spawns, tool downloads, outbound connections, and interactive access such as `kubectl exec`) to reconstruct the sequence and probable entry vector.  
- Check for the same change across replicas/nodes and in the image/build pipeline, and if the modification is unapproved, isolate and redeploy from a known-good image while preserving artifacts for analysis.

### False positive analysis

- An application container running as root updates shell startup files (e.g., `/root/.bashrc`, `/etc/profile.d/*`) at runtime to enforce environment variables, PATH changes, or interactive defaults for troubleshooting, triggering a write/open event without any persistence intent.  
- A container startup/entrypoint script generates or adjusts cron/systemd-related files (e.g., `/etc/cron.d/*`, `/etc/systemd/system/*.service`) to schedule internal maintenance tasks or align configuration on first boot, causing file creations/renames outside package-manager processes.

### Response and remediation

- Quarantine the affected workload by scaling the deployment to zero or applying a deny-all egress policy, and isolate the node if the container was privileged or had host filesystem mounts that could make the persistence change impact the host.  
- Preserve evidence by exporting the modified persistence-related file(s) (e.g., `/etc/cron.d/*`, `/etc/sudoers*`, systemd unit/timer, shell profile) and collecting the writing process binary, command line, environment, and a short window of process and network activity from the container.  
- Eradicate by deleting or reverting the unauthorized cron/systemd/sudoers/profile changes, removing any referenced payload binaries/scripts, revoking any newly added users/keys/tokens, and rotating credentials used by the container or mounted into it.  
- Recover by redeploying the service from a known-good image and clean configuration (ConfigMaps/Secrets), validating that no persistence files are modified at runtime and that outbound connections and scheduled executions return to expected behavior.  
- Escalate to incident response immediately if the change grants passwordless sudo, drops a new systemd unit/timer or cron job that executes a network-capable command, or if the container is privileged/has `/var/run/docker.sock` or host `/etc` mounted, as this may indicate attempted host persistence or escape.  
- Harden by enforcing read-only root filesystem and non-root execution, restricting capabilities/privileged mode and sensitive host mounts, and adding policy controls to block writes to `/etc/cron*`, `/etc/sudoers*`, systemd paths, and shell profiles outside the image build pipeline.
