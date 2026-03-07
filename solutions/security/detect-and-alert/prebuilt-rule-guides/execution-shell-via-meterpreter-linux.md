---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Meterpreter Reverse Shell" prebuilt detection rule.'
---

# Potential Meterpreter Reverse Shell

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Meterpreter Reverse Shell

Meterpreter is a sophisticated payload within the Metasploit framework, enabling attackers to execute commands and scripts on compromised systems. Adversaries exploit it to perform system reconnaissance and data exfiltration. The detection rule identifies suspicious file access patterns typical of Meterpreter's system fingerprinting activities, such as reading key system files, indicating a potential reverse shell connection.

### Possible investigation steps

- Review the process associated with the alert by examining the process ID (process.pid) and user ID (user.id) to determine if the process is legitimate or potentially malicious.
- Check the host ID (host.id) to identify the specific system where the suspicious activity was detected and assess if it is a high-value target or has been previously compromised.
- Investigate the command history and running processes on the affected host to identify any unusual or unauthorized activities that may indicate a Meterpreter session.
- Analyze network connections from the host to detect any suspicious outbound connections that could suggest a reverse shell communication.
- Examine the file access patterns, particularly the access to files like /etc/machine-id, /etc/passwd, /proc/net/route, /proc/net/ipv6_route, and /proc/net/if_inet6, to understand the context and purpose of these reads and whether they align with normal system operations.
- Correlate the alert with other security events or logs from the same timeframe to identify any additional indicators of compromise or related malicious activities.

### False positive analysis

- System administration scripts or tools that perform regular checks on system files like /etc/machine-id or /etc/passwd may trigger this rule. To manage this, identify and whitelist these legitimate processes by their process ID or user ID.
- Backup or monitoring software that accesses network configuration files such as /proc/net/route or /proc/net/ipv6_route can cause false positives. Exclude these applications by adding exceptions for their specific file access patterns.
- Security tools that perform network diagnostics or inventory checks might read files like /proc/net/if_inet6. Review these tools and exclude their known benign activities from triggering the rule.
- Custom scripts used for system health checks or inventory management that access the flagged files should be reviewed. If deemed safe, add them to an exception list based on their host ID or user ID.

### Response and remediation

- Isolate the affected system from the network immediately to prevent further data exfiltration or lateral movement by the attacker.
- Terminate any suspicious processes identified by the detection rule, particularly those associated with the process IDs flagged in the alert.
- Conduct a thorough review of the affected system's logs and file access history to identify any additional unauthorized access or data exfiltration attempts.
- Change all credentials and keys that may have been exposed or compromised on the affected system, especially those related to user accounts identified in the alert.
- Restore the affected system from a known good backup to ensure any malicious changes are removed, and verify the integrity of the restored system.
- Implement network segmentation to limit the potential impact of future attacks and enhance monitoring of critical systems for similar suspicious activities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
