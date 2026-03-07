---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Newly Observed Process Exhibiting High CPU Usage" prebuilt detection rule.
---

# Newly Observed Process Exhibiting High CPU Usage

## Triage and analysis

### Investigating Newly Observed Process Exhibiting High CPU Usage

This rule alerts on processes exhibiting high CPU usage and that are observed for the first time in the previous 5 days.

### Possible investigation steps
- Examine the process name, command line, and SHA-256 hash to determine whether the process is expected or known to be malicious.
- Validate the observed CPU usage and duration to determine whether the spike is abnormal for this process and host.
- Check for related process activity such as parent/child processes, suspicious process spawning, or privilege escalation attempts.
- Review additional host telemetry including:
  - Network connections initiated by the process
  - File creation or modification events
  - Persistence mechanisms (services, scheduled tasks, registry keys)
- Determine whether similar activity is observed on other hosts, which may indicate a broader compromise.

### False positive analysis
- Legitimate high-CPU processes such as software updates, backup agents, security scans, or system maintenance tasks.
- Resource-intensive but benign applications (e.g., compilers, video encoding, data processing jobs).
- Security tools or monitoring agents temporarily consuming high CPU.

### Related Rules

- Detection Alert on a Process Exhibiting CPU Spike - df9c0e92-5dee-4f1d-a760-3a5c039e4382
- Multiple Alerts on a Host Exhibiting CPU Spike - b7f77c3c-1bcb-4afc-9ace-49357007947b

### Response and remediation
- If malicious activity is confirmed, isolate the affected host to prevent further impact.
- Terminate the offending process if safe to do so.
- Remove any identified malicious binaries or artifacts and eliminate persistence mechanisms.
- Apply relevant patches or configuration changes to remediate the root cause.
- Monitor the environment for recurrence of similar high-CPU processes combined with security alerts.
- Escalate the incident if multiple hosts or indicators suggest coordinated or widespread activity.
