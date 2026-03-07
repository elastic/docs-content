---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Execution from a WebDav Share" prebuilt detection rule.'
---

# Suspicious Execution from a WebDav Share

## Triage and analysis

### Investigating Suspicious Execution from a WebDav Share

#### Possible investigation steps

- Check if the remote webdav server is autorized by the organization.
- Check all the downloaded files from the remote server and their content.
- Investigate the process execution chain (parent process tree) to identify the initial vector.
- Investigate other alerts associated with the user/host during the past 5 minutes.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Identify the target computer and its role in the IT environment.
- Investigate what commands were run, and assess whether this behavior is prevalent in the environment by looking for similar occurrences across hosts.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Review the privileges assigned to the user to ensure that the least privilege principle is being followed.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
