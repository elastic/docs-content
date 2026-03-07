---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Reset MFA Factors for an Okta User Account" prebuilt detection rule.
---

# Attempt to Reset MFA Factors for an Okta User Account

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Reset MFA Factors for an Okta User Account

Okta is a widely used identity management service that provides multi-factor authentication (MFA) to enhance security. Adversaries may attempt to reset MFA factors to register their own, gaining unauthorized access while appearing legitimate. The detection rule identifies such attempts by monitoring specific Okta system events, helping to flag potential account manipulation activities.

### Possible investigation steps

- Review the Okta system logs for the specific event.action:user.mfa.factor.reset_all to identify the user account involved in the MFA reset attempt.
- Check the timestamp of the event to determine when the reset attempt occurred and correlate it with any other suspicious activities around the same time.
- Investigate the IP address and location associated with the event to assess if it aligns with the user's typical access patterns or if it appears unusual.
- Examine the user account's recent activity history for any anomalies or unauthorized access attempts that might indicate compromise.
- Verify if there have been any recent changes to the user's account settings or permissions that could suggest account manipulation.
- Contact the affected user to confirm whether they initiated the MFA reset or if it was unauthorized, and advise them on securing their account if necessary.

### False positive analysis

- Routine administrative actions may trigger the rule if IT staff reset MFA factors for legitimate reasons such as assisting users who have lost access to their MFA devices. To manage this, create exceptions for known IT personnel or specific administrative actions.
- User-initiated resets due to lost or changed devices can also appear as suspicious activity. Implement a process to verify user requests and document these instances to differentiate them from malicious attempts.
- Automated scripts or tools used for account management might reset MFA factors as part of their operations. Identify and whitelist these tools to prevent false positives.
- Scheduled security audits or compliance checks that involve resetting MFA factors should be documented and excluded from triggering alerts by setting up time-based exceptions during these activities.

### Response and remediation

- Immediately disable the affected Okta user account to prevent further unauthorized access.
- Review recent login activity and MFA changes for the affected account to identify any unauthorized access or suspicious behavior.
- Reset the MFA factors for the affected account and ensure that only the legitimate user can re-enroll their MFA devices.
- Notify the legitimate user of the account compromise and advise them to change their password and review their account activity.
- Conduct a security review of the affected user's permissions and access to sensitive resources to ensure no unauthorized changes were made.
- Escalate the incident to the security operations team for further investigation and to determine if other accounts may be affected.
- Update security monitoring and alerting to enhance detection of similar MFA reset attempts, leveraging the MITRE ATT&CK framework for guidance on persistence and account manipulation tactics.

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
