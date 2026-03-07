---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Azure Compute Restore Point Collection Deleted by Unusual User" prebuilt detection rule.
---

# Azure Compute Restore Point Collection Deleted by Unusual User

## Triage and analysis

### Investigating Azure Compute Restore Point Collection Deleted by Unusual User

Azure Compute Restore Point Collections are critical components for disaster recovery, containing snapshots that enable point-in-time
recovery of virtual machines. Deletion of these collections can severely impact an organization's ability to recover from
incidents, making them attractive targets for adversaries conducting ransomware attacks or attempting to cover their tracks.

This rule detects when a user who has not previously deleted Restore Point Collections performs this operation, which may
indicate unauthorized activity or a compromised account.

### Possible investigation steps

- Review the `azure.activitylogs.identity.claims_initiated_by_user.name` field to identify the specific user who performed the deletion operation.
- Investigate the `azure.resource.id` or `azure.resource.name` fields to identify which Restore Point Collection was deleted and assess its criticality to business operations.
- Review the timeline of the deletion event and correlate it with other security events or user activities to identify any suspicious patterns or related activities.
- Verify whether the user account has legitimate access to perform this operation and whether this deletion was authorized through change management processes.
- Check for any other unusual activities by the same user account around the time of the deletion, such as privilege escalation attempts or access to other sensitive resources.
- Investigate whether there are any active alerts or indicators of compromise related to ransomware activity in the environment.

### False positive analysis

- Routine administrative activities by infrastructure teams may trigger this alert when team members rotate or new administrators are onboarded. Create exceptions for known administrative accounts after verification.
- Automated cleanup scripts or Azure policies that periodically remove old restore points may cause alerts. Identify and exclude service accounts used for these automated operations.
- Planned decommissioning activities or migration projects may involve legitimate deletion of restore point collections. Document these activities and create temporary exceptions during known maintenance windows.
- Testing and development environments may see frequent creation and deletion of resources. Consider excluding these environments from monitoring or adjusting the rule to focus on production resources only.

### Response and remediation

- Immediately verify the legitimacy of the deletion operation with the user or their manager. If the activity is unauthorized, proceed with incident response procedures.
- If unauthorized deletion is confirmed, immediately isolate the affected user account to prevent further malicious activity. Reset credentials and review account permissions.
- Check if the deleted Restore Point Collection can be recovered through Azure backup services or other recovery mechanisms.
- Review and audit all recent activities performed by the affected user account to identify other potentially malicious actions.
- Assess the impact on disaster recovery capabilities and inform relevant stakeholders about potential recovery limitations.
- Review access controls and permissions for Restore Point Collection management, implementing principle of least privilege where necessary.
- If ransomware activity is suspected, escalate to the security incident response team and implement broader containment measures, including checking for other indicators of ransomware such as deletion of Recovery Services vaults or backup fabric containers.
- Document the incident and update detection rules or procedures based on lessons learned.

