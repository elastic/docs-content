---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Dumping Account Hashes via Built-In Commands" prebuilt detection rule.'
---

# Dumping Account Hashes via Built-In Commands

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Dumping Account Hashes via Built-In Commands

In macOS environments, built-in commands like `defaults` and `mkpassdb` can be exploited by adversaries to extract user account hashes, which are crucial for credential access. These hashes, once obtained, can be cracked to reveal passwords or used for lateral movement within a network. The detection rule identifies suspicious process executions involving these commands and specific arguments, signaling potential credential dumping activities.

### Possible investigation steps

- Review the process execution details to confirm the presence of the `defaults` or `mkpassdb` commands with arguments like `ShadowHashData` or `-dump`, as these are indicative of credential dumping attempts.
- Identify the user account associated with the process execution to determine if the activity aligns with expected behavior for that user or if it appears suspicious.
- Check the historical activity of the involved user account and the host to identify any patterns or anomalies that could suggest unauthorized access or lateral movement.
- Investigate any network connections or subsequent processes initiated by the suspicious process to assess potential data exfiltration or further malicious actions.
- Correlate the event with other security alerts or logs from the same host or user account to build a comprehensive timeline of the activity and assess the scope of the potential compromise.

### False positive analysis

- System administrators or security tools may legitimately use the `defaults` or `mkpassdb` commands for system maintenance or auditing purposes. To manage these, create exceptions for known administrative accounts or tools that regularly execute these commands.
- Automated scripts or management software might invoke these commands as part of routine operations. Identify and whitelist these scripts or software to prevent unnecessary alerts.
- Developers or IT personnel might use these commands during testing or development phases. Establish a process to temporarily exclude these activities by setting up time-bound exceptions for specific user accounts or devices.
- Security assessments or penetration tests could trigger this rule. Coordinate with security teams to schedule and document these activities, allowing for temporary rule adjustments during the testing period.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further lateral movement or data exfiltration.
- Terminate any suspicious processes identified as using the `defaults` or `mkpassdb` commands with the specified arguments to halt ongoing credential dumping activities.
- Conduct a thorough review of user accounts on the affected system to identify any unauthorized access or changes, focusing on accounts with elevated privileges.
- Reset passwords for all potentially compromised accounts, especially those with administrative access, and enforce strong password policies.
- Analyze system logs and network traffic to identify any additional systems that may have been accessed using the compromised credentials, and apply similar containment measures.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the full scope of the breach.
- Implement enhanced monitoring and alerting for similar suspicious activities across the network to detect and respond to future attempts promptly.
