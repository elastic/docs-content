---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Interactive Terminal Spawned via Python" prebuilt detection rule.'
---

# Interactive Terminal Spawned via Python

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Interactive Terminal Spawned via Python

Python's ability to spawn interactive terminals is a powerful feature often used for legitimate administrative tasks. However, adversaries can exploit this to escalate a basic reverse shell into a fully interactive terminal, enhancing their control over a compromised system. The detection rule identifies such abuse by monitoring processes where Python spawns a shell, focusing on specific patterns in process arguments and parent-child process relationships, indicating potential malicious activity.

### Possible investigation steps

- Review the process tree to understand the parent-child relationship, focusing on the parent process named "python*" and the child process that is a shell (e.g., bash, sh, zsh).
- Examine the command-line arguments of the parent Python process to identify the use of "pty.spawn" and the presence of the "-c" flag, which may indicate an attempt to spawn an interactive terminal.
- Check the process start event details, including the timestamp and user context, to determine if the activity aligns with expected administrative tasks or if it appears suspicious.
- Investigate the source IP address and user account associated with the process to assess if they are known and authorized entities within the network.
- Look for any related alerts or logs that might indicate prior suspicious activity, such as initial access vectors or other execution attempts, to build a timeline of events.
- Correlate this activity with any recent changes or incidents reported on the host to determine if this is part of a larger attack or an isolated event.

### False positive analysis

- Administrative scripts or automation tools that use Python to manage system processes may trigger this rule. To handle this, identify and whitelist specific scripts or tools that are known to perform legitimate tasks.
- Developers or system administrators using Python for interactive debugging or system management might inadvertently match the rule's criteria. Consider excluding processes initiated by trusted user accounts or within specific directories associated with development or administration.
- Scheduled tasks or cron jobs that utilize Python to execute shell commands could be mistaken for malicious activity. Review and exclude these tasks by specifying their unique process arguments or parent-child process relationships.
- Security tools or monitoring solutions that leverage Python for executing shell commands as part of their normal operation may also trigger this rule. Identify these tools and create exceptions based on their process signatures or execution context.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious Python processes identified in the alert, especially those spawning shell processes, to disrupt the attacker's control.
- Conduct a thorough review of the affected system for any additional signs of compromise, such as unauthorized user accounts, scheduled tasks, or modified system files.
- Reset credentials for any accounts accessed from the compromised host to prevent further unauthorized access.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Enhance monitoring and logging on the affected host and network to detect any similar activities in the future, focusing on process creation and network connections.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
