---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Successful Application SSO from Rare Unknown Client Device" prebuilt detection rule.
---

# Successful Application SSO from Rare Unknown Client Device

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Successful Application SSO from Rare Unknown Client Device

Single sign-on (SSO) streamlines user access across applications by using a single set of credentials. However, adversaries can exploit vulnerabilities in SSO systems, like Okta's, to bypass security policies using stolen credentials. The detection rule identifies unusual SSO events from unknown devices, signaling potential unauthorized access attempts, thus helping to mitigate risks associated with credential theft.

### Possible investigation steps

- Review the event details in the alert to confirm the presence of the "Unknown" or "unknown" client device in the okta.client.device field.
- Check the user-agent string associated with the event to gather more information about the unknown device and assess if it matches any known legitimate devices used by the user.
- Investigate the user's recent login history and patterns to identify any anomalies or deviations from their typical behavior, such as unusual login times or locations.
- Verify if there have been any recent changes to the user's account, such as password resets or modifications to multi-factor authentication settings, which could indicate account compromise.
- Cross-reference the IP address associated with the SSO event against known malicious IP databases or internal threat intelligence to identify potential threats.
- Contact the user to confirm whether they recognize the login activity and the device used, ensuring it was an authorized access attempt.

### False positive analysis

- Employees using new or updated devices may trigger false positives. Regularly update the list of recognized devices to include these changes.
- Legitimate users accessing applications from different locations or networks, such as while traveling, can appear as unknown devices. Implement geolocation checks and allow exceptions for known travel patterns.
- Software updates or changes in user-agent strings can cause devices to be misidentified. Monitor for consistent patterns and adjust the rule to accommodate these variations.
- Shared devices in environments like conference rooms or labs may not have unique identifiers. Establish a process to register these shared devices to prevent them from being flagged.
- Temporary network issues causing devices to appear as unknown can lead to false positives. Correlate with network logs to verify if the device is indeed unknown or if it was a transient issue.

### Response and remediation

- Immediately isolate the affected user account by disabling it to prevent further unauthorized access.
- Conduct a thorough review of the affected user's recent activity across all Okta-integrated applications to identify any unauthorized actions or data access.
- Reset the affected user's credentials and enforce a password change, ensuring the new password adheres to strong security policies.
- Implement multi-factor authentication (MFA) for the affected user account if not already in place, to add an additional layer of security.
- Notify the security team and relevant stakeholders about the incident for awareness and further investigation.
- Review and update Okta's device recognition policies to improve detection of unknown or rare devices, reducing the risk of similar incidents.
- Monitor for any further suspicious SSO activities from unknown devices and escalate to the incident response team if additional alerts are triggered.
