---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Identity Global Administrator Role Assigned" prebuilt detection rule.
---

# M365 Identity Global Administrator Role Assigned

## Triage and Analysis

### Investigating M365 Identity Global Administrator Role Assigned

The Microsoft 365 Global Administrator role grants comprehensive administrative access across Entra ID and services such as Microsoft 365 Defender, Exchange, SharePoint, and Skype for Business. Adversaries who compromise an account may assign this role to themselves or other users to ensure persistent and privileged access. This rule identifies successful assignments of this role by inspecting audit logs from Azure Active Directory (Entra ID) where the role display name matches "Administrator."

### Possible investigation steps

- Review the `user.id` and `user.name` fields to determine who performed the role assignment. Assess whether this user normally has permissions to modify high-privilege roles.
- Confirm the `event.action` is `"Add member to role."` and that the `Role_DisplayName.NewValue` is `"Global Administrator"` or a similarly privileged role.
- Review the `user.target.id` and `user.target.name` fields to identify the user or service principal that received the role.
- Inspect `o365.audit.ExtendedProperties.additionalDetails` for context on how the action was performed (e.g., via Admin Portal, Graph API).
- Pivot to sign-in logs for the assigning account to check for recent anomalies such as logins from new geolocations, unrecognized devices, or suspicious IP ranges.
- Investigate if the account assignment occurred outside of known change windows, during non-business hours, or by a user with no change history.
- Correlate with other role assignments or directory changes to check for broader role abuse or privilege escalation campaigns.

### False positive analysis

- Role assignments by IT administrators as part of routine maintenance or incident response may appear suspicious in environments without change tracking or ticket correlation.
- PIM (Privileged Identity Management) activations may temporarily elevate accounts to Global Administrator and then revoke the role afterward.
- Onboarding processes or internal audits may require temporary elevation to Global Administrator for legitimate users.
- Automation tools and scripts may trigger this alert if misconfigured to assign Global Administrator privileges during provisioning or sync jobs.

### Response and remediation

- If the assignment is unapproved or suspicious, immediately revoke the Global Administrator role from the assigned user or service principal.
- Reset credentials and initiate containment steps for the assigning account, especially if compromise is suspected.
- Enable or verify enforcement of MFA for both assigning and assigned accounts.
- Review Azure AD activity logs for additional signs of privilege misuse or suspicious directory changes.
- Notify the appropriate identity and security operations teams to investigate further and begin incident response procedures.
- Limit the number of Global Administrator accounts and enforce role-based access control (RBAC) using least privilege principles.
- Consider implementing conditional access policies to limit role assignment actions to specific networks, devices, or user groups.

