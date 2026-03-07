---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Reverse Shell Activity via Terminal" prebuilt detection rule.
---

# Potential Reverse Shell Activity via Terminal

## Triage and analysis

### Investigating Potential Reverse Shell Activity via Terminal

A reverse shell is a mechanism that's abused to connect back to an attacker-controlled system. It effectively redirects the system's input and output and delivers a fully functional remote shell to the attacker. Even private systems are vulnerable since the connection is outgoing. This activity is typically the result of vulnerability exploitation, malware infection, or penetration testing.

This rule identifies commands that are potentially related to reverse shell activities using shell applications.

#### Possible investigation steps

- Examine the command line and extract the target domain or IP address information.
  - Check if the domain is newly registered or unexpected.
  - Check the reputation of the domain or IP address.
  - Scope other potentially compromised hosts in your environment by mapping hosts that also communicated with the domain or IP address.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Investigate any abnormal account behavior, such as command executions, file creations or modifications, and network connections.
- Investigate any abnormal behavior by the subject process such as network connections, file modifications, and any spawned child processes.

### False positive analysis

- This activity is unlikely to happen legitimately. Any activity that triggered the alert and is not inherently malicious must be monitored by the security team.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Take actions to terminate processes and connections used by the attacker.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

