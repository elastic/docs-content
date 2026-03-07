---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Reverse Shell via Child" prebuilt detection rule.'
---

# Potential Reverse Shell via Child

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Reverse Shell via Child

Reverse shells are a technique where attackers gain remote access to a system by initiating a connection from the target back to the attacker's machine. This is often achieved using shell processes like bash or socat. Adversaries exploit this by executing commands remotely, bypassing firewalls. The detection rule identifies such activity by monitoring for network events followed by suspicious shell process executions, focusing on unusual command-line arguments and parent-child process relationships.

### Possible investigation steps

- Review the network event details to identify the source and destination IP addresses involved in the connection attempt or acceptance. Pay special attention to any external IP addresses that are not part of the internal network.
- Examine the process execution details, focusing on the command-line arguments used by the shell process. Look for unusual or suspicious arguments such as "-i" or "-l" that may indicate interactive or login shells.
- Investigate the parent-child process relationship, especially if the parent process is "socat" with arguments containing "exec". This could suggest an attempt to execute a reverse shell.
- Check the timeline of events to determine if the network event and shell process execution occurred within a short time frame (maxspan=5s), which may indicate a coordinated attack.
- Correlate the alert with any other recent suspicious activities on the host, such as unauthorized access attempts or changes in system configurations, to assess the broader context of the potential threat.
- Verify the legitimacy of the involved processes and connections by consulting with system owners or reviewing system documentation to rule out any false positives due to legitimate administrative activities.

### False positive analysis

- Legitimate administrative scripts or tools that use shell processes with interactive flags may trigger the rule. To manage this, identify and document these scripts, then create exceptions for their specific command-line arguments or parent processes.
- Automated maintenance tasks or cron jobs that involve shell execution with similar command-line arguments can be mistaken for reverse shell activity. Review these tasks and exclude them by specifying their unique process names or arguments.
- Development or testing environments where developers frequently use shell processes for debugging or testing purposes might cause false positives. Consider excluding these environments by filtering based on host identifiers or specific user accounts.
- Network monitoring tools or legitimate applications that use socat for network connections may appear suspicious. Identify these applications and exclude their specific process names or parent-child relationships from the detection rule.
- Custom scripts or applications that mimic reverse shell behavior for legitimate purposes should be reviewed and excluded by adding their specific process names or command-line patterns to the exception list.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious shell processes identified by the detection rule, especially those initiated by or involving the listed shell programs (e.g., bash, socat).
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise, such as unauthorized user accounts or modified system files.
- Review and reset credentials for any accounts that may have been compromised, ensuring the use of strong, unique passwords.
- Apply relevant security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Monitor network traffic for any further suspicious activity, particularly outgoing connections to unknown or suspicious IP addresses.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
