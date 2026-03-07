---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Mount Execution Detected via Defend for Containers" prebuilt detection rule.
---

# Mount Execution Detected via Defend for Containers

## Setup
## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Mount Execution Detected via Defend for Containers

In containerized environments, the `mount` utility is crucial for attaching file systems to the system's directory tree. When executed within a privileged container, which has extensive host capabilities, it can be exploited by adversaries to access sensitive host files, potentially leading to privilege escalation or container escapes. The detection rule identifies such misuse by monitoring the execution of `mount` in privileged containers, flagging potential security threats for further investigation.

### Possible investigation steps

- Review the alert details to confirm that the process name is "mount" and that the container's security context is marked as privileged.
- Identify the container involved in the alert by examining the container ID or name, and gather information about its purpose and the applications it runs.
- Check the container's deployment configuration to verify if it was intentionally set as privileged and assess whether this level of privilege is necessary for its function.
- Investigate the user or process that initiated the mount command within the container to determine if it aligns with expected behavior or if it indicates potential malicious activity.
- Examine the mounted file systems and directories to identify any sensitive host files that may have been accessed or exposed.
- Review logs and historical data for any previous suspicious activities associated with the same container or user to identify patterns or repeated attempts at privilege escalation.

### False positive analysis

- Routine maintenance tasks within privileged containers may trigger the rule. Exclude known maintenance scripts or processes by adding them to an exception list based on their unique identifiers or command patterns.
- Backup operations that require mounting file systems might be flagged. Identify and exclude these operations by specifying the backup process names or arguments in the rule exceptions.
- Development or testing environments often use privileged containers for convenience. If these environments are known and controlled, consider excluding them by container IDs or labels to reduce noise.
- Automated deployment tools that use mount commands in privileged containers can be mistaken for threats. Review and whitelist these tools by their process names or specific arguments to prevent false alerts.
- Certain monitoring or logging solutions may use mount operations for data collection. Verify these solutions and exclude their processes if they are legitimate and necessary for system operations.

### Response and remediation

- Immediately isolate the affected container to prevent further access to sensitive host files. This can be done by stopping the container or disconnecting it from the network.
- Review and revoke any unnecessary privileges from the container's security context to prevent similar incidents. Ensure that containers run with the least privileges necessary.
- Conduct a thorough analysis of the container's file system and logs to identify any unauthorized access or modifications to host files.
- If unauthorized access is confirmed, perform a comprehensive audit of the host system to check for any signs of compromise or privilege escalation attempts.
- Patch and update the container image and host system to address any vulnerabilities that may have been exploited.
- Implement stricter access controls and monitoring for privileged containers, ensuring that only trusted users and processes can execute sensitive commands like `mount`.
- Escalate the incident to the security operations team for further investigation and to assess the need for additional security measures or incident response actions.
