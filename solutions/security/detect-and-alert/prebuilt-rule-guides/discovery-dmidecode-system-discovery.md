---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "System Information Discovery via dmidecode from Parent Shell" prebuilt detection rule.'
---

# System Information Discovery via dmidecode from Parent Shell

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating System Information Discovery via dmidecode from Parent Shell

This rule flags dmidecode launched from a parent shell, signaling collection of hardware and firmware inventory that adversaries use to profile a host and inform exploitation or lateral movement. A typical pattern is an intruder running bash -c 'dmidecode -t system -t bios' within a post-exploitation script to harvest model, serial, BIOS vendor, and hypervisor indicators, then tailoring payload choices or host-based evasion accordingly.

### Possible investigation steps

- Extract the full parent shell command payload to see exact dmidecode arguments, targeted DMI types, and any output redirection or piping to grep, gzip, curl, scp, or similar utilities indicating data collection or exfiltration.
- Correlate execution context by tying the parent shell to the user, TTY versus non-interactive origin (cron/systemd/SSH), source IP, and presence of unexpected sudo/root elevation to judge intent and privilege.
- Pivot on the parent PID and session to list adjacent commands within the timeline to identify broader discovery or staging chains and any script or binary loader used.
- Search for captured output by reviewing recent file writes under /tmp, /var/tmp, /dev/shm, and home directories for DMI dumps, hardware inventory files, or compressed archives, and triage ownership and timestamps.
- Investigate network activity from the shell and its children around the event for outbound connections, especially HTTP/S3/SSH transfers that could carry dmidecode output, and capture destination details for enrichment.

### False positive analysis

- A system administrator runs a shell with -c to execute dmidecode during manual troubleshooting; corroborate with an interactive TTY, a known admin user, and absence of adjacent collection or network activity.
- A legitimate cron or systemd maintenance/provisioning job calls a shell with -c to run dmidecode for hardware inventory; verify the scheduled unit or service, script location under /etc, and expected run cadence.

### Response and remediation

- Immediately kill the shell process running '-c "dmidecode ..."', terminate its children (e.g., grep, gzip, curl, scp), and isolate the host if the command chained output to a network transfer.
- Block observed exfil destinations by adding temporary egress rules for the IP/domain referenced in the parent shell (curl/wget/scp targets), and confiscate any DMI dumps or archives found under /tmp, /var/tmp, or /dev/shm.
- Remove persistence by deleting scripts and jobs that call dmidecode, including entries under /etc/cron.*, systemd units in /etc/systemd/system, or shell scripts dropped in home directories and /opt, and clear residual output files.
- Recover by validating integrity of /usr/sbin/dmidecode and shell binaries (bash/sh/zsh), restoring from backup if tampering is detected, and re-enable network only after rotating passwords and SSH keys for affected accounts.
- Escalate to incident response if dmidecode output is compressed/encoded then sent externally (e.g., '/tmp/dmi.txt.gz' piped to curl or scp), if run via sudo by an unexpected user, or observed on multiple hosts in a short window.
- Harden by restricting dmidecode use to approved scripts via sudoers and AppArmor/SELinux profiles, alerting on shell '-c' hardware inventory commands, auditing writes to /tmp and /var/tmp, and replacing ad-hoc inventory with signed, centrally managed tooling.
