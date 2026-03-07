---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Azure Storage Account Deletions by User" prebuilt detection rule.'
---

# Azure Storage Account Deletions by User

## Triage and analysis

### Investigating Azure Storage Account Deletions by User

Azure Storage Accounts are critical infrastructure components that store application data, backups, and business-critical information. Mass deletion of storage accounts is an unusual and high-impact activity that can result in significant data loss and service disruption. Adversaries may perform bulk deletions to destroy evidence after data exfiltration, cause denial of service, or as part of ransomware campaigns targeting cloud infrastructure. This detection identifies when a single identity deletes multiple storage accounts in a short timeframe, which is indicative of potentially malicious activity.

### Possible investigation steps

- Review the Azure activity logs to identify the user or service principal that initiated the multiple storage account deletions by examining the principal ID, UPN and user agent fields in `azure.activitylogs.identity.claims_initiated_by_user.name`.
- Check the specific storage account names in `azure.resource.name` to understand which storage resources were deleted and assess the overall business impact.
- Investigate the timing and sequence of deletions to determine if they followed a pattern consistent with automated malicious activity or manual destruction.
- Examine the user's recent activity history including authentication events, privilege changes, and other Azure resource modifications to identify signs of account compromise.
- Verify if the storage account deletions align with approved change requests, maintenance windows, or decommissioning activities in your organization.
- Check if the deleted storage accounts contained critical data and whether backups are available for recovery.
- Review any related alerts or activities such as data exfiltration, unusual authentication patterns, or privilege escalation that occurred before the deletions.
- Investigate if other Azure resources (VMs, databases, resource groups) were also deleted or modified by the same principal.
- Check the authentication source and location to identify if the activity originated from an expected network location or potentially compromised session.

### False positive analysis

- Legitimate bulk decommissioning of storage accounts during infrastructure cleanup may trigger this alert. Document approved resource cleanup activities and coordinate with infrastructure teams to create exceptions during planned maintenance windows.
- Infrastructure-as-Code (IaC) automation tools or CI/CD pipelines may delete multiple test or temporary storage accounts. Identify service principals used by automation tools and consider creating exceptions for these identities when operating in non-production environments.
- Cloud resource optimization initiatives may involve bulk deletion of unused storage accounts. Coordinate with finance and infrastructure teams to understand planned cost optimization activities and schedule them during documented maintenance windows.
- Disaster recovery testing or blue-green deployment strategies may involve deletion of multiple storage accounts. Work with DevOps teams to identify these patterns and create time-based exceptions during testing periods.

### Response and remediation

- Immediately investigate whether the deletions were authorized by verifying with the account owner or relevant stakeholders.
- If the deletions were unauthorized, disable the compromised user account or service principal immediately to prevent further damage.
- Attempt to recover deleted storage accounts if soft-delete is enabled, or restore data from backups for critical storage accounts.
- Review and audit all Azure RBAC permissions to identify how the attacker gained storage account deletion capabilities (requires Contributor or Owner role).
- Conduct a full security assessment to identify the initial access vector and any other compromised accounts or resources.
- Implement Azure Resource Locks on all critical storage accounts to prevent accidental or malicious deletion.
- Configure Azure Policy to require approval workflows for storage account deletions using Azure Blueprints or custom governance solutions.
- Enable Azure Activity Log alerts to notify security teams immediately when storage accounts are deleted.
- Escalate the incident to the security operations center (SOC) or incident response team for investigation of potential broader compromise.
- Document the incident and update security policies, playbooks, and procedures to prevent similar incidents in the future.
