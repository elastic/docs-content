---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Spike in User Lifecycle Management Change Events" prebuilt detection rule.'
---

# Spike in User Lifecycle Management Change Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in User Lifecycle Management Change Events

User lifecycle management in environments like Okta involves creating, modifying, and deleting user accounts. Adversaries may exploit this by manipulating accounts to escalate privileges or maintain access. The detection rule leverages machine learning to identify unusual spikes in these events, signaling potential misuse. By focusing on anomalies, it aids in early detection of privilege escalation tactics.

### Possible investigation steps

- Review the specific user accounts involved in the lifecycle management change events to identify any patterns or anomalies, such as multiple changes in a short period or changes made by unusual sources.
- Check the timestamps of the change events to determine if they align with normal business hours or if they occurred during unusual times, which might indicate suspicious activity.
- Investigate the source IP addresses and locations associated with the change events to identify any unusual or unauthorized access points.
- Examine the types of changes made to the user accounts, such as privilege escalations or role modifications, to assess if they align with legitimate business needs.
- Cross-reference the user accounts involved with recent security alerts or incidents to determine if they have been previously flagged for suspicious activity.
- Consult with the account owners or relevant department heads to verify if the changes were authorized and necessary for business operations.

### False positive analysis

- Routine administrative tasks such as bulk user account updates or scheduled maintenance can trigger spikes in user lifecycle management events. To manage this, create exceptions for known maintenance windows or bulk operations.
- Automated processes or scripts that regularly modify user accounts may cause false positives. Identify these processes and exclude them from the detection rule to prevent unnecessary alerts.
- Onboarding or offboarding periods with high user account activity can lead to spikes. Adjust the detection thresholds temporarily during these periods or exclude specific user groups involved in these activities.
- Integration with third-party applications that frequently update user attributes might result in false positives. Review and whitelist these applications to reduce noise in the detection system.

### Response and remediation

- Immediately isolate the affected user accounts to prevent further unauthorized access or privilege escalation. This can be done by disabling the accounts or changing their passwords.
- Review and revoke any unauthorized permissions or roles that were assigned during the spike in user lifecycle management change events. Ensure that only legitimate access rights are restored.
- Conduct a thorough audit of recent user account changes to identify any additional accounts that may have been manipulated. Pay special attention to accounts with elevated privileges.
- Notify the security team and relevant stakeholders about the incident to ensure awareness and coordination for further investigation and response.
- Implement additional monitoring on the affected accounts and related systems to detect any further suspicious activity or attempts to regain unauthorized access.
- Escalate the incident to higher-level security management if the scope of the breach is extensive or if sensitive data may have been compromised.
- Review and update access management policies and procedures to prevent similar incidents in the future, ensuring that changes to user accounts are logged and regularly reviewed.
