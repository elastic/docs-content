---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kubernetes Denied Service Account Request via Unusual User Agent" prebuilt detection rule.
---

# Kubernetes Denied Service Account Request via Unusual User Agent

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Denied Service Account Request via Unusual User Agent

Kubernetes service accounts are integral for managing pod permissions and accessing the API server. They typically follow strict access patterns. Adversaries may exploit compromised service account credentials to probe or manipulate cluster resources, potentially leading to unauthorized access or lateral movement. The detection rule identifies anomalies by flagging unauthorized API requests from service accounts, signaling possible security breaches or misconfigurations.

### Possible investigation steps

- Review the specific service account involved in the unauthorized request by examining the kubernetes.audit.user.username field to determine which service account was used.
- Analyze the kubernetes.audit.annotations.authorization_k8s_io/decision field to confirm the request was indeed forbidden and identify the nature of the denied request.
- Investigate the source of the request by checking the originating pod or node to understand where the unauthorized request was initiated.
- Examine recent activity logs for the service account to identify any unusual patterns or deviations from its typical behavior.
- Check for any recent changes or deployments in the cluster that might have affected service account permissions or configurations.
- Assess whether there have been any recent security incidents or alerts related to the cluster that could be connected to this unauthorized request.

### False positive analysis

- Service accounts used for testing or development may generate unauthorized requests if they are not properly configured. Regularly review and update permissions for these accounts to ensure they align with their intended use.
- Automated scripts or tools that interact with the Kubernetes API might trigger false positives if they use service accounts with insufficient permissions. Ensure these tools have the necessary permissions or adjust the detection rule to exclude known benign activities.
- Misconfigured role-based access control (RBAC) settings can lead to legitimate service accounts being denied access. Conduct periodic audits of RBAC policies to verify that service accounts have appropriate permissions.
- Temporary service accounts created for specific tasks might not have the correct permissions, leading to denied requests. Consider excluding these accounts from the rule if they are known to perform non-threatening activities.
- Service accounts from third-party integrations or plugins may not have the required permissions, resulting in false positives. Validate the permissions needed for these integrations and adjust the rule to exclude their expected behavior.

### Response and remediation

- Immediately isolate the affected service account by revoking its access tokens and credentials to prevent further unauthorized API requests.
- Conduct a thorough review of the audit logs to identify any other suspicious activities or unauthorized access attempts associated with the compromised service account.
- Rotate credentials for the affected service account and any other potentially impacted accounts to mitigate the risk of further exploitation.
- Assess and remediate any misconfigurations in role-based access control (RBAC) policies that may have allowed the unauthorized request, ensuring that service accounts have the minimum necessary permissions.
- Escalate the incident to the security operations team for further investigation and to determine if additional containment measures are required.
- Implement enhanced monitoring and alerting for similar unauthorized access attempts to improve detection and response times for future incidents.
- Review and update incident response plans to incorporate lessons learned from this event, ensuring readiness for similar threats in the future.

## Setup

The Kubernetes Fleet integration with Audit Logs enabled or similarly structured data is required to be compatible with this rule.
