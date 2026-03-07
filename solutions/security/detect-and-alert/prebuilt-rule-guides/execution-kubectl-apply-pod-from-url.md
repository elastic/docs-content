---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubectl Apply Pod from URL" prebuilt detection rule.'
---

# Kubectl Apply Pod from URL

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubectl Apply Pod from URL

Kubectl is a command-line tool for managing Kubernetes clusters, allowing users to deploy and manage applications. Adversaries may exploit the 'kubectl apply' command with a URL to deploy malicious configurations or pods, potentially compromising the cluster. The detection rule identifies such activities by monitoring for the execution of 'kubectl apply' with URL arguments, flagging potential unauthorized deployments.

### Possible investigation steps

- Review the process execution details to confirm the presence of 'kubectl apply' with a URL argument, ensuring the command matches the query criteria.
- Identify the source IP address or hostname from which the 'kubectl apply' command was executed to determine if it originates from a known or trusted source.
- Check the URL used in the 'kubectl apply' command to assess its legitimacy and whether it points to a trusted or suspicious source.
- Investigate the user account associated with the execution of the command to verify if it has the necessary permissions and if the activity aligns with expected behavior.
- Examine the Kubernetes cluster logs for any recent changes or deployments that correspond with the time of the alert to identify any unauthorized modifications or deployments.
- Cross-reference the alert with other security tools or logs, such as network traffic analysis, to detect any related suspicious activities or data exfiltration attempts.

### False positive analysis

- Routine administrative tasks: Regular use of 'kubectl apply' with URLs for legitimate configuration updates or deployments can trigger alerts. To manage this, create exceptions for known and trusted URLs used by administrators.
- Automated deployment scripts: Continuous integration/continuous deployment (CI/CD) pipelines often use 'kubectl apply' with URLs to automate deployments. Identify and exclude these scripts by their specific process arguments or originating IP addresses.
- Monitoring and logging tools: Some monitoring solutions may use 'kubectl apply' with URLs as part of their normal operations. Review and whitelist these tools by verifying their source and purpose.
- Internal development environments: Developers may frequently use 'kubectl apply' with URLs in test environments. Establish a separate rule set or exceptions for these environments to reduce noise while maintaining security in production clusters.

### Response and remediation

- Immediately isolate the affected Kubernetes cluster to prevent further unauthorized deployments or access. This can be done by restricting network access or disabling external API access temporarily.
- Review the specific pod or configuration deployed using the 'kubectl apply' command with a URL. Identify any malicious or unauthorized changes and remove them from the cluster.
- Conduct a thorough audit of the cluster's current state to identify any other unauthorized deployments or configurations that may have been applied.
- Revoke any compromised credentials or access tokens that may have been used to execute the unauthorized 'kubectl apply' command. Ensure that all access keys and tokens are rotated.
- Escalate the incident to the security operations team for further investigation and to determine the root cause of the breach. This may involve analyzing logs and network traffic to trace the source of the attack.
- Implement network policies and role-based access controls (RBAC) to limit the ability to apply configurations from external URLs, ensuring only trusted sources are allowed.
- Enhance monitoring and alerting for similar activities by integrating with security information and event management (SIEM) systems to detect and respond to future threats promptly.
