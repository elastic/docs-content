---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Modification of Safari Settings via Defaults Command" prebuilt detection rule.'
---

# Modification of Safari Settings via Defaults Command

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Modification of Safari Settings via Defaults Command

The 'defaults' command in macOS is a utility that allows users to read, write, and manage macOS application preferences, including Safari settings. Adversaries may exploit this command to alter Safari configurations, potentially enabling harmful features like JavaScript from Apple Events, which can facilitate browser hijacking. The detection rule monitors for suspicious 'defaults' command usage targeting Safari settings, excluding benign preference changes, to identify potential defense evasion attempts.

### Possible investigation steps

- Review the process execution details to confirm the use of the 'defaults' command with arguments targeting Safari settings, specifically looking for any suspicious or unauthorized changes.
- Check the user account associated with the process execution to determine if the action was performed by a legitimate user or an unauthorized entity.
- Investigate the system's recent activity logs to identify any other unusual or suspicious behavior around the time the 'defaults' command was executed.
- Examine the Safari settings before and after the change to assess the impact and identify any potentially harmful configurations, such as enabling JavaScript from Apple Events.
- Correlate the event with other security alerts or incidents to determine if this action is part of a broader attack or compromise attempt.

### False positive analysis

- Changes to Safari settings for legitimate user preferences can trigger alerts, such as enabling or disabling search suggestions. Users can create exceptions for these specific settings by excluding them from the detection rule.
- System administrators may use the defaults command to configure Safari settings across multiple devices for compliance or user experience improvements. These actions can be whitelisted by identifying the specific process arguments used in these administrative tasks.
- Automated scripts or management tools that adjust Safari settings as part of routine maintenance or updates may cause false positives. Users should identify these scripts and exclude their specific process arguments from the detection rule.
- Developers testing Safari configurations might frequently change settings using the defaults command. Excluding known developer machines or user accounts from the rule can help reduce false positives.
- Educational or training environments where users are instructed to modify Safari settings for learning purposes can lead to alerts. Identifying and excluding these environments or sessions can mitigate unnecessary alerts.

### Response and remediation

- Immediately isolate the affected macOS device from the network to prevent further malicious activity or data exfiltration.
- Terminate any suspicious processes related to the 'defaults' command that are currently running on the affected device.
- Revert any unauthorized changes made to Safari settings by restoring them to their default or previously known safe state.
- Conduct a thorough scan of the affected device using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malware or malicious scripts.
- Review and update the device's security settings to prevent unauthorized changes, including disabling unnecessary Apple Events and restricting the use of the 'defaults' command to authorized personnel only.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other devices in the network are affected.
- Implement enhanced monitoring and alerting for similar 'defaults' command usage across the network to detect and respond to future attempts promptly.
