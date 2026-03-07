---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Azure Compute Snapshot Deletion by Unusual User and Resource Group" prebuilt detection rule.
---

# Azure Compute Snapshot Deletion by Unusual User and Resource Group

## Triage and analysis

### Investigating Azure Compute Snapshot Deletion by Unusual User and Resource Group

Azure disk snapshots provide point-in-time copies of managed disks, serving as critical components for backup strategies, disaster recovery plans, and forensic investigations. Snapshots enable organizations to restore data and reconstruct system states after security incidents. Adversaries aware of backup strategies may delete snapshots to prevent recovery, eliminate forensic evidence, or maximize impact before executing ransomware attacks. This detection monitors for snapshot deletion operations to identify potential attempts to compromise backup and recovery capabilities. This is a New Terms rule that looks for this behavior by a user and resource group that has not been seen in the last 7 days.

### Possible investigation steps

- Review the Azure activity logs to identify the user or service principal that initiated the snapshot deletion by examining the principal ID, UPN and user agent fields.
- Check the specific snapshot name in `azure.resource.name` to understand which backup was deleted and assess the potential impact on recovery capabilities.
- Investigate the timing of the event to correlate with any other suspicious activities, such as unusual login patterns, privilege escalation attempts, or other resource deletions.
- Examine the user's recent activity history to identify any other snapshots, disks, or Azure resources that were deleted or modified by the same principal.
- Verify if the snapshot deletion aligns with approved change requests, maintenance windows, or data retention policies in your organization.
- Check if other backup-related resources (backup vaults, recovery services) were accessed or modified around the same time.
- Review any related alerts or activities such as data encryption, VM modifications, or access policy changes that occurred before the deletion.
- Investigate if the account was recently compromised by checking for suspicious authentication events or privilege escalations.

### False positive analysis

- Legitimate cleanup of expired snapshots according to data retention policies may trigger this alert. Document approved retention management processes and consider creating exceptions for automated retention tools or scheduled cleanup activities.
- DevOps automation tools might delete temporary snapshots created during deployment or testing processes. Identify service principals used by CI/CD pipelines and consider time-based exceptions during deployment windows.
- Storage optimization initiatives may involve deleting old or redundant snapshots to reduce costs. Coordinate with infrastructure teams to understand planned optimization activities and create exceptions during documented maintenance windows.
- Disaster recovery testing may involve creating and deleting test snapshots. Work with business continuity teams to identify these patterns and create exceptions during scheduled DR testing periods.

### Response and remediation

- Immediately investigate whether the deletion was authorized by verifying with the account owner, backup administrators, or relevant stakeholders.
- If the deletion was unauthorized, disable the compromised user account or service principal immediately to prevent further damage.
- Check if the snapshot can be recovered through Azure backup services or soft-delete capabilities if enabled.
- Create new snapshots of critical disks immediately if the deleted snapshot was part of your backup strategy.
- Review and audit all Azure RBAC permissions to identify how the attacker gained snapshot deletion capabilities.
- Conduct a full security assessment to identify the initial access vector and any other compromised accounts or resources.
- Implement Azure Resource Locks on critical snapshots to prevent accidental or malicious deletion.
- Configure Azure Policy to restrict snapshot deletion permissions to only authorized backup administrators.
- Enable Azure Activity Log alerts to notify security teams immediately when snapshots are deleted.
- Review backup and disaster recovery procedures to ensure redundant backup mechanisms exist beyond Azure snapshots.
- Document the incident and update security policies and procedures to prevent similar incidents in the future.

