---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Activity Reported by Okta User" prebuilt detection rule.'
---

# Suspicious Activity Reported by Okta User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Activity Reported by Okta User

Okta is a widely used identity management service that facilitates secure user authentication and access control. Adversaries may exploit compromised credentials to gain unauthorized access, posing a threat to network security. The detection rule monitors for user-reported suspicious activity, signaling potential unauthorized access attempts. By analyzing these alerts, security teams can swiftly identify and mitigate threats, leveraging Okta's logging capabilities to trace and respond to malicious actions.

### Possible investigation steps

- Review the specific event details in the Okta logs where event.dataset is okta.system and event.action is user.account.report_suspicious_activity_by_enduser to gather initial context about the reported activity.
- Identify the user who reported the suspicious activity and check their recent login history and access patterns for any anomalies or deviations from their typical behavior.
- Correlate the reported suspicious activity with other security logs and alerts to determine if there are any related incidents or patterns indicating a broader attack.
- Verify if there are any known vulnerabilities or compromised credentials associated with the user's account that could have been exploited.
- Contact the user to gather additional information about the suspicious activity they observed and confirm whether they recognize any recent access attempts or changes to their account.
- Assess the risk and potential impact of the suspicious activity on the network and determine if any immediate containment or remediation actions are necessary.

### False positive analysis

- Users frequently accessing their accounts from new devices or locations may trigger false positives. Implement geofencing or device recognition to reduce these alerts.
- Routine administrative actions, such as password resets or account updates, might be misinterpreted as suspicious. Exclude these actions from alerts if they are performed by known administrators.
- Automated scripts or applications using service accounts can generate alerts if not properly configured. Ensure these accounts are whitelisted or have appropriate permissions set.
- Employees using VPNs or proxy services for remote work can cause location-based false positives. Consider marking known VPN IP addresses as safe.
- High-volume login attempts from legitimate users, such as during password recovery, can be mistaken for suspicious activity. Monitor for patterns and adjust thresholds accordingly.

### Response and remediation

- Immediately isolate the affected user account by temporarily disabling it to prevent further unauthorized access.
- Notify the user and relevant stakeholders about the suspicious activity and the actions being taken to secure the account.
- Conduct a password reset for the affected user account and enforce multi-factor authentication (MFA) if not already enabled.
- Review recent login activity and access logs for the affected account to identify any unauthorized access or data exfiltration attempts.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if other accounts or systems have been compromised.
- Implement additional monitoring on the affected account and related systems to detect any further suspicious activity.
- Update security policies and procedures based on findings to prevent similar incidents in the future, ensuring alignment with MITRE ATT&CK framework recommendations for Initial Access and Valid Accounts.

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
