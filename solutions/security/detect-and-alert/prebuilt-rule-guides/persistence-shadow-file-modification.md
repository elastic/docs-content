---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Shadow File Modification by Unusual Process" prebuilt detection rule.
---

# Shadow File Modification by Unusual Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Shadow File Modification by Unusual Process

The Linux shadow file is crucial for storing hashed user passwords, ensuring system security. Adversaries may exploit this by altering the file to add users or change passwords, thus gaining unauthorized access or maintaining persistence. The detection rule identifies suspicious modifications by monitoring changes and renames of the shadow file, flagging potential unauthorized access attempts for further investigation.

### Possible investigation steps

- Review the alert details to confirm the event type is "change" and the action is "rename" for the file path "/etc/shadow".
- Check the file.Ext.original.path to identify the original location of the shadow file before the rename event.
- Investigate recent user account changes or additions by examining system logs and user management commands executed around the time of the alert.
- Analyze the history of commands executed by users with elevated privileges to identify any unauthorized or suspicious activities.
- Correlate the event with other security alerts or logs to determine if there are additional indicators of compromise or persistence tactics being employed.
- Verify the integrity of the shadow file by comparing its current state with a known good backup to detect unauthorized modifications.

### False positive analysis

- System updates or package installations may trigger legitimate changes to the shadow file. Users can create exceptions for known update processes or package managers to prevent these from being flagged.
- Administrative tasks performed by authorized personnel, such as password changes or user management, can also result in shadow file modifications. Implementing a whitelist for specific user accounts or processes that are known to perform these tasks can reduce false positives.
- Backup or restoration processes that involve the shadow file might cause rename events. Users should identify and exclude these processes if they are part of regular system maintenance.
- Automated scripts or configuration management tools that manage user accounts could lead to expected changes in the shadow file. Users should ensure these tools are recognized and excluded from triggering alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Verify the integrity of the /etc/shadow file by comparing it with a known good backup to identify unauthorized changes or additions.
- Reset passwords for all user accounts on the affected system, ensuring the use of strong, unique passwords to mitigate the risk of compromised credentials.
- Review and remove any unauthorized user accounts that may have been added to the system, ensuring that only legitimate users have access.
- Conduct a thorough audit of system logs and user activity to identify any additional signs of compromise or persistence mechanisms employed by the threat actor.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
- Implement enhanced monitoring and alerting for future modifications to the /etc/shadow file to quickly detect and respond to similar threats.
