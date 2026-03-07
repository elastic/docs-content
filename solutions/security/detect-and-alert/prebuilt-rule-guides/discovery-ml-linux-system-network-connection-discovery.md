---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Linux Network Connection Discovery" prebuilt detection rule.
---

# Unusual Linux Network Connection Discovery

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Linux Network Connection Discovery

In Linux environments, network connection discovery tools help administrators understand system connectivity. Adversaries exploit these tools to map networks, aiding in lateral movement and further attacks. The detection rule leverages machine learning to identify atypical usage patterns by unusual users, signaling potential account compromise or unauthorized network probing activities.

### Possible investigation steps

- Review the alert details to identify the specific user account and the command executed that triggered the alert.
- Check the user's activity history to determine if this behavior is consistent with their normal usage patterns or if it is anomalous.
- Investigate the source IP address and hostname associated with the command execution to verify if they are known and trusted within the network.
- Examine system logs for any additional suspicious activities or commands executed by the same user account around the time of the alert.
- Assess the user's access permissions and recent changes to their account to identify any unauthorized modifications or potential compromise.
- Correlate the alert with other security events or alerts to determine if this activity is part of a larger attack pattern or campaign.

### False positive analysis

- Routine administrative tasks by system administrators can trigger alerts. Regularly review and whitelist known administrator accounts performing legitimate network discovery.
- Automated scripts or monitoring tools that perform network checks may be flagged. Identify and exclude these scripts from triggering alerts by adding them to an exception list.
- Uncommon troubleshooting activities by support teams might be misidentified. Document and approve these activities to prevent false positives.
- Scheduled maintenance activities involving network discovery should be accounted for. Create a schedule-based exception to avoid unnecessary alerts during these periods.
- New employees or contractors performing legitimate network discovery as part of their onboarding process can be mistaken for threats. Ensure their activities are monitored and approved by the IT department.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes or sessions initiated by the unusual user to halt ongoing network discovery activities.
- Conduct a thorough review of the affected user's account activity and permissions to identify any unauthorized changes or access patterns.
- Reset the credentials of the compromised account and enforce multi-factor authentication to prevent further unauthorized access.
- Analyze network logs and system logs to identify any additional systems that may have been accessed or probed by the threat actor.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or accounts are compromised.
- Update and enhance network monitoring and alerting rules to detect similar unauthorized network discovery activities in the future.
