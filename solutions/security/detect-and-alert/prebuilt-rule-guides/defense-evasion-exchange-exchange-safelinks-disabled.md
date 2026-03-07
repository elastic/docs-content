---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Exchange Email Safe Link Policy Disabled" prebuilt detection rule.
---

# M365 Exchange Email Safe Link Policy Disabled

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating M365 Exchange Email Safe Link Policy Disabled

Microsoft 365's Safe Link policies enhance security by scanning hyperlinks in documents for phishing threats, even post-delivery. Disabling these policies can expose users to phishing attacks. Adversaries might exploit this by disabling Safe Links to facilitate malicious link delivery. The detection rule identifies successful attempts to disable Safe Link policies, signaling potential security breaches.

### Possible investigation steps

- Review the event logs for the specific event.dataset:o365.audit and event.provider:Exchange to confirm the occurrence of the "Disable-SafeLinksRule" action with a successful outcome.
- Identify the user account associated with the event.action:"Disable-SafeLinksRule" to determine if the action was performed by an authorized individual or if the account may have been compromised.
- Check the recent activity of the identified user account for any unusual or unauthorized actions that could indicate a broader security incident.
- Investigate any recent changes to Safe Link policies in the Microsoft 365 environment to understand the scope and impact of the policy being disabled.
- Assess whether there have been any recent phishing attempts or suspicious emails delivered to users, which could exploit the disabled Safe Link policy.
- Coordinate with the IT security team to re-enable the Safe Link policy and implement additional monitoring to prevent future unauthorized changes.

### False positive analysis

- Administrative changes: Legitimate administrative actions may involve disabling Safe Link policies temporarily for testing or configuration purposes. To manage this, create exceptions for known administrative accounts or scheduled maintenance windows.
- Third-party integrations: Some third-party security tools or integrations might require Safe Link policies to be disabled for compatibility reasons. Identify and document these tools, and set up exceptions for their associated actions.
- Policy updates: During policy updates or migrations, Safe Link policies might be disabled as part of the process. Monitor and document these events, and exclude them from alerts if they match known update patterns.
- User training sessions: Safe Link policies might be disabled during user training or demonstrations to showcase potential threats. Schedule these sessions and exclude related activities from triggering alerts.

### Response and remediation

- Immediately re-enable the Safe Link policy in Microsoft 365 to restore phishing protection for hyperlinks in documents.
- Conduct a thorough review of recent email and document deliveries to identify any potentially malicious links that may have been delivered while the Safe Link policy was disabled.
- Isolate any identified malicious links or documents and notify affected users to prevent interaction with these threats.
- Investigate the account or process that disabled the Safe Link policy to determine if it was compromised or misused, and take appropriate actions such as password resets or privilege revocation.
- Escalate the incident to the security operations team for further analysis and to determine if additional security measures are needed to prevent similar incidents.
- Implement additional monitoring and alerting for changes to Safe Link policies to ensure rapid detection of any future unauthorized modifications.
- Review and update access controls and permissions related to Safe Link policy management to ensure only authorized personnel can make changes.

## Setup

The Office 365 Logs Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
