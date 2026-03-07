---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Spike in User Account Management Events" prebuilt detection rule.'
---

# Spike in User Account Management Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in User Account Management Events

The detection rule leverages machine learning to identify unusual spikes in user account management activities, such as account creation or modification, which may indicate privilege escalation attempts. Adversaries exploit these activities to gain unauthorized access or elevate privileges. By analyzing patterns and deviations from normal behavior, the rule helps detect potential misuse, enabling timely intervention.

### Possible investigation steps

- Review the specific user account(s) involved in the spike to determine if the activity aligns with their typical behavior or role within the organization.
- Examine the timestamps of the account management events to identify any patterns or anomalies, such as activity occurring outside of normal business hours.
- Check for any recent changes in user permissions or roles that could explain the spike in account management events.
- Investigate any associated IP addresses or devices used during the account management activities to determine if they are known and trusted within the organization.
- Look for any correlated alerts or logs that might indicate concurrent suspicious activities, such as failed login attempts or access to sensitive resources.
- Consult with the user or their manager to verify if the account management activities were authorized and legitimate.

### False positive analysis

- Routine administrative tasks can trigger spikes in user account management events. Regularly scheduled account audits or bulk updates by IT staff may appear as unusual activity. To manage this, create exceptions for known maintenance periods or specific administrative accounts.
- Automated scripts or tools used for user provisioning and de-provisioning can cause false positives. Identify these scripts and exclude their activity from the rule to prevent unnecessary alerts.
- Onboarding or offboarding processes that involve creating or deleting multiple user accounts in a short period can be mistaken for privilege escalation attempts. Document these processes and adjust the rule to recognize these patterns as normal behavior.
- Changes in organizational structure, such as mergers or departmental shifts, may lead to increased account management activities. Update the rule to accommodate these changes by temporarily adjusting thresholds or excluding specific user groups during transition periods.

### Response and remediation

- Immediately isolate the affected user account to prevent further unauthorized access or privilege escalation. This can be done by disabling the account or changing its password.
- Review recent account management activities for the affected user to identify any unauthorized changes or suspicious patterns. This includes checking for new account creations, modifications, or deletions.
- Conduct a thorough audit of the affected system and network segment to identify any additional compromised accounts or systems. Look for signs of lateral movement or further exploitation attempts.
- Revert any unauthorized changes made to user accounts or system configurations to their original state, ensuring that no backdoors or unauthorized access points remain.
- Notify the security team and relevant stakeholders about the incident, providing them with details of the spike in user account management events and any identified malicious activities.
- Implement additional monitoring and alerting for the affected user account and related systems to detect any further suspicious activities promptly.
- Review and update access controls and user account management policies to prevent similar incidents in the future, ensuring that only authorized personnel have the necessary privileges.
