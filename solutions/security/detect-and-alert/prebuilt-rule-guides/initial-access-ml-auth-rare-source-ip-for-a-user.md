---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Source IP for a User to Logon from" prebuilt detection rule.'
---

# Unusual Source IP for a User to Logon from

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Source IP for a User to Logon from
Machine learning models analyze login patterns to identify atypical IP addresses for users, which may indicate compromised accounts or lateral movement by threat actors. Adversaries exploit valid credentials to access systems from unexpected locations. This detection rule flags such anomalies, aiding in early identification of unauthorized access attempts, thereby enhancing security posture.

### Possible investigation steps

- Review the login details to identify the unusual source IP address and compare it with the user's typical login locations and times.
- Check the geolocation of the unusual IP address to determine if it aligns with any known travel or business activities of the user.
- Analyze the user's recent activity logs to identify any other suspicious behavior or anomalies that might indicate account compromise.
- Investigate if there are any other users or systems that have logged in from the same unusual IP address, which could suggest lateral movement.
- Contact the user to verify if they recognize the login activity and if they have recently traveled or used a VPN that might explain the unusual IP address.
- Cross-reference the unusual IP address with threat intelligence sources to determine if it is associated with known malicious activity.

### False positive analysis

- Users frequently traveling or working remotely may trigger false positives due to legitimate logins from various locations. To manage this, create exceptions for known travel patterns or remote work IP ranges.
- Employees using VPNs or proxy services can appear to log in from unusual IP addresses. Identify and whitelist IP ranges associated with company-approved VPNs or proxies.
- Shared accounts used by multiple users across different locations can generate alerts. Implement stricter access controls or assign unique credentials to each user to reduce false positives.
- Automated systems or scripts that log in from different IP addresses might be flagged. Document and exclude these systems from the rule if they are verified as non-threatening.
- Regularly review and update the list of excluded IP addresses to ensure that only legitimate exceptions are maintained, reducing the risk of overlooking genuine threats.

### Response and remediation

- Immediately isolate the affected user account by disabling it to prevent further unauthorized access.
- Conduct a password reset for the compromised account and ensure the new password adheres to strong security policies.
- Review and terminate any active sessions associated with the unusual IP address to cut off any ongoing unauthorized access.
- Analyze logs to identify any lateral movement or additional compromised accounts and isolate those accounts as necessary.
- Notify the user of the suspicious activity and verify if they recognize the unusual IP address or if they have recently traveled.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or accounts have been affected.
- Implement IP whitelisting or geofencing rules to restrict access from unexpected locations, enhancing future detection and prevention.
