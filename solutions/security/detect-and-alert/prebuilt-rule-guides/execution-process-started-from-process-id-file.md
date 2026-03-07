---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Process Started from Process ID (PID) File" prebuilt detection rule.
---

# Process Started from Process ID (PID) File

## Triage and analysis

### Investigating Process Started from Process ID (PID) File
Detection alerts from this rule indicate a process spawned from an executable masqueraded as a legitimate PID file which is very unusual and should not occur. Here are some possible avenues of investigation:
- Examine parent and child process relationships of the new process to determine if other processes are running.
- Examine the /var/run directory using Osquery to determine other potential PID files with unsually large file sizes, indicative of it being an executable: "SELECT f.size, f.uid, f.type, f.path from file f WHERE path like '/var/run/%%';"
- Examine the reputation of the SHA256 hash from the PID file in a database like VirusTotal to identify additional pivots and artifacts for investigation.

