---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Launch Service Creation and Immediate Loading" prebuilt detection rule.
---

# Launch Service Creation and Immediate Loading

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Launch Service Creation and Immediate Loading

Launch Agents in macOS are used to execute scripts or applications automatically at user login, providing a mechanism for persistence. Adversaries exploit this by creating or modifying Launch Agents to execute malicious payloads. The detection rule identifies such activities by monitoring file changes in Launch Agent directories and subsequent immediate loading via `launchctl`, indicating potential unauthorized persistence attempts.

### Possible investigation steps

- Review the file path where the modification or creation of the Launch Agent occurred to determine if it is in a system directory (e.g., /System/Library/LaunchAgents/) or a user directory (e.g., /Users/*/Library/LaunchAgents/). This can help assess the potential impact and scope of the change.
- Examine the contents of the newly created or modified plist file to identify the script or application it is configured to execute. Look for any suspicious or unexpected entries that could indicate malicious activity.
- Check the timestamp of the file modification event to correlate it with any known user activities or other system events that might explain the change.
- Investigate the process execution details of the launchctl command, including the user account under which it was executed and any associated parent processes, to determine if it aligns with legitimate administrative actions or if it appears suspicious.
- Search for any additional related alerts or logs around the same timeframe that might indicate further malicious behavior or corroborate the persistence attempt, such as other process executions or network connections initiated by the suspicious process.

### False positive analysis

- System or application updates may create or modify Launch Agents as part of their installation or update process. Users can create exceptions for known and trusted applications by whitelisting their specific file paths or process names.
- User-installed applications that require background processes might use Launch Agents for legitimate purposes. Identify these applications and exclude their associated Launch Agent paths from monitoring.
- Administrative scripts or tools used by IT departments for system management might trigger this rule. Coordinate with IT to document these scripts and exclude their activities from detection.
- Development tools or environments that automatically configure Launch Agents for testing purposes can cause false positives. Developers should be aware of these activities and can exclude their specific development directories.
- Backup or synchronization software that uses Launch Agents to schedule tasks may be flagged. Verify these applications and exclude their Launch Agent paths if they are deemed safe.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further malicious activity or lateral movement.
- Terminate any suspicious processes associated with the unauthorized Launch Agent using Activity Monitor or the `kill` command in Terminal.
- Remove the malicious Launch Agent plist file from the affected directories: `/System/Library/LaunchAgents/`, `/Library/LaunchAgents/`, or `/Users/*/Library/LaunchAgents/`.
- Review and restore any system or application settings that may have been altered by the malicious Launch Agent.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or processes.
- Monitor the system for any signs of re-infection or further unauthorized changes to Launch Agents, ensuring that logging and alerting are configured to detect similar activities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
