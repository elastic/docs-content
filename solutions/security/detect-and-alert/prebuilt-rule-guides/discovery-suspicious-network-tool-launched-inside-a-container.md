---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Network Tool Launch Detected via Defend for Containers" prebuilt detection rule.
---

# Suspicious Network Tool Launch Detected via Defend for Containers

## Setup

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Network Tool Launch Detected via Defend for Containers

Containers are lightweight, portable units that encapsulate applications and their dependencies, often used to ensure consistent environments across development and production. Adversaries exploit network tools within containers for reconnaissance or lateral movement, leveraging utilities like `nc` or `nmap` to map networks or intercept traffic. The detection rule identifies these tools' execution by monitoring process starts and arguments, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the container ID and process name from the alert to identify which container and network tool triggered the alert.
- Examine the process arguments to understand the specific command or options used, which may provide insight into the intent of the tool's execution.
- Check the container's creation and modification timestamps to determine if the container was recently deployed or altered, which could indicate suspicious activity.
- Investigate the user or service account associated with the process start event to assess if it aligns with expected behavior or if it might be compromised.
- Analyze network logs and traffic patterns from the container to identify any unusual outbound connections or data exfiltration attempts.
- Correlate the alert with other security events or logs from the same container or host to identify potential lateral movement or further malicious activity.

### False positive analysis

- Development and testing environments often use network tools for legitimate purposes such as debugging or network configuration. To manage this, create exceptions for containers identified as part of these environments by tagging them appropriately and excluding them from the rule.
- Automated scripts or orchestration tools may trigger network utilities for routine checks or maintenance tasks. Identify these scripts and whitelist their associated container IDs or process names to prevent false alerts.
- Some monitoring solutions deploy containers with built-in network tools for performance analysis. Verify the legitimacy of these containers and exclude them from the rule by using specific labels or container IDs.
- Containers used for educational or training purposes might intentionally run network tools. Ensure these containers are marked and excluded from detection by setting up rules based on their unique identifiers or labels.

### Response and remediation

- Immediately isolate the affected container to prevent further network reconnaissance or lateral movement. This can be done by restricting its network access or stopping the container entirely.
- Conduct a thorough review of the container's logs and process history to identify any unauthorized access or data exfiltration attempts. Focus on the execution of the flagged network utilities.
- Remove any unauthorized or suspicious network tools from the container to prevent further misuse. Ensure that only necessary and approved utilities are present.
- Patch and update the container image to address any vulnerabilities that may have been exploited. Rebuild and redeploy the container using the updated image.
- Implement network segmentation to limit the container's access to sensitive resources and reduce the potential impact of similar threats in the future.
- Enhance monitoring and alerting for the execution of network utilities within containers, ensuring that any future occurrences are detected promptly.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or containers have been compromised.
