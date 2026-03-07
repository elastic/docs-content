---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "File Transfer or Listener Established via Netcat" prebuilt detection rule.
---

# File Transfer or Listener Established via Netcat

## Triage and analysis

### Investigating File Transfer or Listener Established via Netcat

Netcat is a dual-use command line tool that can be used for various purposes, such as port scanning, file transfers, and connection tests. Attackers can abuse its functionality for malicious purposes such creating bind shells or reverse shells to gain access to the target system.

A reverse shell is a mechanism that's abused to connect back to an attacker-controlled system. It effectively redirects the system's input and output and delivers a fully functional remote shell to the attacker. Even private systems are vulnerable since the connection is outgoing.

A bind shell is a type of backdoor that attackers set up on the target host and binds to a specific port to listen for an incoming connection from the attacker.

This rule identifies potential reverse shell or bind shell activity using Netcat by checking for the execution of Netcat followed by a network connection.

#### Possible investigation steps

- Examine the command line to identify if the command is suspicious.
- Extract and examine the target domain or IP address.
  - Check if the domain is newly registered or unexpected.
  - Check the reputation of the domain or IP address.
  - Scope other potentially compromised hosts in your environment by mapping hosts that also communicated with the domain or IP address.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Investigate any abnormal account behavior, such as command executions, file creations or modifications, and network connections.
- Investigate any abnormal behavior by the subject process such as network connections, file modifications, and any spawned child processes.

### False positive analysis

- Netcat is a dual-use tool that can be used for benign or malicious activity. It is included in some Linux distributions, so its presence is not necessarily suspicious. Some normal use of this program, while uncommon, may originate from scripts, automation tools, and frameworks.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Block the identified indicators of compromise (IoCs).
- Take actions to terminate processes and connections used by the attacker.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

