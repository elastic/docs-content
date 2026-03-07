---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Interactive Shell Spawn Detected via Defend for Containers" prebuilt detection rule.'
---

# Interactive Shell Spawn Detected via Defend for Containers

## Setup

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Interactive Shell Spawn Detected via Defend for Containers

Containers are lightweight, portable units that encapsulate applications and their dependencies, often used to ensure consistent environments across development and production. Adversaries may exploit containers by spawning interactive shells to execute unauthorized commands, potentially leading to container escape and host compromise. The detection rule identifies such threats by monitoring for shell processes initiated within containers, focusing on specific process actions and arguments indicative of interactive sessions.

### Possible investigation steps

- Review the alert details to identify the specific container ID where the interactive shell was spawned. This will help in isolating the affected container for further analysis.
- Examine the process executable and arguments, particularly looking for shell types and interactive flags (e.g., "-i", "-it"), to understand the nature of the shell session initiated.
- Check the process entry leader to determine if the shell process is part of a larger process tree, which might indicate a more complex attack chain or script execution.
- Investigate the user context under which the shell was spawned to assess if it aligns with expected user behavior or if it indicates potential unauthorized access.
- Analyze recent logs and events from the container and host to identify any preceding suspicious activities or anomalies that might have led to the shell spawning.
- Correlate the event with other security alerts or incidents to determine if this is part of a broader attack pattern or campaign targeting the environment.

### False positive analysis

- Development and testing activities may trigger this rule when developers intentionally spawn interactive shells within containers for debugging or configuration purposes. To manage this, create exceptions for specific user accounts or container IDs frequently used in development environments.
- Automated scripts or orchestration tools that use interactive shells for legitimate tasks can also cause false positives. Identify these scripts and exclude their associated process names or arguments from the rule.
- Some container management platforms might use interactive shells as part of their normal operations. Review the processes and arguments used by these platforms and add them to an exception list if they are known to be safe.
- Regular maintenance tasks that require interactive shell access, such as system updates or configuration changes, can be excluded by scheduling these tasks during known maintenance windows and temporarily adjusting the rule settings.

### Response and remediation

- Immediately isolate the affected container to prevent further unauthorized access or potential container escape. This can be done by stopping the container or disconnecting it from the network.
- Capture and preserve forensic data from the container, including logs, process lists, and network activity, to aid in further investigation and understanding of the attack vector.
- Conduct a thorough review of the container's configuration and permissions to identify and rectify any misconfigurations or vulnerabilities that may have been exploited.
- Patch and update the container image and any associated software to address known vulnerabilities that could have been leveraged by the attacker.
- Implement stricter access controls and monitoring on container environments to prevent unauthorized shell access, such as using role-based access controls and enabling audit logging.
- Escalate the incident to the security operations team for further analysis and to determine if the threat has spread to other parts of the infrastructure.
- Review and enhance detection capabilities to identify similar threats in the future, ensuring that alerts are tuned to detect unauthorized shell access attempts promptly.
