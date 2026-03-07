---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Rare User Logon" prebuilt detection rule.'
---

# Rare User Logon

## Triage and analysis

### Investigating Rare User Logon

This rule uses a machine learning job to detect an unusual user name in authentication logs, which could detect new accounts created for persistence.

#### Possible investigation steps

- Check if the user was newly created and if the company policies were followed.
  - Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate other alerts associated with the involved users during the past 48 hours.
- Investigate any abnormal account behavior, such as command executions, file creations or modifications, and network connections.

### False positive analysis

- Accounts that are used for specific purposes — and therefore not normally active — may trigger the alert.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
