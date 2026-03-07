---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential release_agent Container Escape Detected via Defend for Containers" prebuilt detection rule.'
---

# Potential release_agent Container Escape Detected via Defend for Containers

## Setup

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential release_agent Container Escape Detected via Defend for Containers

In containerized environments, the release_agent file in CGroup directories can execute scripts upon process termination. Adversaries exploit this by modifying the file from privileged containers, potentially escalating privileges or escaping to the host. The detection rule monitors changes to the release_agent file, flagging unauthorized modifications indicative of such exploits.

### Possible investigation steps

- Identify the container from which the modification attempt originated, focusing on whether it has SYS_ADMIN capabilities, which could indicate a privileged container.
- Check the history of the release_agent file for any recent changes or modifications, including timestamps and user accounts involved, to understand the context of the modification.
- Investigate the processes running within the container at the time of the alert to identify any suspicious or unauthorized activities that could be related to privilege escalation attempts.
- Examine the network activity and connections from the container to detect any unusual outbound traffic that might suggest an attempt to communicate with external systems or exfiltrate data.
- Review system logs and audit logs on the host for any signs of unauthorized access or privilege escalation attempts that coincide with the alert timestamp.
- Assess the security posture of the container environment, including the configuration of CGroup directories and permissions, to identify potential vulnerabilities that could be exploited for container escape.

### False positive analysis

- Routine maintenance scripts or system updates may modify the release_agent file without malicious intent. Users can create exceptions for known maintenance activities by identifying the specific processes or scripts involved and excluding them from the rule.
- Automated container management tools might access and modify the release_agent file as part of their normal operations. Users should verify the legitimacy of these tools and whitelist their actions to prevent unnecessary alerts.
- Custom container orchestration solutions could interact with the release_agent file for legitimate reasons. Users should document these interactions and configure the rule to ignore changes made by these trusted solutions.
- Development and testing environments often involve frequent changes to container configurations, including the release_agent file. Users can reduce false positives by setting up separate monitoring profiles for these environments, allowing more lenient detection thresholds.

### Response and remediation

- Immediately isolate the affected container to prevent further unauthorized actions or potential spread to other containers or the host system.
- Revoke SYS_ADMIN capabilities from the container to limit its ability to modify critical system files and directories.
- Conduct a thorough review of the modified release_agent file to identify any malicious scripts or commands that may have been inserted.
- Restore the release_agent file to its original state from a known good backup to ensure no unauthorized scripts are executed.
- Investigate the source of the privilege escalation to determine how the adversary gained SYS_ADMIN capabilities and address any security gaps.
- Escalate the incident to the security operations team for further analysis and to assess the potential impact on the host system.
- Implement additional monitoring and alerting for changes to critical files and directories within privileged containers to enhance detection of similar threats in the future.
