---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Azure Storage Account Deletion by Unusual User" prebuilt detection rule.
---

# Azure Storage Account Deletion by Unusual User

## Triage and analysis

### Investigating Azure Storage Account Deletion by Unusual User

Azure Storage Accounts provide scalable cloud storage for applications and services. Deletion of storage accounts is a high-impact operation that permanently removes all contained data including blobs, files, queues, and tables. Adversaries may delete storage accounts to destroy evidence of their activities, disrupt business operations, or cause denial of service as part of ransomware or destructive attacks. This detection monitors for successful storage account deletion operations to identify potential malicious activity.

### Possible investigation steps

- Review the Azure activity logs to identify the user or service principal that initiated the storage account deletion by examining the principal ID, UPN and user agent fields.
- Check the specific storage account name in `azure.resource.name` to understand which storage resources were deleted and assess the business impact.
- Investigate the timing of the event to correlate with any other suspicious activities, such as unusual login patterns, privilege escalation attempts, or other resource deletions.
- Examine the user's recent activity history to identify any other storage accounts or Azure resources that were deleted or modified by the same principal.
- Verify if the storage account deletion aligns with approved change requests or maintenance windows in your organization.
- Check if the deleted storage account contained critical data and whether backups are available for recovery.
- Review any related alerts or activities such as data exfiltration, configuration changes, or access policy modifications that occurred before the deletion.
- Investigate if the account was recently compromised by checking for suspicious authentication events or privilege escalations.

### False positive analysis

- Legitimate decommissioning of unused storage accounts may trigger this alert. Document approved storage account cleanup activities and coordinate with infrastructure teams to understand planned deletions.
- DevOps automation tools might delete temporary storage accounts as part of infrastructure lifecycle management. Identify service principals used by CI/CD pipelines and consider creating exceptions for these automated processes.
- Testing and development environments may have frequent storage account creation and deletion cycles. Consider filtering out non-production storage accounts if appropriate for your environment.
- Cost optimization initiatives may involve deleting unused or redundant storage accounts. Coordinate with finance and infrastructure teams to understand planned resource optimization activities.

### Response and remediation

- Immediately investigate whether the deletion was authorized by verifying with the account owner or relevant stakeholders.
- If the deletion was unauthorized, attempt to recover the storage account if soft-delete is enabled, or restore data from backups.
- Disable the compromised user account or service principal if unauthorized activity is confirmed and investigate how the credentials were obtained.
- Review and restrict Azure RBAC permissions to ensure only authorized users have storage account deletion capabilities (requires Contributor or Owner role).
- Implement Azure Resource Locks to prevent accidental or malicious deletion of critical storage accounts.
- Configure Azure Activity Log alerts to notify security teams immediately when storage accounts are deleted.
- Conduct a full security assessment to identify any other compromised resources or accounts and look for indicators of broader compromise.
- Document the incident and update security policies and procedures to prevent similar incidents in the future.

