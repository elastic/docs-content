---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID Actor Token User Impersonation Abuse" prebuilt detection rule.
---

# Entra ID Actor Token User Impersonation Abuse

## Triage and analysis

### Investigating Entra ID Actor Token User Impersonation Abuse

This rule detects when Microsoft services use actor tokens to perform operations in audit logs. Actor tokens are undocumented backend mechanisms used by Microsoft for service-to-service (S2S) communication. They appear with a mismatch: the service's display name but the impersonated user's UPN. While some operations legitimately use actor tokens, unexpected usage may indicate exploitation of CVE-2025-55241, which allowed attackers to obtain Global Admin privileges across any Entra ID tenant. Note that this vulnerability has been patched by Microsoft as of September 2025.

### Possible investigation steps

- Review the `azure.auditlogs.properties.initiated_by.user.userPrincipalName` field to identify which service principals are exhibiting this behavior.
- Check the `azure.auditlogs.properties.initiated_by.user.displayName` to confirm these are legitimate Microsoft services.
- Analyze the actions performed by these service principals - look for privilege escalations, permission grants, or unusual administrative operations.
- Review the timing and frequency of these events to identify potential attack patterns or automated exploitation.
- Cross-reference with recent administrative changes or service configurations that might explain legitimate use cases.
- Check if any new applications or service principals were registered recently that could be related to this activity.
- Investigate any correlation with other suspicious authentication events or privilege escalation attempts in your tenant.

### False positive analysis

- Legitimate Microsoft service migrations or updates may temporarily exhibit this behavior.
- Third-party integrations using Microsoft Graph or other APIs might trigger this pattern during normal operations.
- Automated administrative tools or scripts using service principal authentication could be misconfigured.

### Response and remediation

- Immediately review and audit all service principal permissions and recent consent grants in your Entra ID tenant.
- Disable or restrict any suspicious service principals exhibiting this behavior until verified.
- Review and revoke any unnecessary application permissions, especially those with high privileges.
- Enable and review Entra ID audit logs for any permission grants or role assignments made by these service principals.
- Implement Conditional Access policies to restrict service principal authentication from unexpected locations or conditions.
- Enable Entra ID Identity Protection to detect and respond to risky service principal behaviors.
- Review and harden application consent policies to prevent unauthorized service principal registrations.
- Consider implementing privileged identity management (PIM) for service principal role assignments.

