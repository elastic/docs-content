---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID Elevated Access to User Access Administrator" prebuilt detection rule.'
---

# Entra ID Elevated Access to User Access Administrator

## Triage and Analysis

### Investigating Entra ID Elevated Access to User Access Administrator

This rule identifies when a user elevates their permissions to the "User Access Administrator" role in Azure RBAC. This role allows full control over access management for Azure resources and can be abused by attackers for lateral movement, persistence, or privilege escalation. Since this is a New Terms rule, the alert will only trigger if the user has not performed this elevation in the past 14 days, helping reduce alert fatigue.

### Possible investigation steps

- Review the `azure.auditlogs.properties.initiated_by.user.userPrincipalName` field to identify the user who elevated access.
- Check `source.ip` and associated `source.geo.*` fields to determine the origin of the action. Confirm whether the IP, ASN, and location are expected for this user.
- Investigate the application ID from `azure.auditlogs.properties.additional_details.value` to determine which interface or method was used to elevate access.
- Pivot to Azure `signinlogs` or Entra `auditlogs` to:
  - Review recent login history for the user.
  - Look for unusual sign-in patterns or MFA prompts.
  - Determine whether the account has performed any other privilege-related operations.
- Correlate with directory role assignments or role-based access control (RBAC) modifications to assess whether the elevated access was used to add roles or modify permissions.

### False positive analysis

- Legitimate admin actions may involve access elevation during maintenance, migration, or investigations.
- Some IT departments may elevate access temporarily without leaving structured change records.
- Review internal tickets, change logs, or admin activity dashboards for approved operations.

### Response and remediation

- If elevation was not authorized:
  - Immediately remove the User Access Administrator role from the account.
  - Disable or lock the account and begin credential rotation.
  - Audit activity performed by the account after elevation, especially changes to role assignments and resource access.
- If suspicious:
  - Notify the user and confirm whether they performed the action.
  - Check for any automation or scripts that could be exploiting unused elevated access paths.
  - Review conditional access and PIM (Privileged Identity Management) configurations to limit elevation without approval.
- Strengthen posture:
  - Require MFA and approval for all privilege escalation actions.
  - Consider enabling JIT (Just-in-Time) access with expiration.
  - Add alerts for repeated or unusual use of `Microsoft.Authorization/elevateAccess/action`.
