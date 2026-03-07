---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Creation or Modification of Root Certificate" prebuilt detection rule.
---

# Creation or Modification of Root Certificate

## Triage and analysis

### Investigating Creation or Modification of Root Certificate

Root certificates are the primary level of certifications that tell a browser that the communication is trusted and legitimate. This verification is based upon the identification of a certification authority. Windows adds several trusted root certificates so browsers can use them to communicate with websites.

[Check out this post](https://www.thewindowsclub.com/what-are-root-certificates-windows) for more details on root certificates and the involved cryptography.

This rule identifies the creation or modification of a root certificate by monitoring registry modifications. The installation of a malicious root certificate would allow an attacker the ability to masquerade malicious files as valid signed components from any entity (for example, Microsoft). It could also allow an attacker to decrypt SSL traffic.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Investigate abnormal behaviors observed by the subject process such as network connections, other registry or file modifications, and any spawned child processes.
- If one of the processes is suspicious, retrieve it and determine if it is malicious:
  - Use a private sandboxed malware analysis system to perform analysis.
    - Observe and collect information about the following activities:
      - Attempts to contact external domains and addresses.
      - File and registry access, modification, and creation activities.
      - Service creation and launch activities.
      - Scheduled task creation.
  - Use the PowerShell `Get-FileHash` cmdlet to get the files' SHA-256 hash values.
    - Search for the existence and reputation of the hashes in resources like VirusTotal, Hybrid-Analysis, CISCO Talos, Any.run, etc.

### False positive analysis

- This detection may be triggered by certain applications that install root certificates for the purpose of inspecting SSL traffic. Benign true positives (B-TPs) can be added as exceptions if necessary.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove the malicious certificate from the root certificate store.
- Remove and block malicious artifacts identified during triage.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

