---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Network Connection Initiated by Suspicious SSHD Child Process" prebuilt detection rule.'
---

# Network Connection Initiated by Suspicious SSHD Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Network Connection Initiated by Suspicious SSHD Child Process

The SSH Daemon (SSHD) facilitates secure remote logins and command execution on Linux systems. Adversaries may exploit SSHD by modifying shell configurations or backdooring the daemon to establish unauthorized connections, often for persistence or data exfiltration. The detection rule identifies suspicious outbound connections initiated by SSHD child processes, excluding benign processes and internal IP ranges, to flag potential malicious activity.

### Possible investigation steps

- Review the process details of the SSHD child process that initiated the network connection, focusing on the process.entity_id and process.parent.entity_id to understand the process hierarchy and parent-child relationship.
- Examine the destination IP address of the network connection attempt to determine if it is associated with known malicious activity or suspicious external entities, especially since it is not within the excluded internal IP ranges.
- Investigate the executable path of the process that initiated the connection to ensure it is not a known benign process like "/bin/yum" or "/usr/bin/yum", and verify if the process name is not among the excluded ones such as "login_duo", "ssh", "sshd", or "sshd-session".
- Check the timing and frequency of the SSHD child process executions and network connection attempts to identify any patterns or anomalies that could indicate unauthorized or persistent access attempts.
- Correlate the alert with other security events or logs from the same host.id to gather additional context and determine if there are other indicators of compromise or related suspicious activities.

### False positive analysis

- Internal administrative scripts or tools that initiate network connections upon SSH login can trigger false positives. To manage this, identify and whitelist these specific scripts or tools by their process names or executable paths.
- Automated software updates or package management processes like yum may occasionally initiate network connections. Exclude these processes by adding them to the exception list using their executable paths.
- Security tools such as login_duo or other authentication mechanisms that establish network connections during SSH sessions can be mistaken for malicious activity. Exclude these tools by specifying their process names in the exception list.
- Custom monitoring or logging solutions that connect to external servers for data aggregation might be flagged. Identify these processes and exclude them by their executable paths or process names to prevent false alerts.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified as child processes of SSHD that are attempting unauthorized network connections.
- Conduct a thorough review of SSHD configuration files and shell configuration files for unauthorized modifications or backdoors, and restore them from a known good backup if necessary.
- Change all credentials associated with the affected system, especially those that may have been exposed or used during the unauthorized SSH sessions.
- Apply security patches and updates to the SSH daemon and related software to mitigate known vulnerabilities that could be exploited for persistence or unauthorized access.
- Monitor network traffic for any further suspicious outbound connections from other systems, indicating potential lateral movement or additional compromised hosts.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the compromise.
