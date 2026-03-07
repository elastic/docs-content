---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Egress Connection from Entrypoint in Container" prebuilt detection rule.
---

# Egress Connection from Entrypoint in Container

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Egress Connection from Entrypoint in Container

Containers, often used for deploying applications, start with an entrypoint script that initializes the environment. Adversaries may exploit this by embedding malicious commands to initiate unauthorized network connections, potentially breaching security boundaries. The detection rule monitors for processes named `entrypoint.sh` followed by suspicious network activity, flagging attempts to connect to external IPs, thus identifying potential threats.

### Possible investigation steps

- Review the process details for the `entrypoint.sh` script execution, focusing on the `process.entity_id` and `host.id` to understand the context of the container where the script was executed.
- Examine the network connection attempt details, particularly the `destination.ip`, to determine if the IP address is known to be malicious or associated with suspicious activity.
- Check the container's Dockerfile or image configuration to verify if the `entrypoint.sh` script is expected and whether it contains any unauthorized modifications or additions.
- Investigate the parent process of the network connection attempt using `process.parent.entity_id` to identify if there are any other suspicious processes or activities linked to the same parent.
- Correlate the event with other logs or alerts from the same `host.id` to identify any additional indicators of compromise or related suspicious activities within the same timeframe.

### False positive analysis

- Legitimate application updates or installations may trigger the rule if they involve network connections from the entrypoint script. To handle this, identify and whitelist specific applications or update processes that are known to perform such actions.
- Automated configuration management tools might execute scripts that initiate network connections as part of their normal operations. Exclude these tools by specifying their process names or parent entity IDs in the rule exceptions.
- Containers designed to perform network diagnostics or monitoring could naturally attempt connections to external IPs. Review and exclude these containers by their image names or specific entrypoint scripts.
- Development or testing environments often run scripts that connect to external services for integration testing. Consider excluding these environments by tagging them appropriately and adjusting the rule to ignore these tags.
- Scheduled maintenance scripts that run periodically and require network access might be flagged. Document these scripts and create exceptions based on their execution schedule or specific network destinations.

### Response and remediation

- Immediately isolate the affected container to prevent further unauthorized network connections. This can be done by stopping the container or disconnecting it from the network.
- Conduct a thorough review of the `entrypoint.sh` script within the container to identify and remove any malicious commands or scripts that may have been injected.
- Analyze the network traffic logs to identify any external IP addresses that the container attempted to connect to. Block these IPs at the firewall level to prevent future connections.
- Check for any signs of lateral movement or attempts to escape the container to the host system. If detected, escalate to the security team for a comprehensive investigation.
- Restore the container from a known good backup if available, ensuring that the restored version is free from any malicious modifications.
- Implement additional monitoring on the affected host and container environment to detect any similar suspicious activities in the future.
- Report the incident to the appropriate internal security team or incident response team for further analysis and to update threat intelligence databases.
