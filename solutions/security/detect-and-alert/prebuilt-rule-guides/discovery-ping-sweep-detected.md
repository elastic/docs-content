---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Network Scan Executed From Host" prebuilt detection rule.'
---

# Potential Network Scan Executed From Host

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Network Scan Executed From Host

In Linux environments, utilities like ping, netcat, and socat are essential for network diagnostics and communication. However, adversaries can exploit these tools to perform network scans, identifying active hosts and services for further exploitation. The detection rule identifies rapid execution of these utilities, signaling potential misuse for network reconnaissance, by monitoring process initiation events linked to these tools.

### Possible investigation steps

- Review the process initiation events to confirm the rapid execution of utilities like ping, netcat, or socat by examining the process.name field in the alert.
- Identify the user account associated with the process execution by checking the user information in the event data to determine if the activity aligns with expected behavior.
- Analyze the command line arguments used with the executed utilities by inspecting the process.command_line field to understand the scope and intent of the network scan.
- Correlate the alert with other recent events on the host by reviewing event timestamps and related process activities to identify any patterns or additional suspicious behavior.
- Check network logs or firewall logs for any unusual outbound connections or traffic patterns originating from the host to assess the potential impact of the network scan.
- Investigate the host's recent login history and user activity to determine if there are signs of unauthorized access or compromise that could explain the network scan activity.

### False positive analysis

- Routine network diagnostics by system administrators can trigger alerts. To manage this, create exceptions for known administrator accounts or specific IP addresses frequently used for legitimate network diagnostics.
- Automated monitoring scripts that use these utilities for health checks or performance monitoring may cause false positives. Identify and exclude these scripts by their process names or execution paths.
- Scheduled tasks or cron jobs that involve network utilities for maintenance purposes can be mistaken for network scans. Exclude these tasks by their specific scheduling patterns or associated user accounts.
- Security tools that perform regular network sweeps as part of their functionality might be flagged. Whitelist these tools by their process names or hash values to prevent unnecessary alerts.
- Development or testing environments where network utilities are used for testing purposes can generate false positives. Implement exclusions based on environment-specific identifiers or network segments.

### Response and remediation

- Isolate the affected host from the network to prevent further reconnaissance or lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, such as those involving ping, netcat, or socat, to halt ongoing network scans.
- Conduct a thorough review of the host's process logs and network activity to identify any additional indicators of compromise or related malicious activity.
- Reset credentials and review access permissions for accounts that were active on the compromised host to prevent unauthorized access.
- Apply patches and updates to the host's operating system and installed software to mitigate vulnerabilities that could be exploited by adversaries.
- Enhance network monitoring and logging to detect similar reconnaissance activities in the future, ensuring that alerts are configured to notify security teams promptly.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional hosts or systems are affected.
