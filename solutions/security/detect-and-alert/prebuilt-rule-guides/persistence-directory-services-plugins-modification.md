---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Persistence via DirectoryService Plugin Modification" prebuilt detection rule.'
---

# Persistence via DirectoryService Plugin Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Persistence via DirectoryService Plugin Modification

DirectoryService PlugIns on macOS are integral for managing directory-based services, automatically executing on system boot. Adversaries exploit this by modifying or creating malicious plugins to ensure persistent access. The detection rule identifies suspicious activity by monitoring non-deletion events involving dsplug files in the PlugIns directory, flagging potential unauthorized modifications indicative of persistence tactics.

### Possible investigation steps

- Review the alert details to confirm the file path matches /Library/DirectoryServices/PlugIns/*.dsplug, indicating a potential unauthorized modification or creation of a DirectoryService plugin.
- Check the file creation or modification timestamp to determine when the suspicious activity occurred and correlate it with other system events or user activities around that time.
- Investigate the file's origin by examining the file's metadata, such as the creator or modifying user, and cross-reference with known user accounts and their typical behavior.
- Analyze the contents of the modified or newly created dsplug file to identify any malicious code or unusual configurations that could indicate adversarial activity.
- Review system logs and other security alerts around the time of the event to identify any related suspicious activities or patterns that could suggest a broader compromise.
- Assess the risk and impact of the modification by determining if the plugin is actively being used for persistence or if it has been executed by the DirectoryService daemon.

### False positive analysis

- Routine system updates or legitimate software installations may modify dsplug files, triggering alerts. Users can create exceptions for known update processes or trusted software installations to reduce noise.
- Administrative tasks performed by IT personnel, such as configuring directory services, might involve legitimate modifications to dsplug files. Implementing a whitelist for actions performed by verified IT accounts can help minimize false positives.
- Security software or system management tools that interact with directory services might cause benign modifications. Identifying and excluding these tools from monitoring can prevent unnecessary alerts.
- Automated scripts or maintenance tasks that regularly check or update directory service configurations could be flagged. Documenting and excluding these scripts from detection can help maintain focus on genuine threats.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Conduct a thorough review of the identified dsplug file(s) in the /Library/DirectoryServices/PlugIns/ directory to confirm unauthorized modifications or creations. Compare against known good configurations or backups.
- Remove any unauthorized or malicious dsplug files and restore legitimate versions from a trusted backup if available.
- Restart the DirectoryService daemon to ensure it is running only legitimate plugins. This can be done by executing `sudo launchctl stop com.apple.DirectoryServices` followed by `sudo launchctl start com.apple.DirectoryServices`.
- Perform a comprehensive scan of the system using updated security tools to identify any additional malicious files or indicators of compromise.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring on the DirectoryServices PlugIns directory to detect future unauthorized changes promptly, ensuring alerts are configured to notify the security team immediately.
