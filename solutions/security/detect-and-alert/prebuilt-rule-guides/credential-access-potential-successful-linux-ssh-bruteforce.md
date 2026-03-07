---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Successful SSH Brute Force Attack" prebuilt detection rule.'
---

# Potential Successful SSH Brute Force Attack

## Triage and analysis

### Investigating Potential Successful SSH Brute Force Attack

The rule identifies consecutive SSH login failures followed by a successful login from the same source IP address to the same target host indicating a successful attempt of brute force password guessing.

#### Possible investigation steps

- Investigate the login failure user name(s).
- Investigate the source IP address of the failed ssh login attempt(s).
- Investigate other alerts associated with the user/host during the past 48 hours.
- Identify the source and the target computer and their roles in the IT environment.

### False positive analysis

- Authentication misconfiguration or obsolete credentials.
- Service account password expired.
- Infrastructure or availability issue.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Ensure active session(s) on the host(s) are terminated as the attacker could have gained initial access to the system(s).
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
