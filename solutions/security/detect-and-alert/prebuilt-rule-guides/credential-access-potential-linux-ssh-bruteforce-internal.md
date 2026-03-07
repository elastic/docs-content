---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Internal Linux SSH Brute Force Detected" prebuilt detection rule.'
---

# Potential Internal Linux SSH Brute Force Detected

## Triage and analysis

### Investigating Potential Internal Linux SSH Brute Force Detected

The rule identifies consecutive internal SSH login failures targeting a user account from the same source IP address to the same target host indicating brute force login attempts.

#### Possible investigation steps

- Investigate the login failure user name(s).
- Investigate the source IP address of the failed ssh login attempt(s).
- Investigate other alerts associated with the user/host during the past 48 hours.
- Identify the source and the target computer and their roles in the IT environment.

### False positive analysis

- Authentication misconfiguration or obsolete credentials.
- Service account password expired.
- Infrastructure or availability issue.

### Related Rules

- Potential External Linux SSH Brute Force Detected - fa210b61-b627-4e5e-86f4-17e8270656ab
- Potential SSH Password Guessing - 8cb84371-d053-4f4f-bce0-c74990e28f28

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
