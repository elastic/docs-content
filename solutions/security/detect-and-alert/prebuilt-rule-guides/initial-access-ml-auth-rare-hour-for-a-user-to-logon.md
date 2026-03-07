---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Hour for a User to Logon" prebuilt detection rule.
---

# Unusual Hour for a User to Logon

## Triage and analysis

### Investigating Unusual Hour for a User to Logon

This rule uses a machine learning job to detect a user logging in at a time of day that is unusual for the user. This can be due to credentialed access via a compromised account when the user and the threat actor are in different time zones. It can also indicate unauthorized user activity, as it often occurs during non-business hours.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate any abnormal account behavior, such as command executions, file creations or modifications, network connections, data access, and logon events.
- Investigate other alerts associated with the involved users during the past 48 hours.

### False positive analysis

- Users may need to log in during non-business hours to perform work-related tasks. Examine whether the company policies authorize this or if the activity is done under change management.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

