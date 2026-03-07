---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential SharpRDP Behavior" prebuilt detection rule.'
---

# Potential SharpRDP Behavior

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential SharpRDP Behavior

Remote Desktop Protocol (RDP) enables users to connect to and control remote systems, facilitating legitimate administrative tasks. However, adversaries can exploit RDP for lateral movement within a network. SharpRDP, a tool for executing commands on remote systems via RDP, can be misused for unauthorized access. The detection rule identifies suspicious RDP activity by monitoring network connections, registry changes, and process executions, flagging potential misuse indicative of SharpRDP behavior.

### Possible investigation steps

- Review the network logs to confirm the presence of incoming RDP connections on port 3389, specifically looking for connections initiated by IP addresses other than localhost (127.0.0.1 or ::1).
- Examine the registry changes to identify any new RunMRU string values set to cmd, powershell, taskmgr, or tsclient, which could indicate command execution attempts.
- Investigate the process execution logs to verify if any processes were started with parent processes like cmd.exe, powershell.exe, or taskmgr.exe, and ensure these are not legitimate administrative actions.
- Correlate the timestamps of the RDP connection, registry change, and process execution to determine if they align within the 1-minute window specified by the detection rule.
- Check the source IP address of the RDP connection against known threat intelligence feeds to assess if it is associated with any malicious activity.
- Analyze user account activity associated with the RDP session to determine if the account was compromised or if the actions were authorized.

### False positive analysis

- Legitimate administrative tasks using RDP may trigger the rule if they involve command execution through cmd, powershell, or taskmgr. To manage this, create exceptions for known administrative IP addresses or user accounts frequently performing these tasks.
- Automated scripts or software updates that modify the RunMRU registry key with benign commands can be mistaken for SharpRDP behavior. Identify and exclude these processes or scripts from the detection rule.
- Remote management tools that use RDP and execute commands as part of their normal operation might be flagged. Whitelist these tools by their process names or specific command patterns to prevent false positives.
- Internal network scanning or monitoring tools that simulate RDP connections for security assessments could be misinterpreted. Exclude these tools by their source IP addresses or network behavior signatures.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further lateral movement and unauthorized access.
- Terminate any suspicious processes identified in the alert, such as those initiated by cmd.exe, powershell.exe, or taskmgr.exe, to halt any ongoing malicious activity.
- Review and revert any unauthorized registry changes, particularly those related to the RunMRU registry path, to restore system integrity.
- Conduct a thorough examination of the affected host for additional indicators of compromise, such as unauthorized user accounts or scheduled tasks, and remove any found.
- Reset credentials for any accounts that were accessed or potentially compromised during the incident to prevent further unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for RDP connections and registry changes to detect and respond to similar threats more effectively in the future.
