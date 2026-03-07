---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "SoftwareUpdate Preferences Modification" prebuilt detection rule.
---

# SoftwareUpdate Preferences Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SoftwareUpdate Preferences Modification

In macOS environments, the SoftwareUpdate preferences manage system updates, crucial for maintaining security. Adversaries may exploit the 'defaults' command to alter these settings, potentially disabling updates to evade defenses. The detection rule identifies such modifications by monitoring specific command executions that attempt to change update preferences without enabling them, signaling potential malicious activity.

### Possible investigation steps

- Review the process execution details to confirm the presence of the 'defaults' command with arguments attempting to modify SoftwareUpdate preferences, specifically looking for 'write', '-bool', and the targeted preferences file paths.
- Check the user account associated with the process execution to determine if it aligns with expected administrative activity or if it might be indicative of unauthorized access.
- Investigate the host's recent activity for any other suspicious processes or commands that may suggest a broader attempt to impair system defenses or evade detection.
- Examine system logs and security alerts around the time of the detected event to identify any correlated activities or anomalies that could provide additional context or evidence of malicious intent.
- Assess the current state of the SoftwareUpdate preferences on the affected host to verify if updates have been disabled or altered, and take corrective actions if necessary.

### False positive analysis

- System administrators may use the defaults command to configure SoftwareUpdate settings during routine maintenance. To handle this, create exceptions for known administrative scripts or processes that frequently execute these commands.
- Automated configuration management tools might alter SoftwareUpdate preferences as part of their standard operations. Identify these tools and exclude their process identifiers from triggering the rule.
- Some legitimate applications may require specific update settings and modify preferences accordingly. Monitor and whitelist these applications to prevent unnecessary alerts.
- User-initiated changes to update settings for personal preferences can trigger false positives. Educate users on the implications of such changes and consider excluding user-specific processes if they are consistently non-threatening.
- During system setup or reconfiguration, defaults commands may be used to establish baseline settings. Temporarily disable the rule or set up a temporary exception during these periods to avoid false alerts.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential spread or further unauthorized changes.
- Review the process execution logs to confirm the unauthorized use of the 'defaults' command and identify any associated user accounts or processes.
- Revert any unauthorized changes to the SoftwareUpdate preferences by resetting them to their default state using the 'defaults' command with appropriate parameters.
- Conduct a thorough scan of the affected system for additional signs of compromise, such as malware or unauthorized access attempts, using endpoint security tools.
- Change passwords and review permissions for any user accounts involved in the incident to prevent further unauthorized access.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
- Implement enhanced monitoring for similar command executions across the network to detect and respond to future attempts promptly.
