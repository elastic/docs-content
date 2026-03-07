---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Prompt for Credentials with Osascript" prebuilt detection rule.
---

# Prompt for Credentials with Osascript

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Prompt for Credentials with OSASCRIPT

OSASCRIPT is a macOS utility that allows the execution of AppleScript and other OSA language scripts. Adversaries may exploit it to display deceptive dialogs prompting users for credentials, mimicking legitimate requests. The detection rule identifies suspicious OSASCRIPT usage by monitoring specific command patterns and excluding known legitimate processes, thereby flagging potential credential theft attempts.

### Possible investigation steps

- Review the process command line to confirm if the osascript command includes suspicious patterns like "display dialog" with "password" or "passphrase" to determine if it is attempting to prompt for credentials.
- Check the parent process executable to see if it matches any known legitimate applications or services, such as those listed in the exclusion criteria, to rule out false positives.
- Investigate the user account associated with the process to determine if it is a privileged account or if there is any unusual activity associated with it.
- Examine the process execution context, including the effective parent executable, to identify if the osascript was executed by a legitimate management tool or script.
- Look for any other related alerts or logs around the same timeframe to identify if this is part of a broader attack or isolated incident.
- Assess the risk and impact by determining if any credentials were potentially compromised and if further containment or remediation actions are necessary.

### False positive analysis

- Legitimate administrative scripts using osascript may trigger alerts if they include dialog prompts for passwords or passphrases. To manage this, identify and exclude these scripts by adding their specific command lines or parent executables to the exception list.
- Processes initiated by trusted applications like JAMF or Karabiner-Elements can be mistakenly flagged. Ensure these applications are included in the exclusion list to prevent unnecessary alerts.
- Scheduled maintenance tasks that use osascript for legitimate purposes might be misidentified. Review and exclude these tasks by specifying their user IDs or command line patterns in the detection rule exceptions.
- Custom scripts executed by system administrators for routine operations may appear suspicious. Document these scripts and add them to the exclusion criteria to avoid false positives.
- Terminal-based automation tools that interact with osascript could be incorrectly flagged. Verify these tools and include their paths in the exclusion list to reduce false alerts.

### Response and remediation

- Immediately isolate the affected macOS device from the network to prevent further unauthorized access or data exfiltration.
- Terminate the suspicious osascript process identified by the alert to stop any ongoing credential theft attempts.
- Conduct a thorough review of the affected system's recent activity logs to identify any unauthorized access or changes made during the incident.
- Reset credentials for any accounts that may have been compromised, ensuring that new passwords are strong and unique.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
- Implement additional monitoring on the affected system and similar endpoints to detect any recurrence of the threat.
- Review and update endpoint security configurations to block unauthorized script execution and enhance detection capabilities for similar threats in the future.
