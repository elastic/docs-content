---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Network Activity to a Suspicious Top Level Domain" prebuilt detection rule.'
---

# Network Activity to a Suspicious Top Level Domain

## Triage and analysis

### Investigating Network Activity to a Suspicious Top Level Domain

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes or malicious scripts.
- Review if the domain reputation and the frequency of network activities as well as any download/upload activity.
- Verify if the executed process is persistent on the host like common mechanisms Startup folder, task or Run key.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Extract this communication's indicators of compromise (IoCs) and use traffic logs to search for other potentially compromised hosts.

### False positive analysis

- Trusted domain from an expected process running in the environment.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Immediately block the identified indicators of compromise (IoCs).
- Implement any temporary network rules, procedures, and segmentation required to contain the attack.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Update firewall rules to be more restrictive.
- Reimage the host operating system or restore the compromised files to clean versions.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
