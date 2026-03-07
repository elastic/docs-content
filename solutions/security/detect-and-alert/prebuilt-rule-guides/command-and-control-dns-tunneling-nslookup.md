---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential DNS Tunneling via NsLookup" prebuilt detection rule.
---

# Potential DNS Tunneling via NsLookup

## Triage and analysis

### Investigating Potential DNS Tunneling via NsLookup

Attackers can abuse existing network rules that allow DNS communication with external resources to use the protocol as their command and control and/or exfiltration channel.

DNS queries can be used to infiltrate data such as commands to be run, malicious files, etc., and also for exfiltration, since queries can be used to send data to the attacker-controlled DNS server. This process is commonly known as DNS tunneling.

More information on how tunneling works and how it can be abused can be found on [Palo Alto Unit42 Research](https://unit42.paloaltonetworks.com/dns-tunneling-how-dns-can-be-abused-by-malicious-actors).

#### Possible investigation steps

- Investigate the script execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Inspect the DNS query and identify the information sent.
- Extract this communication's indicators of compromise (IoCs) and use traffic logs to search for other potentially compromised hosts.

### False positive analysis

- This mechanism can be used legitimately. If the parent process is trusted and the data sent is not sensitive nor command and control related, this alert can be closed.

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

