---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kubernetes Service Account Secret Access" prebuilt detection rule.
---

# Kubernetes Service Account Secret Access

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Service Account Secret Access

Kubernetes service account secrets are crucial for authenticating applications within clusters, providing access to necessary resources. Adversaries may exploit these secrets to escalate privileges or move laterally within the cluster. The detection rule identifies unauthorized access by monitoring processes that interact with secret file paths or specific secret files, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the process command line and working directory to confirm if the access to the service account secrets was expected or authorized. Check for any known applications or scripts that should have access to these paths.
- Investigate the user or service account under which the process was executed to determine if it has legitimate reasons to access the Kubernetes service account secrets.
- Examine the process arguments, specifically looking for access to files like "ca.crt", "token", and "namespace", to understand the nature of the access and whether it aligns with normal operations.
- Check the history of the process and any associated processes to identify if there are any patterns of unauthorized access or if this is an isolated incident.
- Correlate the event with other logs or alerts from the same host or cluster to identify any signs of privilege escalation or lateral movement attempts.
- Assess the risk score and severity in the context of the environment to prioritize the investigation and response actions accordingly.

### False positive analysis

- Routine access by system processes or monitoring tools can trigger false positives. Identify these processes and create exceptions to prevent unnecessary alerts.
- Automated scripts or applications that regularly access service account secrets for legitimate purposes may be flagged. Review these scripts and whitelist them if they are verified as non-threatening.
- Development and testing environments often have processes accessing service account secrets as part of normal operations. Exclude these environments from the rule or adjust the rule's scope to focus on production environments.
- Frequent access by container orchestration tools or agents that manage Kubernetes clusters can be mistaken for unauthorized access. Ensure these tools are recognized and excluded from triggering alerts.
- Scheduled jobs or cron tasks that interact with service account secrets for maintenance or updates might be flagged. Validate these tasks and add them to an exception list if they are part of regular operations.

### Response and remediation

- Immediately isolate the affected pod or container to prevent further unauthorized access or lateral movement within the cluster.
- Revoke and rotate the compromised service account credentials to prevent further misuse. Ensure that new credentials are securely distributed and stored.
- Conduct a thorough review of access logs to identify any unauthorized actions or data access that occurred using the compromised credentials.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on the cluster and associated resources.
- Implement network segmentation and access controls to limit the exposure of sensitive secrets and reduce the risk of unauthorized access in the future.
- Enhance monitoring and alerting for unusual access patterns to Kubernetes service account secrets to detect similar threats promptly.
- Review and update Kubernetes security policies to enforce least privilege access and ensure that service accounts have only the necessary permissions for their intended functions.

