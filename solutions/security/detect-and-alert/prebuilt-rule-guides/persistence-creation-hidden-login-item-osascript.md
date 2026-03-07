---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Creation of Hidden Login Item via Apple Script" prebuilt detection rule.'
---

# Creation of Hidden Login Item via Apple Script

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Creation of Hidden Login Item via Apple Script

AppleScript is a scripting language for automating tasks on macOS, including managing login items. Adversaries exploit this by creating hidden login items to maintain persistence without detection. The detection rule identifies suspicious use of `osascript` to create such items, focusing on command patterns that specify hidden attributes, thus flagging potential stealthy persistence attempts.

### Possible investigation steps

- Review the process details to confirm the presence of 'osascript' in the command line, specifically looking for patterns like "login item" and "hidden:true" to verify the alert's accuracy.
- Investigate the parent process of the 'osascript' execution to determine if it was initiated by a legitimate application or a potentially malicious source.
- Check the user account associated with the process to assess whether the activity aligns with typical user behavior or if it suggests unauthorized access.
- Examine recent login items and system logs to identify any new or unusual entries that could indicate persistence mechanisms being established.
- Correlate the event with other security alerts or logs from the same host to identify any related suspicious activities or patterns.
- If possible, retrieve and analyze the AppleScript code executed to understand its purpose and potential impact on the system.

### False positive analysis

- Legitimate applications or scripts that automate login item management may trigger this rule. Review the process command line details to verify if the application is trusted.
- System administrators or IT management tools might use AppleScript for legitimate configuration tasks. Confirm if the activity aligns with scheduled maintenance or deployment activities.
- Users with advanced scripting knowledge might create custom scripts for personal use. Check if the script is part of a known user workflow and consider excluding it if verified as non-threatening.
- Frequent triggers from the same source could indicate a benign automation process. Implement exceptions for specific scripts or processes after thorough validation to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or data exfiltration.
- Terminate the suspicious osascript process identified in the alert to halt any ongoing malicious activity.
- Remove the hidden login item created by the osascript to eliminate the persistence mechanism. This can be done by accessing the user's login items and deleting any unauthorized entries.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or processes.
- Review system logs and the user's recent activity to identify any other signs of compromise or related suspicious behavior.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring for osascript usage and login item modifications across the network to detect similar threats in the future.
