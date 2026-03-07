---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Successful Logon Events from a Source IP" prebuilt detection rule.
---

# Spike in Successful Logon Events from a Source IP

## Triage and analysis

### Investigating Spike in Successful Logon Events from a Source IP

This rule uses a machine learning job to detect a substantial spike in successful authentication events. This could indicate post-exploitation activities that aim to test which hosts, services, and other resources the attacker can access with the compromised credentials.

#### Possible investigation steps

- Identify the specifics of the involved assets, such as role, criticality, and associated users.
- Check if the authentication comes from different sources.
- Use the historical data available to determine if the same behavior happened in the past.
- Investigate other alerts associated with the involved users during the past 48 hours.
- Check whether the involved credentials are used in automation or scheduled tasks.
- If this activity is suspicious, contact the account owner and confirm whether they are aware of it.

### False positive analysis

- Understand the context of the authentications by contacting the asset owners. If this activity is related to a new business process or newly implemented (approved) technology, consider adding exceptions — preferably with a combination of user and source conditions.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

