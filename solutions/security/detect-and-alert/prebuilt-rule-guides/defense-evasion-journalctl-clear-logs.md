---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Clear Logs via Journalctl" prebuilt detection rule.
---

# Attempt to Clear Logs via Journalctl

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Clear Logs via Journalctl

This detection flags attempts to purge systemd journal logs by invoking journalctl with vacuum options, which attackers use to erase evidence and impede investigations. A common pattern is a compromised user escalating to root and immediately running sudo journalctl --vacuum-time=1s or --vacuum-size=1M, sometimes via a script or cron job, to rapidly truncate the journal across all boots and hide prior execution traces.

### Possible investigation steps

- Enrich with user/UID, effective privileges, parent and command-line, session/TTY, and origin (SSH IP or local), and determine if execution came from a scheduled job (cron/systemd timer) or a script.
- Quantify destructiveness by extracting the exact vacuum parameter value(s) and immediately checking journal state (journalctl --disk-usage and --list-boots) and /var/log/journal size/mtime to see how much history was removed.
- Inspect configuration and persistence paths for intentional log suppression, including recent changes in /etc/systemd/journald.conf (Storage=volatile, SystemMaxUse, SystemMaxFileSize, MaxRetentionSec) and any new systemd units or scripts invoking journalctl vacuum.
- Correlate the vacuum timestamp with preceding activity to identify what might be concealed (privilege escalation, new accounts, sudoers edits, suspicious binaries), using auditd/EDR telemetry and shell history to rebuild the timeline.
- Verify remote log forwarding and SIEM ingestion for this host, compare gaps around the vacuum time, and recover pre-vacuum events from central storage to assess impact and intent.

### False positive analysis

- A sysadmin or maintenance script ran journalctl --vacuum-time or --vacuum-size to reclaim space on a host under log disk pressure, which should correlate with low-free-space alerts, approved retention policy, and a scheduled systemd timer or cron job.
- OS provisioning or image-preparation steps vacuumed the journal with journalctl --vacuum-files to sanitize logs before snapshotting, typically a one-time root action occurring near installation and matching documented build procedures.

### Response and remediation

- Immediately kill any active journalctl vacuum invocation (e.g., pkill -x journalctl), lock or remove sudo for the initiating user, and network-quarantine the host to prevent further tampering.
- Remove persistence by disabling systemd units/timers and cron jobs that call "journalctl --vacuum-*", inspecting /etc/systemd/system/* for ExecStart=journalctl vacuum and /etc/crontab, /etc/cron.*, and user crontabs, then deleting the offending scripts.
- Recover logging by setting Storage=persistent and policy-compliant SystemMaxUse/SystemMaxFileSize/MaxRetentionSec in /etc/systemd/journald.conf, restarting systemd-journald, and backfilling missing events from central log archives.
- Harden by enabling remote forwarding (ForwardToSyslog=yes and rsyslog/syslog-ng to SIEM), adding auditd rules to alert on "journalctl --vacuum-*", and tightening sudoers to require MFA and record command I/O for journalctl on critical hosts.
- Preserve evidence by archiving remaining /var/log/journal entries, journald.conf and its mtime, modified unit files under /etc/systemd/system, and shell/auth logs, and capture a disk snapshot before making further changes.
- Escalate to incident response if root executed "journalctl --vacuum-time/size/files" outside a documented maintenance window, if Storage=volatile was set or retention reduced below policy, or if the same actor performed vacuums on multiple hosts within 24 hours.

