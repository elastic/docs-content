---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Successful SSH Authentication from Unusual IP Address" prebuilt detection rule.
---

# Successful SSH Authentication from Unusual IP Address

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Successful SSH Authentication from Unusual IP Address

Secure Shell (SSH) is a protocol used to securely access and manage Linux systems. Adversaries may exploit SSH by using stolen credentials to gain unauthorized access. The detection rule identifies successful logins from IPs not seen in the past 10 days, flagging potential intrusions. This approach helps in spotting unusual access patterns that could indicate compromised accounts.

### Possible investigation steps

- Review the IP address flagged in the alert to determine its geolocation and assess if it aligns with expected access patterns for the user account involved.
- Check historical authentication logs for the user account to identify any other unusual or unauthorized access attempts, focusing on the event.category:authentication and event.action:ssh_login fields.
- Investigate the user account's recent activity on the system to identify any suspicious commands or actions executed post-authentication.
- Correlate the flagged IP address with known threat intelligence sources to determine if it is associated with any malicious activity or previously reported incidents.
- Contact the user associated with the account to verify if they recognize the login attempt and if they have recently accessed the system from a new location or device.

### False positive analysis

- New employee or contractor access from a previously unseen IP address may trigger the rule. Regularly update the list of known IP addresses for new users to prevent unnecessary alerts.
- Remote workers or employees traveling may log in from different IP addresses. Implement a process to whitelist IP ranges associated with common travel destinations or VPNs used by the organization.
- Automated scripts or services that occasionally run from different IPs can cause false positives. Identify and document these services, then create exceptions for their known IP addresses.
- Cloud-based infrastructure changes, such as new instances or containers, might authenticate from new IPs. Maintain an updated inventory of cloud resources and their expected IP ranges to adjust the rule accordingly.
- Third-party vendors accessing systems for maintenance or support might use different IPs. Establish a protocol for temporary exceptions for vendor IPs during their access periods.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the attacker.
- Verify the legitimacy of the login by contacting the account owner to confirm whether the access was authorized. If unauthorized, proceed with further steps.
- Change the password of the compromised account and any other accounts that may have been accessed using the same credentials.
- Review and analyze the system logs for any additional suspicious activity or changes made during the unauthorized access period.
- Escalate the incident to the security operations team for a thorough investigation and to determine if further systems are affected.
- Implement IP whitelisting or geofencing to restrict SSH access to known and trusted IP addresses only.
- Update and enhance monitoring rules to detect similar unauthorized access attempts in the future, ensuring that alerts are promptly reviewed and acted upon.

