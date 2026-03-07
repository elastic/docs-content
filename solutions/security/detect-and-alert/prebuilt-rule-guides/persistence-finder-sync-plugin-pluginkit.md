---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Finder Sync Plugin Registered and Enabled" prebuilt detection rule.
---

# Finder Sync Plugin Registered and Enabled

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Finder Sync Plugin Registered and Enabled

Finder Sync plugins enhance macOS Finder by allowing third-party applications to integrate and modify its interface. While beneficial for legitimate software, adversaries can exploit this feature to maintain persistence by registering malicious plugins. The detection rule identifies suspicious plugin registrations by monitoring the `pluginkit` process, filtering out known safe applications, and flagging unusual activity, thus helping analysts spot potential threats.

### Possible investigation steps

- Review the process details to confirm the execution of the `pluginkit` process with the specific arguments `-e`, `use`, and `-i`, which indicate the registration of a Finder Sync plugin.
- Cross-reference the plugin identifier found in the process arguments against the list of known safe applications to determine if it is potentially malicious.
- Investigate the parent process of the `pluginkit` execution to identify any unusual or unauthorized parent processes that might suggest malicious activity.
- Check the system for any recent installations or updates of applications that might have introduced the suspicious Finder Sync plugin.
- Analyze the behavior and origin of the executable associated with the suspicious plugin to assess its legitimacy and potential threat level.
- Review system logs and other security alerts around the time of the plugin registration to identify any correlated suspicious activities or anomalies.

### False positive analysis

- Known safe applications like Google Drive, Boxcryptor, Adobe, Microsoft OneDrive, Insync, and Box are already excluded from triggering false positives. Ensure these applications are up-to-date to maintain their exclusion status.
- If a legitimate application not listed in the exclusions is causing false positives, consider adding its specific Finder Sync plugin identifier to the exclusion list after verifying its safety.
- Monitor the parent process paths of legitimate applications. If a trusted application frequently triggers alerts, add its executable path to the exclusion list to prevent unnecessary alerts.
- Regularly review and update the exclusion list to accommodate new versions or additional legitimate applications that may introduce Finder Sync plugins.
- Educate users on the importance of installing applications from trusted sources to minimize the risk of false positives and ensure that only legitimate plugins are registered.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or data exfiltration by the malicious Finder Sync plugin.
- Terminate the suspicious `pluginkit` process to stop the execution of the rogue Finder Sync plugin and prevent further persistence.
- Remove the malicious Finder Sync plugin by unregistering it using the `pluginkit` command with appropriate flags to ensure it cannot be re-enabled.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious payloads or artifacts.
- Review system logs and the Finder Sync plugin registration history to identify any unauthorized changes or additional compromised systems.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if the threat is part of a larger attack campaign.
- Implement enhanced monitoring for `pluginkit` activity and similar persistence mechanisms to detect and respond to future attempts promptly.
