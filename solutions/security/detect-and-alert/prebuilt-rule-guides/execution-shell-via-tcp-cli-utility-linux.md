---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Reverse Shell" prebuilt detection rule.
---

# Potential Reverse Shell

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Reverse Shell

Reverse shells are tools that adversaries use to gain remote access to a system by initiating a connection from the target back to the attacker. This detection rule identifies such activity by monitoring for network events followed by shell process creation on Linux systems. It flags suspicious patterns, such as shell processes with interactive flags or spawned by tools like socat, indicating potential unauthorized access attempts.

### Possible investigation steps

- Review the network event details to identify the source and destination IP addresses involved in the connection attempt or acceptance. Pay special attention to any external IP addresses that are not part of the internal network ranges.
- Examine the process tree to understand the parent-child relationship, focusing on the shell process creation following the network event. Verify if the shell process was spawned by a known tool like socat.
- Check the process arguments for interactive flags such as "-i" or "-l" to determine if the shell was intended to be interactive, which could indicate malicious intent.
- Investigate the user account associated with the process to determine if it is a legitimate user or if there are signs of compromise, such as unusual login times or locations.
- Correlate the event with other security logs or alerts to identify any additional suspicious activities or patterns that might indicate a broader attack campaign.
- Assess the risk and impact of the potential reverse shell by determining if any sensitive data or critical systems could have been accessed or compromised.

### False positive analysis

- Legitimate administrative tasks using interactive shells may trigger this rule. System administrators often use shells with interactive flags for maintenance. To mitigate, create exceptions for known administrator accounts or specific IP addresses.
- Automated scripts or cron jobs that use shell commands with interactive flags can be mistaken for reverse shells. Review and whitelist these scripts by process name or parent process ID to prevent false alerts.
- Tools like socat are used in legitimate network troubleshooting and testing. If socat is frequently used in your environment, consider excluding specific command patterns or user accounts associated with its legitimate use.
- Development environments may spawn shell processes as part of testing or deployment workflows. Identify and exclude these environments by host ID or process name to reduce noise.
- Internal network connections that match the rule's criteria but are part of normal operations can be excluded by specifying internal IP ranges or known service accounts.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious shell processes identified by the detection rule, especially those initiated by socat or with interactive flags.
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise, such as unauthorized user accounts or modified files.
- Review and secure network configurations to ensure that only authorized IP addresses can initiate connections to critical systems.
- Update and patch the affected system and any related software to close vulnerabilities that may have been exploited.
- Implement enhanced monitoring and logging on the affected host and network to detect any further attempts at reverse shell activity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if broader organizational impacts exist.
