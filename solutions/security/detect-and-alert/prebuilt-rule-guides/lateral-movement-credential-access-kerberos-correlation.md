---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Kerberos Authentication Ticket Request" prebuilt detection rule.
---

# Suspicious Kerberos Authentication Ticket Request

## Triage and analysis

### Investigating Suspicious Kerberos Authentication Ticket Request

Kerberos is the default authentication protocol in Active Directory, designed to provide strong authentication for client/server applications by using secret-key cryptography.

Domain-joined hosts usually perform Kerberos traffic using the `lsass.exe` process. This rule detects the occurrence of traffic on the Kerberos port (88) by processes other than `lsass.exe` to detect the unusual request and usage of Kerberos tickets.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Check if the Destination IP is related to a Domain Controller.
- Review events ID 4769 and 4768 for suspicious ticket requests.
- Investigate potentially compromised accounts. Analysts can do this by searching for login events (for example, 4624) to the target host after the registry modification.

### False positive analysis

- Active Directory audit tools.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
  - Ticket requests can be used to investigate potentially compromised accounts.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

