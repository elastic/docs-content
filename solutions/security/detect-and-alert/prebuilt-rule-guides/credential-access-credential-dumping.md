---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Linux Credential Dumping via Unshadow" prebuilt detection rule.
---

# Potential Linux Credential Dumping via Unshadow

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Linux Credential Dumping via Unshadow

Unshadow is a utility within the John the Ripper suite, used to merge `/etc/shadow` and `/etc/passwd` files, making them vulnerable to password cracking. Adversaries exploit this to extract and crack user credentials, gaining unauthorized access. The detection rule identifies suspicious execution of Unshadow by monitoring process activities, focusing on specific execution patterns and argument counts, thus flagging potential credential dumping attempts.

### Possible investigation steps

- Review the process execution details to confirm the presence of the unshadow utility by checking the process name and arguments, ensuring that the process.args_count is 3 or more.
- Investigate the user account under which the unshadow process was executed to determine if it aligns with expected administrative activities or if it indicates potential unauthorized access.
- Examine the command line arguments used with the unshadow process to identify the specific files targeted, such as /etc/shadow and /etc/passwd, and verify if these files were accessed or modified.
- Check for any subsequent processes or activities that might indicate password cracking attempts, such as the execution of John the Ripper or similar tools, following the unshadow execution.
- Correlate the event with other security alerts or logs from the same host or user to identify any patterns or additional suspicious activities that might suggest a broader attack campaign.
- Assess the risk and impact by determining if any sensitive credentials were potentially exposed and consider implementing additional monitoring or access controls to prevent future incidents.

### False positive analysis

- System administrators or security teams may use the unshadow utility for legitimate auditing or recovery purposes. To handle this, create exceptions for known administrative accounts or specific maintenance windows.
- Automated scripts or backup processes might invoke unshadow as part of routine operations. Identify these scripts and exclude their execution paths or associated user accounts from triggering alerts.
- Security testing or penetration testing activities could involve the use of unshadow. Coordinate with the testing team to whitelist their activities during the testing period to avoid false positives.
- Development or testing environments might have unshadow executed as part of security tool evaluations. Exclude these environments from monitoring or adjust the rule to focus on production systems only.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes related to the unshadow utility to halt ongoing credential dumping activities.
- Conduct a thorough review of the affected system's `/etc/shadow` and `/etc/passwd` files to identify any unauthorized modifications or access.
- Change passwords for all user accounts on the affected system, prioritizing those with elevated privileges, to mitigate the risk of compromised credentials.
- Review and update access controls and permissions for sensitive files, ensuring that only authorized users have access to `/etc/shadow` and `/etc/passwd`.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for similar activities across the network to detect and respond to future credential dumping attempts promptly.
