---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential RemoteMonologue Attack" prebuilt detection rule.'
---

# Potential RemoteMonologue Attack

## Triage and analysis

### Investigating Potential RemoteMonologue Attack


### Possible investigation steps

- Review the registry event logs to confirm the modification of the RunAs value in the specified registry paths, ensuring the change was not part of a legitimate administrative action.
- Identify the user account and process responsible for the registry modification by examining the event logs for associated user and process information.
- Check for any recent remote authentication attempts or sessions on the affected host to determine if this activity is associated with lateral movement or not.
- Investigate the timeline of the registry change to correlate with any other suspicious activities or alerts on the host, such as the execution of unusual processes or network connections.

### False positive analysis

- Software updates or installations that modify COM settings.
- Automated scripts or management tools that adjust COM configurations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Modify the registry value back to its secure state, ensuring that "RunAs" value is not set to "Interactive User".
- Conduct a thorough review of recent user activity and system logs to identify any unauthorized access or changes made during the period NLA was disabled.
- Reset passwords for all accounts that have accessed the affected system to mitigate potential credential compromise.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring on the affected system and similar endpoints to detect any further attempts to disable NLA or other suspicious activities.
