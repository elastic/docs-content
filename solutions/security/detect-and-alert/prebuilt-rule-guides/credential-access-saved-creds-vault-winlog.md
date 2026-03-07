---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Multiple Vault Web Credentials Read" prebuilt detection rule.'
---

# Multiple Vault Web Credentials Read

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Multiple Vault Web Credentials Read

Windows Credential Manager stores credentials for web logins, apps, and networks, facilitating seamless user access. Adversaries exploit this by extracting stored credentials, potentially aiding lateral movement within networks. The detection rule identifies suspicious activity by flagging consecutive credential reads from the same process, excluding benign actions like localhost access, thus highlighting potential credential dumping attempts.

### Possible investigation steps

- Review the process associated with the flagged PID to determine if it is a legitimate application or potentially malicious. Check for known software or unusual executables.
- Investigate the source and destination of the web credentials read by examining the winlog.event_data.Resource field to identify any suspicious or unexpected URLs.
- Check the winlog.computer_name to identify the affected system and assess whether it is a high-value target or has been involved in previous suspicious activities.
- Analyze the timeline of events around the alert to identify any preceding or subsequent suspicious activities that may indicate a broader attack pattern.
- Verify the user context by examining the winlog.event_data.SubjectLogonId to ensure the activity was not performed by a privileged or administrative account without proper authorization.
- Cross-reference the event with other security logs or alerts to identify any correlated activities that might suggest a coordinated attack or compromise.

### False positive analysis

- Localhost access is a common false positive since the rule excludes localhost reads. Ensure that any legitimate applications accessing credentials via localhost are properly whitelisted to prevent unnecessary alerts.
- Automated scripts or applications that frequently access web credentials for legitimate purposes may trigger the rule. Identify these processes and create exceptions for them to reduce noise.
- System maintenance or updates might involve credential reads that are benign. Coordinate with IT teams to schedule these activities and temporarily adjust the rule sensitivity or add exceptions during these periods.
- Security tools or monitoring software that perform regular checks on credential integrity could be flagged. Verify these tools and add them to an exception list if they are part of the organization's security infrastructure.
- User behavior such as frequent password changes or credential updates might cause alerts. Educate users on the impact of their actions and consider adjusting the rule to accommodate expected behavior patterns.

### Response and remediation

- Isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate the suspicious process identified by the process ID (pid) involved in the credential reads to stop further credential access.
- Conduct a thorough review of the affected system for any additional signs of compromise, such as unauthorized user accounts or scheduled tasks.
- Change passwords for any accounts that may have been exposed, focusing on those stored in the Windows Credential Manager.
- Implement network segmentation to limit access to critical systems and data, reducing the risk of lateral movement.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the breach.
- Enhance monitoring and logging on the affected system and similar endpoints to detect any future attempts at credential dumping or unauthorized access.
