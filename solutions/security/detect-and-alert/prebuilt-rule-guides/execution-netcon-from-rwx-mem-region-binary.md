---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Network Connection from Binary with RWX Memory Region" prebuilt detection rule.
---

# Network Connection from Binary with RWX Memory Region

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Network Connection from Binary with RWX Memory Region

In Linux environments, the `mprotect()` system call adjusts memory permissions, potentially enabling read, write, and execute (RWX) access. Adversaries exploit this to execute malicious code in memory, often followed by network connections to exfiltrate data or communicate with command-and-control servers. The detection rule identifies such behavior by monitoring for RWX memory changes and subsequent network activity, flagging suspicious processes for further analysis.

### Possible investigation steps

- Review the process details using the process.pid and process.name fields to identify the binary that requested RWX memory permissions.
- Investigate the context of the mprotect() syscall by examining the process's command line arguments and parent process to understand its origin and purpose.
- Analyze the network connection details, focusing on the destination.ip field, to determine if the connection was made to a known malicious IP or an unusual external server.
- Check the process's execution history and any associated files or scripts to identify potential malicious payloads or scripts that may have been executed.
- Correlate the event with other security logs or alerts from the same host.id to identify any related suspicious activities or patterns.
- Assess the risk and impact by determining if any sensitive data was accessed or exfiltrated during the network connection attempt.

### False positive analysis

- Legitimate software updates or patches may temporarily use RWX memory regions. Monitor the specific process names and verify if they are associated with known update mechanisms. Consider adding these processes to an exception list if they are verified as safe.
- Development tools and environments often require RWX permissions for debugging or testing purposes. Identify these tools and exclude them from the rule if they are part of a controlled and secure development environment.
- Certain system services or daemons, like custom web servers or network services, might use RWX memory regions for legitimate reasons. Review the process names and network destinations to determine if they are part of expected system behavior, and exclude them if confirmed.
- Security software or monitoring tools may exhibit this behavior as part of their normal operation. Validate these processes and consider excluding them if they are recognized as part of your security infrastructure.
- Custom scripts or automation tasks that require dynamic code execution might trigger this rule. Ensure these scripts are reviewed and approved, then exclude them if they are deemed non-threatening.

### Response and remediation

- Isolate the affected host from the network immediately to prevent further data exfiltration or communication with potential command-and-control servers.
- Terminate the suspicious process identified by the detection rule to halt any ongoing malicious activity.
- Conduct a memory dump of the affected system to capture the current state for forensic analysis, focusing on the RWX memory regions.
- Review and analyze the network logs to identify any external IP addresses or domains the process attempted to connect to, and block these on the network firewall.
- Patch and update the affected system to the latest security updates to mitigate any known vulnerabilities that could have been exploited.
- Implement stricter memory protection policies to prevent processes from obtaining RWX permissions unless absolutely necessary.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if this is part of a larger attack campaign.
