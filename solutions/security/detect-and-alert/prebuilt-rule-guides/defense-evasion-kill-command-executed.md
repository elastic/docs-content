---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kill Command Execution" prebuilt detection rule.'
---

# Kill Command Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kill Command Execution
In Linux environments, commands like kill, pkill, and killall are essential for managing processes, allowing users to terminate them as needed. However, adversaries can exploit these commands to disable security tools or disrupt operations, aiding in evasion tactics. The detection rule identifies such misuse by monitoring process execution events, specifically targeting these commands to flag potential threats.

### Possible investigation steps

- Review the process execution event details to identify the user account associated with the kill, pkill, or killall command execution. This can help determine if the action was performed by a legitimate user or a potential adversary.
- Examine the parent process of the command execution to understand the context in which the kill command was initiated. This can provide insights into whether the command was part of a script or an interactive session.
- Check the target process IDs (PIDs) that were terminated by the kill command to assess if critical or security-related processes were affected, which might indicate malicious intent.
- Investigate the timing and frequency of the command execution to identify patterns or anomalies, such as repeated or scheduled executions, which could suggest automated or scripted activity.
- Correlate the event with other security alerts or logs from the same host around the same timeframe to identify any related suspicious activities or indicators of compromise.

### False positive analysis

- Routine system maintenance tasks may trigger the rule when administrators use kill commands to manage processes. To handle this, create exceptions for known maintenance scripts or processes by identifying their unique attributes, such as user or command line arguments.
- Automated scripts or monitoring tools that use kill commands for legitimate purposes, like restarting services, can cause false positives. Exclude these by specifying the script names or paths in the detection rule.
- Development environments where developers frequently use kill commands during testing can lead to alerts. Consider excluding processes executed by specific user accounts associated with development activities.
- System updates or package management tools might use kill commands as part of their operation. Identify these processes and exclude them based on their parent process or command line patterns.
- Backup or recovery operations that involve stopping services may trigger the rule. Exclude these by recognizing the specific backup software or service names involved.

### Response and remediation

- Immediately isolate the affected Linux system from the network to prevent further malicious activity or lateral movement by the attacker.
- Identify and terminate any unauthorized or suspicious processes that were started around the time of the alert, focusing on those that may have been targeted by the kill, pkill, or killall commands.
- Review system logs and process execution history to determine the origin of the kill command execution and assess whether it was initiated by a legitimate user or a compromised account.
- Restore any terminated security tools or critical processes to ensure the system's defenses are fully operational.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection tools to identify and remove any additional malware or persistence mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems may be affected.
- Implement additional monitoring and alerting for similar command executions across the network to enhance detection and response capabilities for future incidents.
