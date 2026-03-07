---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "User or Group Creation/Modification" prebuilt detection rule.'
---

# User or Group Creation/Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating User or Group Creation/Modification

In Linux environments, user and group management is crucial for access control and system administration. Adversaries may exploit this by creating or modifying accounts to maintain unauthorized access. The detection rule utilizes audit logs to monitor successful user or group changes, flagging potential persistence tactics by correlating specific actions with known threat behaviors.

### Possible investigation steps

- Review the audit logs to identify the specific user or group account that was created or modified, focusing on the event.action field values such as "changed-password", "added-user-account", or "added-group-account-to".
- Check the timestamp of the event to determine when the account change occurred and correlate it with any other suspicious activities or alerts around the same time.
- Investigate the source of the event by examining the host information, particularly the host.os.type field, to understand which system the changes were made on.
- Identify the user or process that initiated the account change by reviewing the associated user information in the audit logs, which may provide insights into whether the action was authorized or potentially malicious.
- Cross-reference the identified user or group changes with known threat actor behaviors or recent incidents to assess if the activity aligns with any known persistence tactics.

### False positive analysis

- Routine administrative tasks may trigger alerts when system administrators create or modify user or group accounts as part of regular maintenance. To manage this, consider creating exceptions for known administrative accounts or scheduled maintenance windows.
- Automated scripts or configuration management tools that manage user accounts can generate false positives. Identify these tools and exclude their actions from triggering alerts by whitelisting their processes or user accounts.
- System updates or software installations that require user or group modifications might be flagged. Review the context of these changes and exclude specific update processes or installation scripts from the rule.
- Temporary user accounts created for short-term projects or testing purposes can be mistaken for unauthorized access attempts. Implement a naming convention for temporary accounts and exclude them from the rule to reduce noise.
- Changes made by trusted third-party services or applications that integrate with the system may appear suspicious. Verify these services and add them to an exception list to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Review the audit logs to identify the specific user or group accounts that were created or modified, and disable or remove any unauthorized accounts.
- Reset passwords for any compromised or suspicious accounts to prevent further unauthorized access.
- Conduct a thorough review of system and application logs to identify any additional unauthorized changes or suspicious activities that may have occurred.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems have been compromised.
- Implement additional monitoring on the affected system and similar systems to detect any further unauthorized account activities.
- Review and update access control policies and procedures to prevent similar incidents in the future, ensuring that only authorized personnel have the ability to create or modify user and group accounts.
