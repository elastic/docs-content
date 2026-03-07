---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Failed Logon Events" prebuilt detection rule.
---

# Spike in Failed Logon Events

## Triage and analysis

### Investigating Spike in Failed Logon Events

This rule uses a machine learning job to detect a substantial spike in failed authentication events. This could indicate attempts to enumerate users, password spraying, brute force, etc.

#### Possible investigation steps

- Identify the users involved and if the activity targets a specific user or a set of users.
- Check if the authentication comes from different sources.
- Investigate if the host where the failed authentication events occur is exposed to the internet.
  - If the host is exposed to the internet, and the source of these attempts is external, the activity can be related to bot activity and possibly not directed at your organization.
  - If the host is not exposed to the internet, investigate the hosts where the authentication attempts are coming from, as this can indicate that they are compromised and the attacker is trying to move laterally.
- Investigate other alerts associated with the involved users and hosts during the past 48 hours.
- Check whether the involved credentials are used in automation or scheduled tasks.
- If this activity is suspicious, contact the account owner and confirm whether they are aware of it.
- Investigate whether there are successful authentication events from the involved sources. This could indicate a successful brute force or password spraying attack.

### False positive analysis

- If the account is used in automation tasks, it is possible that they are using expired credentials, causing a spike in authentication failures.
- Authentication failures can be related to permission issues.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Assess whether the asset should be exposed to the internet, and take action to reduce your attack surface.
  - If the asset needs to be exposed to the internet, restrict access to remote login services to specific IPs.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

