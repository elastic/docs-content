---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "TCC Bypass via Mounted APFS Snapshot Access" prebuilt detection rule.'
---

# TCC Bypass via Mounted APFS Snapshot Access

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating TCC Bypass via Mounted APFS Snapshot Access

Apple's TCC framework safeguards user data by controlling app access to sensitive files. Adversaries exploit APFS snapshots, mounting them with specific flags to bypass these controls, gaining unauthorized access to protected data. The detection rule identifies this misuse by monitoring the execution of the `mount_apfs` command with parameters indicative of such bypass attempts, flagging potential security breaches.

### Possible investigation steps

- Review the process execution details to confirm the presence of the `mount_apfs` command with the specific arguments `/System/Volumes/Data` and `noowners` to verify the alert's accuracy.
- Investigate the user account associated with the process execution to determine if the activity aligns with expected behavior or if it indicates potential unauthorized access.
- Examine the timeline of events leading up to and following the alert to identify any related suspicious activities or processes that may indicate a broader attack or compromise.
- Check for any recent changes or anomalies in system configurations or user permissions that could have facilitated the bypass attempt.
- Correlate the alert with other security logs or alerts to assess if this is part of a larger pattern of malicious behavior or an isolated incident.

### False positive analysis

- System maintenance tools or backup software may legitimately use the mount_apfs command with the noowners flag for routine operations. Users can create exceptions for these specific tools by identifying their process names or paths and excluding them from the detection rule.
- Developers or IT administrators might use the mount_apfs command during testing or troubleshooting. To prevent these activities from triggering false positives, users can whitelist specific user accounts or IP addresses associated with these roles.
- Automated scripts or scheduled tasks that require access to APFS snapshots for legitimate purposes might trigger the rule. Users should review these scripts and, if deemed safe, add them to an exclusion list based on their unique identifiers or execution context.
- Security software or monitoring tools that perform regular checks on file system integrity might inadvertently match the rule's criteria. Users can mitigate this by identifying these tools and excluding their specific process signatures from the detection parameters.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes related to the `mount_apfs` command to halt ongoing unauthorized access attempts.
- Conduct a thorough review of system logs and user activity to identify any data accessed or exfiltrated during the breach.
- Restore any compromised files from a known good backup to ensure data integrity and security.
- Update macOS and all installed applications to the latest versions to patch any vulnerabilities that may have been exploited.
- Implement stricter access controls and monitoring for APFS snapshot usage to prevent similar bypass attempts in the future.
- Escalate the incident to the security operations center (SOC) or relevant IT security team for further investigation and to assess the need for additional security measures.
