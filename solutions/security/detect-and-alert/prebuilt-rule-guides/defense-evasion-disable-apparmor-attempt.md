---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Disabling of AppArmor" prebuilt detection rule.'
---

# Potential Disabling of AppArmor

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Disabling of AppArmor

AppArmor is a Linux security module that enforces strict access controls, limiting what applications can do. Adversaries may attempt to disable AppArmor to evade detection and freely execute malicious activities. The detection rule identifies suspicious processes attempting to stop or disable AppArmor services, such as using commands like `systemctl` or `service` with specific arguments, indicating potential tampering with security defenses.

### Possible investigation steps

- Review the process details to confirm the command used, focusing on the process name and arguments, such as "systemctl", "service", "chkconfig", or "ln" with arguments related to AppArmor.
- Check the user account associated with the process execution to determine if it is a legitimate user or potentially compromised.
- Investigate the host's recent activity logs to identify any other suspicious behavior or anomalies around the time the alert was triggered.
- Examine the system's AppArmor status to verify if it has been disabled or tampered with, and assess any potential impact on system security.
- Correlate this event with other alerts or logs from the same host or user to identify patterns or a broader attack campaign.
- Consult threat intelligence sources to determine if there are known adversaries or malware that commonly attempt to disable AppArmor in similar ways.

### False positive analysis

- Routine system maintenance activities may trigger this rule, such as administrators stopping AppArmor for legitimate updates or configuration changes. To manage this, create exceptions for known maintenance windows or specific administrator accounts.
- Automated scripts or configuration management tools like Ansible or Puppet might stop or disable AppArmor as part of their deployment processes. Identify these scripts and whitelist their execution paths or associated user accounts.
- Testing environments where security modules are frequently enabled and disabled for testing purposes can generate false positives. Consider excluding these environments from the rule or adjusting the rule's sensitivity for these specific hosts.
- Some legitimate software installations may require temporarily disabling AppArmor. Monitor installation logs and correlate them with the rule triggers to identify and exclude these benign activities.
- In environments where AppArmor is not actively used or managed, the rule may trigger on default system actions. Evaluate the necessity of monitoring AppArmor in such environments and adjust the rule scope accordingly.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or potential lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, specifically those attempting to disable AppArmor, to halt any ongoing malicious activities.
- Conduct a thorough review of system logs and process execution history to identify any additional indicators of compromise or related malicious activities.
- Restore AppArmor to its intended operational state by re-enabling the service and ensuring all security policies are correctly applied.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems may be affected.
- Implement enhanced monitoring on the affected system and similar environments to detect any future attempts to disable AppArmor or other security controls.
- Review and update access controls and permissions to ensure that only authorized personnel can modify security settings, reducing the risk of similar incidents.
