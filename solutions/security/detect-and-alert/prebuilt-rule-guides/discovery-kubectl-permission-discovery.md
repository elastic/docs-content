---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubectl Permission Discovery" prebuilt detection rule.'
---

# Kubectl Permission Discovery

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubectl Permission Discovery

Kubectl is a command-line tool for interacting with Kubernetes clusters, allowing users to manage applications and resources. Adversaries may exploit the "kubectl auth can-i" command to probe for permission misconfigurations, potentially leading to unauthorized access or privilege escalation. The detection rule identifies this activity by monitoring specific command executions on Linux systems, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the process execution details to confirm the use of the "kubectl auth can-i" command, focusing on the process name "kubectl" and arguments "auth" and "can-i".
- Identify the user account associated with the execution of the command to determine if it aligns with expected administrative activity or if it indicates potential unauthorized access.
- Check the timing and frequency of the command execution to assess whether it corresponds with routine operations or suggests suspicious behavior.
- Investigate the source IP address or hostname from which the command was executed to verify if it originates from a known and trusted environment.
- Examine related logs and events around the time of the alert to identify any subsequent actions that might indicate privilege escalation or unauthorized access attempts.
- Cross-reference the alert with any recent changes or incidents in the Kubernetes cluster to determine if the command execution is part of a broader security concern.

### False positive analysis

- Routine administrative checks by authorized personnel can trigger the rule. To manage this, create exceptions for specific user accounts or roles that regularly perform these checks as part of their job duties.
- Automated scripts or monitoring tools that verify permissions as part of their normal operation may cause false positives. Identify these scripts and whitelist their execution paths or associated service accounts.
- Development and testing environments where developers frequently check permissions might lead to alerts. Consider excluding these environments from the rule or adjusting the risk score for these specific contexts.
- Scheduled audits or compliance checks that involve permission verification can be mistaken for malicious activity. Document these activities and set up time-based exceptions to prevent unnecessary alerts during known audit periods.

### Response and remediation

- Immediately isolate the affected Kubernetes cluster to prevent further unauthorized access or privilege escalation.
- Revoke any suspicious or unauthorized credentials or tokens identified during the investigation to prevent further misuse.
- Conduct a thorough review of the Kubernetes Role-Based Access Control (RBAC) configurations to identify and rectify any permission misconfigurations.
- Implement stricter access controls and least privilege principles for Kubernetes users and service accounts to minimize the risk of unauthorized access.
- Monitor for any additional suspicious activity or anomalies in the cluster, focusing on access patterns and command executions.
- Escalate the incident to the security operations team for further analysis and to determine if additional clusters or systems are affected.
- Update detection and monitoring systems to enhance visibility and alerting for similar permission discovery attempts in the future.
