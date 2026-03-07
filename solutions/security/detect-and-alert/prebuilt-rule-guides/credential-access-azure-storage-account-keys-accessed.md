---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Azure Storage Account Keys Accessed by Privileged User" prebuilt detection rule.
---

# Azure Storage Account Keys Accessed by Privileged User

## Triage and Analysis

### Investigating Azure Storage Account Keys Accessed by Privileged User

Azure Storage Account keys provide full administrative access to storage resources. While legitimate administrators may occasionally need to access these keys, Microsoft recommends using more granular access methods like Shared Access Signatures (SAS) or Azure AD authentication. This detection identifies when users with high-privilege roles (Owner, Contributor, Storage Account Contributor, or User Access Administrator) access storage account keys, particularly focusing on unusual patterns that may indicate compromise. This technique was notably observed in STORM-0501 ransomware campaigns where compromised identities retrieved keys for unauthorized storage operations.

### Possible investigation steps

- Review the `azure.activitylogs.identity.authorization.evidence.principal_id` to identify the specific user who accessed the storage account keys.
- Examine the `azure.resource.name` field to determine which storage account's keys were accessed and assess the sensitivity of data stored there.
- Check the `azure.activitylogs.identity.authorization.evidence.role` to confirm the user's assigned role and whether this level of access is justified for their job function.
- Investigate the timing and frequency of the key access event - multiple key retrievals in a short timeframe may indicate automated exfiltration attempts.
- Review the source IP address and geographic location of the access request to identify any anomalous access patterns or locations.
- Correlate this event with other activities by the same principal ID, looking for patterns such as permission escalations, unusual data access, or configuration changes.
- Check Azure AD sign-in logs for the user around the same timeframe to identify any suspicious authentication events or MFA bypasses.
- Examine subsequent storage account activities to determine if the retrieved keys were used for data access, modification, or exfiltration.

### False positive analysis

- DevOps and infrastructure teams may legitimately access storage keys during deployment or migration activities. Document these planned activities and consider creating exceptions for specific time windows.
- Emergency troubleshooting scenarios may require administrators to retrieve storage keys. Establish a process for documenting these emergency accesses and review them regularly.
- Automated backup or disaster recovery systems might use high-privilege service accounts that occasionally need key access. Consider using managed identities or service principals with more restricted permissions instead.
- Legacy applications that haven't been migrated to use SAS tokens or Azure AD authentication may still require key-based access. Plan to modernize these applications and track them as exceptions in the meantime.
- New storage account provisioning by administrators will often include initial key retrieval. Consider the age of the storage account when evaluating the risk level.

### Response and remediation

- Immediately rotate the storage account keys that were accessed using Azure Portal or Azure CLI.
- Review all recent activities on the affected storage account to identify any unauthorized data access, modification, or exfiltration attempts.
- If unauthorized access is confirmed, disable the compromised user account and initiate password reset procedures.
- Audit all storage accounts accessible by the compromised identity and rotate keys for any accounts that may have been accessed.
- Implement Entra ID authentication or SAS tokens for applications currently using storage account keys to reduce future risk.
- Configure Azure Policy to restrict the listKeys operation to specific roles or require additional approval workflows.
- Review and potentially restrict the assignment of high-privilege roles like Owner and Contributor, following the principle of least privilege.
- Enable diagnostic logging for all storage accounts to maintain detailed audit trails of access and operations.
- Consider implementing Privileged Identity Management (PIM) for just-in-time access to high-privilege roles that can list storage keys.

