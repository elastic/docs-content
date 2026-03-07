---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubernetes Unusual Decision by User Agent" prebuilt detection rule.'
---

# Kubernetes Unusual Decision by User Agent

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Unusual Decision by User Agent

Kubernetes orchestrates containerized applications, relying on API requests for operations. Typically, these requests originate from system components or trusted users with consistent user agents. Adversaries might exploit this by using atypical user agents to mask unauthorized access or misconfigurations. The detection rule identifies anomalies in user agents and response annotations, signaling potential threats in the Kubernetes environment.

### Possible investigation steps

- Review the Kubernetes audit logs for entries where the user_agent.original field is present to identify any unusual or unexpected user agents.
- Cross-reference the identified user agents with known system components and trusted users to determine if the user agent is legitimate or potentially malicious.
- Examine the kubernetes.audit.stage field for "ResponseComplete" entries to understand the context and outcome of the requests associated with the unusual user agent.
- Investigate the source IP addresses and associated usernames in the audit logs to identify any patterns or anomalies that could indicate unauthorized access.
- Check for any recent changes or deployments in the Kubernetes environment that might explain the presence of unusual user agents or unexpected behavior.
- Assess the risk and impact of the detected anomaly by considering the sensitivity of the accessed resources and the permissions associated with the user account involved.

### False positive analysis

- System components or trusted users with legitimate but infrequent user agents may trigger the rule. To manage this, identify these user agents and add them to an exception list to prevent unnecessary alerts.
- Automated scripts or tools used for maintenance or monitoring might use unique user agents. Regularly review these tools and update the exception list to include their user agents if they are verified as non-threatening.
- New deployments or updates to Kubernetes components can introduce new user agents temporarily. Monitor these changes and adjust the rule exceptions accordingly to accommodate expected behavior during these periods.
- Third-party integrations or plugins may use distinct user agents. Validate these integrations and, if deemed safe, include their user agents in the exception list to reduce false positives.

### Response and remediation

- Immediately isolate the affected Kubernetes node or cluster to prevent further unauthorized access or potential lateral movement by the adversary.
- Review and terminate any suspicious or unauthorized sessions identified in the audit logs to cut off any active malicious activity.
- Revoke and rotate credentials associated with the compromised user agent to prevent further unauthorized access using the same credentials.
- Conduct a thorough review of the affected system's configurations and permissions to identify and rectify any misconfigurations or overly permissive access controls.
- Implement additional monitoring and logging for the affected systems to detect any further anomalies or unauthorized activities promptly.
- Escalate the incident to the security operations team for a comprehensive investigation and to determine if any data exfiltration or further compromise has occurred.
- Update and enhance detection rules and alerts to better identify similar anomalies in user agents and response annotations in the future, ensuring quicker response times.
