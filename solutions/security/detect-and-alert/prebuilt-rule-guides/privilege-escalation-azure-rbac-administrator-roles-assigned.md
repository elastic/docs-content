---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Azure RBAC Built-In Administrator Roles Assigned" prebuilt detection rule.
---

# Azure RBAC Built-In Administrator Roles Assigned

## Triage and Analysis

### Investigating Azure RBAC Built-In Administrator Roles Assigned

This rule identifies when a user is assigned a built-in administrator role in Azure RBAC (Role-Based Access Control). These roles provide significant privileges and can be abused by attackers for lateral movement, persistence, or privilege escalation. The privileged built-in administrator roles include Owner, Contributor, User Access Administrator, Azure File Sync Administrator, Reservations Administrator, and Role Based Access Control Administrator. Assignment can be done via the Azure portal, Azure CLI, PowerShell, or through API calls. Monitoring these assignments helps detect potential unauthorized privilege escalations.

#### Privileged Built-In Administrator Roles
- Contributor: b24988ac-6180-42a0-ab88-20f7382dd24c
- Owner: 8e3af657-a8ff-443c-a75c-2fe8c4bcb635
- Azure File Sync Administrator: 92b92042-07d9-4307-87f7-36a593fc5850
- Reservations Administrator: a8889054-8d42-49c9-bc1c-52486c10e7cd
- Role Based Access Control Administrator: f58310d9-a9f6-439a-9e8d-f62e7b41a168
- User Access Administrator: 18d7d88d-d35e-4fb5-a5c3-7773c20a72d9

### Possible investigation steps

- Identify the user who assigned the role and examine their recent activity for any suspicious actions.
- Review the source IP address and location associated with the role assignment event to assess if it aligns with expected user behavior or if it indicates potential unauthorized access.
- Check the history of role assignments for the user who was assigned the role to determine if this is a recurring pattern or a one-time event.
    - Additionally, identify the lifetime of the targeted user account to determine if it is a newly created account or an existing one.
- Determine if the user assigning the role historically has the necessary permissions to assign such roles and has done so in the past.
- Investigate any recent changes or activities performed by the newly assigned administrator to identify any suspicious actions or configurations that may have been altered.
- Correlate with other logs, such as Microsoft Entra ID sign-in logs, to identify any unusual access patterns or behaviors for the user.

### False positive analysis

- Legitimate administrators may assign built-in administrator roles during routine operations, maintenance or as required for onboarding new staff.
- Review internal tickets, change logs, or admin activity dashboards for approved operations.

### Response and remediation

- If administrative assignment was not authorized:
  - Immediately remove the built-in administrator role from the account.
  - Disable or lock the account and begin credential rotation.
  - Audit activity performed by the account after elevation, especially changes to role assignments and resource access.
- If suspicious:
  - Notify the user and confirm whether they performed the action.
  - Check for any automation or scripts that could be exploiting unused elevated access paths.
  - Review conditional access and PIM (Privileged Identity Management) configurations to limit elevation without approval.
- Strengthen posture:
  - Require MFA and approval for all privilege escalation actions.
  - Consider enabling JIT (Just-in-Time) access with expiration.

