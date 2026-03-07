---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Multiple Alerts on a Host Exhibiting CPU Spike" prebuilt detection rule.
---

# Multiple Alerts on a Host Exhibiting CPU Spike

## Triage and analysis

### Investigating Multiple Alerts on a Host Exhibiting CPU Spike

This rule identifies hosts that both triggered multiple security alerts and exhibited unusually high CPU utilization on the
within a short time window. This combination may indicate malicious execution, resource abuse, or post-compromise activity.

### Possible investigation steps
- Review the correlated alert(s) to understand why the host was flagged by the detection alerts.
- Examine the involved process name, command line, and SHA-256 hash to determine whether those processes are expected or known to be malicious.
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

### Response and remediation
- If malicious activity is confirmed, isolate the affected host to prevent further impact.
- Terminate the offending process if safe to do so.
- Remove any identified malicious binaries or artifacts and eliminate persistence mechanisms.
- Apply relevant patches or configuration changes to remediate the root cause.
- Monitor the environment for recurrence of similar high-CPU processes combined with security alerts.
- Escalate the incident if multiple hosts or indicators suggest coordinated or widespread activity.
