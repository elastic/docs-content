---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious ScreenConnect Client Child Process" prebuilt detection rule.
---

# Suspicious ScreenConnect Client Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious ScreenConnect Client Child Process

ScreenConnect, a remote access tool, facilitates legitimate remote support but can be exploited by adversaries to execute unauthorized commands. Malicious actors may spawn processes like PowerShell or cmd.exe via ScreenConnect to perform harmful activities. The detection rule identifies such suspicious child processes, focusing on unusual arguments and process names, indicating potential abuse of remote access capabilities.

### Possible investigation steps

- Review the parent process name to confirm it is one of the ScreenConnect client processes listed in the query, such as ScreenConnect.ClientService.exe or ScreenConnect.WindowsClient.exe, to verify the source of the suspicious activity.
- Examine the child process name and arguments, such as powershell.exe with encoded commands or cmd.exe with /c, to identify potentially malicious actions or commands being executed.
- Check the network activity associated with the suspicious process, especially if the process arguments include network-related terms like *http* or *downloadstring*, to determine if there is any unauthorized data exfiltration or command and control communication.
- Investigate the user account under which the suspicious process was executed to assess if the account has been compromised or is being misused.
- Correlate the event with other security alerts or logs from data sources like Elastic Defend or Microsoft Defender for Endpoint to gather additional context and identify any related malicious activities.
- Review the system's recent activity and changes, such as new scheduled tasks or services created by schtasks.exe or sc.exe, to identify any persistence mechanisms that may have been established by the attacker.

### False positive analysis

- Legitimate IT support activities using ScreenConnect may trigger the rule when executing scripts or commands for maintenance. To manage this, identify and whitelist specific IT support accounts or IP addresses that regularly perform these actions.
- Automated scripts or scheduled tasks that use ScreenConnect for routine operations might be flagged. Review and document these scripts, then create exceptions for known benign processes and arguments.
- Software updates or installations initiated through ScreenConnect can appear suspicious. Maintain a list of approved software and update processes, and exclude these from the rule.
- Internal security tools or monitoring solutions that leverage ScreenConnect for legitimate purposes may be detected. Verify these tools and add them to an exclusion list to prevent false positives.
- Training sessions or demonstrations using ScreenConnect to showcase command-line tools could be misinterpreted as threats. Ensure these sessions are logged and recognized as non-threatening, and adjust the rule to accommodate these scenarios.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the attacker.
- Terminate any suspicious processes identified in the alert, such as PowerShell, cmd.exe, or other flagged executables, to halt any ongoing malicious activity.
- Review and revoke any unauthorized user accounts or privileges that may have been created or modified using tools like net.exe or schtasks.exe.
- Conduct a thorough scan of the affected system using endpoint protection tools to identify and remove any malware or unauthorized software installed by the attacker.
- Restore the system from a known good backup if any critical system files or configurations have been altered or compromised.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for ScreenConnect and other remote access tools to detect similar activities in the future, ensuring that alerts are promptly reviewed and acted upon.
