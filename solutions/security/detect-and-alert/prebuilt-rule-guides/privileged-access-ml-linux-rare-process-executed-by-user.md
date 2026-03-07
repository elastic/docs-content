---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Process Detected for Privileged Commands by a User" prebuilt detection rule.
---

# Unusual Process Detected for Privileged Commands by a User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Process Detected for Privileged Commands by a User

Machine learning models are employed to identify anomalies in process execution, particularly those involving privileged commands. Adversaries may exploit legitimate user accounts to execute unauthorized privileged actions, aiming for privilege escalation. This detection rule leverages ML to flag atypical processes, indicating potential misuse of elevated access, thus aiding in early threat identification.

### Possible investigation steps

- Review the specific user account associated with the alert to determine if the account has a history of executing privileged commands or if this is an anomaly.
- Examine the process details, including the command line arguments and the parent process, to identify if the process is legitimate or potentially malicious.
- Check the timestamp of the process execution to correlate with any other suspicious activities or alerts that occurred around the same time.
- Investigate the source IP address or host from which the command was executed to verify if it is a known and trusted location for the user.
- Look into recent authentication logs for the user account to identify any unusual login patterns or access from unfamiliar devices.
- Assess the user's role and permissions to determine if the execution of such privileged commands aligns with their job responsibilities.

### False positive analysis

- Routine administrative tasks by IT staff may trigger alerts. Review and whitelist known administrative processes that are regularly executed by trusted personnel.
- Automated scripts or scheduled tasks that perform privileged operations can be flagged. Identify and exclude these scripts if they are verified as part of normal operations.
- Software updates or installations that require elevated privileges might be detected. Ensure that these processes are documented and excluded if they are part of standard maintenance procedures.
- Development or testing environments where privileged commands are frequently used for legitimate purposes can cause false positives. Consider creating exceptions for these environments after thorough validation.
- Temporary elevated access granted for specific projects or tasks can lead to alerts. Monitor and document these instances, and adjust the detection rule to accommodate such temporary changes.

### Response and remediation

- Immediately isolate the affected user account to prevent further unauthorized privileged actions. This can be done by disabling the account or changing its password.
- Review and terminate any suspicious processes or sessions initiated by the user account to contain potential malicious activity.
- Conduct a thorough audit of recent privileged commands executed by the user to identify any unauthorized changes or actions that need to be reversed.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or accounts have been compromised.
- Implement additional monitoring on the affected system and user account to detect any further anomalous behavior or attempts at privilege escalation.
- Review and update access controls and permissions for the affected user account to ensure they align with the principle of least privilege.
- Document the incident, including actions taken and lessons learned, to improve response strategies and prevent recurrence.
