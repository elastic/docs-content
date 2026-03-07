---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Azure Blob Storage Permissions Modified" prebuilt detection rule.'
---

# Azure Blob Storage Permissions Modified

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Azure Blob Storage Permissions Modified

Azure Blob Storage is a service for storing large amounts of unstructured data. It uses Azure RBAC to manage access, ensuring only authorized users can modify or access data. Adversaries may exploit this by altering permissions to gain unauthorized access or disrupt operations. The detection rule monitors specific Azure activity logs for successful permission changes, alerting analysts to potential security breaches or misconfigurations.

### Possible investigation steps

- Review the Azure activity logs to identify the user or service principal associated with the permission modification event by examining the relevant fields such as `event.dataset` and `azure.activitylogs.operation_name`.
- Check the `event.outcome` field to confirm the success of the permission modification and gather details on the specific permissions that were altered.
- Investigate the context of the modification by reviewing recent activities of the identified user or service principal to determine if the change aligns with their typical behavior or role.
- Assess the potential impact of the permission change on the affected Azure Blob by evaluating the sensitivity of the data and the new access levels granted.
- Cross-reference the modification event with any recent security alerts or incidents to identify if this change is part of a broader attack pattern or misconfiguration issue.
- Consult with the relevant data owners or administrators to verify if the permission change was authorized and necessary, and if not, take corrective actions to revert the changes.

### False positive analysis

- Routine administrative changes to Azure Blob permissions by authorized personnel can trigger alerts. To manage this, create exceptions for specific user accounts or roles that frequently perform legitimate permission modifications.
- Automated scripts or tools used for regular maintenance or deployment might modify permissions as part of their operation. Identify these scripts and exclude their activity from triggering alerts by using specific identifiers or tags associated with the scripts.
- Scheduled updates or policy changes that involve permission modifications can result in false positives. Document these schedules and adjust the monitoring rules to account for these timeframes, reducing unnecessary alerts.
- Integration with third-party services that require permission changes might cause alerts. Review and whitelist these services if they are verified and necessary for operations, ensuring they do not trigger false positives.

### Response and remediation

- Immediately revoke any unauthorized permissions identified in the Azure Blob Storage to prevent further unauthorized access or data exposure.
- Conduct a thorough review of the Azure Activity Logs to identify any other suspicious activities or permission changes that may have occurred around the same time.
- Notify the security team and relevant stakeholders about the incident, providing details of the unauthorized changes and any potential data exposure.
- Implement additional monitoring on the affected Azure Blob Storage accounts to detect any further unauthorized access attempts or permission modifications.
- Escalate the incident to the incident response team if there is evidence of a broader security breach or if sensitive data has been compromised.
- Review and update Azure RBAC policies to ensure that only necessary permissions are granted, and consider implementing more granular access controls to minimize the risk of future unauthorized modifications.
- Conduct a post-incident analysis to identify the root cause of the permission change and implement measures to prevent similar incidents in the future, such as enhancing logging and alerting capabilities.

## Setup

The Azure Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
