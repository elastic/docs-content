---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Reverse Shell via Suspicious Child Process" prebuilt detection rule.'
---

# Potential Reverse Shell via Suspicious Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Reverse Shell via Suspicious Child Process

Reverse shells are a common technique used by attackers to gain remote access to a compromised system. They exploit scripting languages and utilities like Python, Perl, and Netcat to execute commands remotely. The detection rule identifies suspicious process chains and network activities, such as unexpected shell spawns and outbound connections, to flag potential reverse shell attempts, leveraging process and network event analysis to detect anomalies.

### Possible investigation steps

- Review the process chain to identify the parent process and determine if it is expected behavior for the system. Check the process.parent.name field for any unusual or unauthorized parent processes.
- Analyze the process arguments captured in the alert, such as process.args, to understand the command being executed and assess if it aligns with known reverse shell patterns.
- Investigate the network connection details, focusing on the destination.ip field, to determine if the connection is to a known malicious IP or an unexpected external address.
- Check the process.name field to identify the specific utility used (e.g., python, perl, nc) and verify if its usage is legitimate or if it indicates a potential compromise.
- Correlate the alert with other security events or logs from the same host.id to identify any additional suspicious activities or patterns that may indicate a broader attack.
- Consult threat intelligence sources to gather information on any identified IP addresses or domains involved in the network connection to assess their reputation and potential threat level.

### False positive analysis

- Development and testing environments may frequently execute scripts using languages like Python, Perl, or Ruby, which can trigger the rule. To manage this, consider excluding specific host IDs or process names associated with known development activities.
- Automated scripts or cron jobs that utilize network connections for legitimate purposes, such as data backups or updates, might be flagged. Identify these processes and add them to an exception list based on their parent process names or specific arguments.
- System administrators might use tools like Netcat or OpenSSL for troubleshooting or monitoring network connections. If these activities are routine and verified, exclude them by specifying the administrator's user ID or the specific command patterns used.
- Security tools or monitoring solutions that simulate attack scenarios for testing purposes can also trigger this rule. Ensure these tools are recognized and excluded by their process names or associated network activities.
- Custom scripts that use shell commands to interact with remote systems for maintenance tasks may appear suspicious. Review these scripts and exclude them by their unique process arguments or parent process names.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, particularly those involving scripting languages or utilities like Python, Perl, or Netcat.
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise, such as unauthorized user accounts or modified system files.
- Review and reset credentials for any accounts that may have been accessed or compromised during the incident.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Monitor network traffic for any signs of further suspicious activity, focusing on outbound connections from the affected host.
- Escalate the incident to the security operations center (SOC) or relevant security team for further investigation and to ensure comprehensive remediation efforts.
