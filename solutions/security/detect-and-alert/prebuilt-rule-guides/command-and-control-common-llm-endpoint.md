---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Connection to Common Large Language Model Endpoints" prebuilt detection rule.'
---

# Connection to Common Large Language Model Endpoints

## Triage and analysis

### Investigating Connection to Common Large Language Model Endpoints

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes or malicious scripts.
- Verify if the executed process is persistent on the host like common mechanisms Startup folder, task or Run key.
- Review any unusual network, files or registry events by the same process.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Extract this communication's indicators of compromise (IoCs) and use traffic logs to search for other potentially compromised hosts.

### False positive analysis

- Trusted applications from an expected process running in the environment.

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
