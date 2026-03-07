---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Apple Script Execution followed by Network Connection" prebuilt detection rule.'
---

# Apple Script Execution followed by Network Connection

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Apple Script Execution followed by Network Connection

AppleScript, a scripting language for macOS, automates tasks by controlling applications and system functions. Adversaries exploit it to execute scripts that establish unauthorized network connections, facilitating command and control activities. The detection rule identifies such abuse by monitoring the osascript process for script execution followed by network activity, excluding local and private IP ranges, within a short timeframe.

### Possible investigation steps

- Review the process details for the osascript execution event, focusing on the process.entity_id and host.id to understand the context of the script execution.
- Examine the network connection details associated with the osascript process, particularly the destination IP address, to determine if it is known or suspicious, and check if it falls outside the excluded IP ranges.
- Investigate the script content or command line arguments used in the osascript execution to identify any potentially malicious or unexpected behavior.
- Check the timeline of events to see if there are any other related or suspicious activities occurring on the same host around the time of the osascript execution and network connection.
- Correlate the osascript activity with any other alerts or logs from the same host to identify patterns or additional indicators of compromise.
- Assess the user account associated with the osascript process to determine if it is a legitimate user or if there are signs of account compromise.

### False positive analysis

- Legitimate automation scripts may trigger the rule if they execute osascript and establish network connections. Review the script's purpose and source to determine if it is authorized.
- System management tools that use AppleScript for remote administration can cause false positives. Identify these tools and consider creating exceptions for their known processes.
- Software updates or applications that use AppleScript for network communication might be flagged. Verify the application's legitimacy and update the rule to exclude these specific processes or IP addresses.
- Development environments that utilize AppleScript for testing or deployment may inadvertently match the rule. Ensure these environments are recognized and excluded from monitoring if they are trusted.
- Regularly review and update the list of excluded IP ranges and processes to ensure they reflect the current network and application landscape, minimizing unnecessary alerts.

### Response and remediation

- Immediately isolate the affected macOS host from the network to prevent further unauthorized access or data exfiltration.
- Terminate the osascript process identified in the alert to stop any ongoing malicious activity.
- Conduct a thorough review of the executed AppleScript to identify any malicious commands or payloads and remove any associated files or scripts from the system.
- Reset credentials for any accounts that were accessed or could have been compromised during the incident.
- Apply security patches and updates to the macOS system to address any vulnerabilities that may have been exploited.
- Monitor network traffic for any further suspicious activity originating from the affected host or similar patterns across other systems.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems have been compromised.
