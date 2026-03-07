---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential NetNTLMv1 Downgrade Attack" prebuilt detection rule.'
---

# Potential NetNTLMv1 Downgrade Attack

## Triage and analysis

### Investigating Potential NetNTLMv1 Downgrade Attack


### Possible investigation steps

- Review the registry event logs to confirm the modification of the LmCompatibilityLevel value in the specified registry paths, ensuring the change was not part of a legitimate administrative action.
- Identify the user account and process responsible for the registry modification by examining the event logs for associated user and process information.
- Check for any recent remote authentication attempts or sessions on the affected host to determine if unauthorized access was achieved.
- Investigate the timeline of the registry change to correlate with any other suspicious activities or alerts on the host, such as the execution of unusual processes or network connections.
- Evaluate the security posture of the affected system, including patch levels and existing security controls, to identify potential vulnerabilities that could have been exploited.

### False positive analysis

- Administrative changes to LmCompatibilityLevel settings can trigger false positives when IT personnel intentionally modify registry settings for legitimate purposes. To handle this, create exceptions for known administrative activities by documenting and excluding these specific registry changes from alerts.
- Software updates or installations that modify NTLM settings might be flagged as false positives. To mitigate this, maintain a list of trusted software and their expected registry changes, and configure the detection system to ignore these during update windows.
- Automated scripts or management tools that adjust NTLM configurations for compliance or performance reasons can also cause false positives. Identify these tools and their expected behavior, then set up exclusions for their registry modifications to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Re-enable NTLMv2 on the affected system by modifying the registry value back to its secure state.
- Conduct a thorough review of recent user activity and system logs to identify any unauthorized access or changes made during the period NLA was disabled.
- Reset passwords for all accounts that have accessed the affected system to mitigate potential credential compromise.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring on the affected system and similar endpoints to detect any further attempts to disable NLA or other suspicious activities.
