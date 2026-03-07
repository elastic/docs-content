---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Windows User Privilege Elevation Activity" prebuilt detection rule.
---

# Unusual Windows User Privilege Elevation Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Windows User Privilege Elevation Activity

In Windows environments, privilege elevation tools like 'runas' allow users to execute programs with different user credentials, typically used by administrators. Adversaries exploit this to gain elevated access, often indicating account compromise. The detection rule leverages machine learning to identify atypical usage patterns of such tools, flagging potential unauthorized privilege escalation attempts.

### Possible investigation steps

- Review the specific user account involved in the alert to determine if it is a regular user or an administrator, as privilege elevation is more common among administrators.
- Check the timestamp of the alert to correlate with any known scheduled tasks or administrative activities that might explain the use of privilege elevation tools.
- Investigate the source IP address and device from which the privilege elevation attempt was made to verify if it aligns with the user's typical access patterns.
- Examine recent login activity for the user account to identify any unusual or unauthorized access attempts that could indicate account compromise.
- Look for any other security alerts or logs related to the same user or device around the time of the alert to gather additional context on potential malicious activity.
- Assess whether there have been any recent changes to user permissions or group memberships that could have facilitated the privilege elevation.

### False positive analysis

- Regular administrative tasks by domain or network administrators can trigger false positives. To manage this, create exceptions for known administrator accounts frequently using the runas command.
- Scheduled tasks or scripts that require privilege elevation might be flagged. Identify and exclude these tasks from monitoring if they are verified as safe and necessary for operations.
- Software updates or installations that require elevated privileges can also cause alerts. Maintain a list of approved software and update processes to exclude them from triggering the rule.
- Training or testing environments where privilege elevation is part of routine operations may generate false positives. Exclude these environments from the rule's scope to prevent unnecessary alerts.
- Third-party applications that use privilege elevation for legitimate purposes should be reviewed and, if deemed safe, added to an exception list to avoid repeated false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Revoke any elevated privileges granted to the compromised account and reset its password to prevent further misuse.
- Conduct a thorough review of recent activity logs for the affected account to identify any unauthorized actions or data access.
- Notify the security team and relevant stakeholders about the incident for awareness and potential escalation.
- Restore any altered or compromised system configurations to their original state using backups or system snapshots.
- Implement additional monitoring on the affected system and account to detect any further suspicious activity.
- Review and update access controls and privilege management policies to minimize the risk of similar incidents in the future.
