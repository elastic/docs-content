---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Linux Network Configuration Discovery" prebuilt detection rule.
---

# Unusual Linux Network Configuration Discovery

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Linux Network Configuration Discovery

In Linux environments, network configuration tools are essential for managing and troubleshooting network settings. Adversaries may exploit these tools to gather network details, aiding in lateral movement or further reconnaissance. The detection rule leverages machine learning to identify atypical usage patterns of network commands by unexpected users, signaling potential account compromise or unauthorized network probing.

### Possible investigation steps

- Review the alert details to identify the specific network configuration commands executed and the user account involved. Focus on commands that are typically used for network discovery, such as `ifconfig`, `ip`, `netstat`, or `route`.
- Check the user's login history and session details to determine if the account activity aligns with the user's normal behavior or if there are signs of unauthorized access, such as logins from unusual IP addresses or at odd times.
- Investigate the user's role and responsibilities to assess whether they have a legitimate reason to perform network configuration discovery. This can help determine if the activity is expected or suspicious.
- Examine recent changes in user permissions or group memberships that might have allowed the execution of network configuration commands by an unexpected user.
- Correlate the alert with other security events or logs, such as authentication logs, to identify any related suspicious activities, such as failed login attempts or privilege escalation attempts.
- If the account is suspected to be compromised, initiate a password reset and review the system for any signs of further compromise or malicious activity, such as unauthorized software installations or data exfiltration attempts.

### False positive analysis

- Routine administrative tasks by system administrators may trigger the rule. To manage this, create exceptions for known admin accounts performing regular network configuration checks.
- Automated scripts or cron jobs that perform network diagnostics can be mistaken for unusual activity. Identify and whitelist these scripts to prevent false alerts.
- Network monitoring tools running under specific service accounts might be flagged. Ensure these service accounts are documented and excluded from the rule.
- Developers or IT staff conducting legitimate troubleshooting in non-production environments may cause alerts. Establish a process to temporarily exclude these users during known maintenance windows.
- New employees or contractors performing onboarding tasks might trigger the rule. Implement a review process to quickly assess and exclude these cases if they are verified as non-threatening.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes or sessions initiated by the unusual user to halt ongoing reconnaissance activities.
- Conduct a thorough review of the affected user's account for signs of compromise, such as unauthorized access attempts or changes in user privileges.
- Reset the credentials of the compromised account and enforce multi-factor authentication to prevent future unauthorized access.
- Analyze network logs and system activity to identify any additional systems that may have been accessed or probed by the adversary.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional containment measures are necessary.
- Update detection mechanisms to include newly identified indicators of compromise (IOCs) and enhance monitoring for similar unusual network configuration discovery activities.
