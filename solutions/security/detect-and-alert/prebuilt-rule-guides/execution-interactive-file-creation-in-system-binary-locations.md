---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "System Path File Creation and Execution Detected via Defend for Containers" prebuilt detection rule.
---

# System Path File Creation and Execution Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating System Path File Creation and Execution Detected via Defend for Containers

This detects an interactive session in a running Linux container creating new files under system binary paths like /etc, /root, /bin, /usr/bin, /usr/local/bin, or /entrypoint, which often signals an attempt to tamper with execution flow or hide tooling. Attackers commonly gain a shell, then use curl/wget (or a busybox variant) from a writable staging area to drop a new executable into /usr/local/bin or overwrite an entrypoint script to ensure their code runs on start.

### Possible investigation steps

- Capture the created file’s metadata (owner, permissions, timestamps) and contents/hash, then determine whether it is an executable/script or a modification to startup/auth/config behavior.  
- Compare the file and its path against the container image baseline (layer diff) to confirm it was introduced at runtime and identify the interactive command that created it.  
- Review the interactive session context (TTY, user, entry method) and surrounding command activity to assess intent and whether secrets or credentials were accessed.  
- Pivot to related activity from the same session such as outbound connections, additional downloads to writable staging areas, or subsequent execution of the new file to gauge impact and scope.  
- Check for persistence or host-impact setup by inspecting entrypoint/service definitions, PATH hijacks, mounted host paths, and any new cron/systemd/profile changes within the container.

### False positive analysis

- A container administrator troubleshooting interactively may use curl/wget (including via busybox wget) to fetch configuration or helper scripts and write them into /etc, /root, or /entrypoint to quickly test startup or runtime behavior changes.  
- An interactive maintenance session may execute a script staged in /tmp or /dev/shm that drops a small wrapper binary or symlink into /usr/local/bin or /usr/bin to temporarily add debugging utilities or adjust PATH-resolved command behavior during incident response.

### Response and remediation

- Isolate the impacted container by removing it from service and blocking its egress, then preserve the container filesystem (or take a snapshot) so the created artifacts under /etc, /root, /bin, /usr/bin, /usr/local/bin, or /entrypoint can be analyzed.  
- Identify and remove the dropped or modified file(s) and any related persistence (e.g., altered /entrypoint script, PATH-hijacking binaries, modified shell profiles), then stop any processes launched from writable staging paths like /tmp, /dev/shm, /var/tmp, /run, /var/run, or /mnt.  
- Redeploy the workload from a known-good image and verified configuration (including entrypoint and mounted volumes), rotate any secrets or tokens that could have been accessed in the interactive session, and validate the new pod/container does not recreate files in system binary locations.  
- Escalate immediately to the incident response team if the created file is executable, replaces an entrypoint, initiates outbound downloads or connections, or if multiple containers show similar drops in system binary paths suggesting broader compromise.  
- Harden by enforcing non-root, read-only root filesystem, and disallowing interactive exec into production containers, then restrict outbound network access and block write access to system binary locations via security policies and runtime controls.
