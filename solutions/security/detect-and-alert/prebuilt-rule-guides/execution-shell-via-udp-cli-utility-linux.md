---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Reverse Shell via UDP" prebuilt detection rule.
---

# Potential Reverse Shell via UDP

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Reverse Shell via UDP

Reverse shells over UDP can be exploited by attackers to bypass firewalls and gain unauthorized access to systems. This technique leverages UDP's connectionless nature, making it harder to detect. Adversaries may use scripting languages or network tools to initiate these connections. The detection rule identifies suspicious processes executing network-related syscalls and egress connections, flagging potential reverse shell activity.

### Possible investigation steps

- Review the process details such as process.pid, process.parent.pid, and process.name to identify the specific process that triggered the alert and its parent process.
- Examine the command line arguments and environment variables associated with the suspicious process to understand its intended function and origin.
- Check the network connection details, including destination.ip and network.direction, to determine the external entity the process attempted to connect to and assess if it is a known malicious IP or domain.
- Investigate the user account associated with the process to determine if it has been compromised or if there are any signs of unauthorized access.
- Analyze historical logs for any previous instances of similar process executions or network connections to identify patterns or repeated attempts.
- Correlate the alert with other security events or alerts from the same host.id to gather additional context and assess the scope of potential compromise.

### False positive analysis

- Legitimate administrative scripts or tools may trigger the rule if they use UDP for valid network operations. Users can create exceptions for specific scripts or processes that are known to perform routine administrative tasks.
- Automated monitoring or network management tools that use UDP for health checks or status updates might be flagged. Identify these tools and exclude their process names or network patterns from the rule.
- Development or testing environments where developers frequently use scripting languages or network tools for legitimate purposes can cause false positives. Consider excluding specific host IDs or process names associated with these environments.
- Custom applications that use UDP for communication, especially if they are developed in-house, may be mistakenly identified. Review these applications and whitelist their process names or network behaviors if they are verified as safe.
- Network scanning or diagnostic tools that use UDP for troubleshooting can be misinterpreted as malicious. Ensure these tools are recognized and excluded from the detection rule if they are part of regular network maintenance activities.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, particularly those associated with known reverse shell tools or scripting languages.
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise, such as unauthorized user accounts or modified system files.
- Review and update firewall rules to block outbound UDP traffic from unauthorized applications or processes, ensuring legitimate traffic is not disrupted.
- Reset credentials for any accounts accessed from the affected host, especially if they have administrative privileges.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems may be affected.
- Implement enhanced monitoring and logging for similar suspicious activities, focusing on the execution of network-related syscalls and egress connections from scripting languages or network tools.
