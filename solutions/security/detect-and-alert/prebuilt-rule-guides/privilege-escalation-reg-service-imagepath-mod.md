---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Privilege Escalation via Service ImagePath Modification" prebuilt detection rule.'
---

# Potential Privilege Escalation via Service ImagePath Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation via Service ImagePath Modification

Windows services are crucial for system operations, often running with high privileges. Adversaries exploit this by altering the ImagePath registry key of services to execute malicious code with elevated privileges. The detection rule identifies suspicious modifications to service ImagePaths, focusing on changes that deviate from standard executable paths, thus flagging potential privilege escalation attempts.

### Possible investigation steps

- Review the specific registry key and value that triggered the alert to confirm it matches one of the monitored service keys, such as those listed in the query (e.g., *\LanmanServer, *\Winmgmt).
- Examine the modified ImagePath value to determine if it points to a non-standard executable path or a suspicious executable, especially those not located in %systemroot%\system32\.
- Check the process.executable field to identify the process responsible for the registry modification and assess its legitimacy.
- Investigate the user account associated with the modification event to determine if it has elevated privileges, such as membership in the Server Operators group.
- Correlate the event with other logs or alerts to identify any related suspicious activities, such as unexpected service starts or process executions.
- Review recent changes or activities on the host to identify any unauthorized access or configuration changes that could indicate a broader compromise.

### False positive analysis

- Legitimate software updates or installations may modify service ImagePaths. Users can create exceptions for known update processes or installation paths to prevent false positives.
- System administrators might intentionally change service configurations for maintenance or troubleshooting. Document and exclude these changes by adding exceptions for specific administrator actions or paths.
- Custom scripts or automation tools that modify service settings as part of their operation can trigger alerts. Identify and whitelist these scripts or tools to avoid unnecessary alerts.
- Some third-party security or management software may alter service ImagePaths as part of their functionality. Verify the legitimacy of such software and exclude their known paths from detection.
- Changes made by trusted IT personnel during system configuration or optimization should be logged and excluded from alerts to reduce noise.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes identified as running from non-standard executable paths, especially those not originating from the system32 directory.
- Restore the modified ImagePath registry key to its original state using a known good configuration or backup.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or persistence mechanisms.
- Review and audit user accounts and group memberships, particularly those with elevated privileges like Server Operators, to ensure no unauthorized changes have been made.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for future modifications to service ImagePath registry keys, focusing on deviations from standard paths to detect similar threats promptly.
