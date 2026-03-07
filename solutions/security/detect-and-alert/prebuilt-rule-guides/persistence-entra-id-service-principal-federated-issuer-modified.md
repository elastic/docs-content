---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID Federated Identity Credential Issuer Modified" prebuilt detection rule.'
---

# Entra ID Federated Identity Credential Issuer Modified

## Triage and analysis

### Investigating Entra ID Federated Identity Credential Issuer Modified

This rule detects when the issuer URL within a federated identity credential is modified on an Entra ID application. Federated identity credentials allow applications to authenticate using tokens from external identity providers (like GitHub Actions, AWS, etc.) without managing secrets. Adversaries can abuse this by changing the issuer to an attacker-controlled identity provider, allowing them to generate valid tokens and authenticate as the application's service principal.

This technique provides persistent access to Azure resources with the application's permissions and bypasses secret-based authentication controls.

### Possible investigation steps

- Review `azure.auditlogs.properties.initiated_by.user.userPrincipalName` and `ipAddress` to identify who made the change and from where.
- Examine the `Esql.external_idp_old_issuer` and `Esql.external_idp_new_issuer` fields to determine if the new issuer is expected or potentially malicious.
- Check if the new issuer domain is controlled by the organization or if it's an external/suspicious domain.
- Review the application's assigned roles and permissions to understand the scope of access gained.
- Use `azure.correlation_id` to pivot to related changes in the same session.
- Check for subsequent Azure sign-in activity using the modified federated credential.
- Investigate if the application has been used to access sensitive resources after the change.

### False positive analysis

- Legitimate migrations from one identity provider to another (e.g., GitHub to GitLab) may trigger this detection.
- DevOps teams may update issuer URLs as part of CI/CD pipeline changes.
- Validate any changes with the application owner or DevOps team before taking action.

### Response and remediation

- If the change is unauthorized, immediately remove or revert the federated identity credential.
- Rotate any secrets or certificates associated with the application.
- Review Azure sign-in logs and audit logs for any unauthorized activity using the application's identity.
- Disable the application or service principal if compromise is confirmed.
- Investigate how the unauthorized change occurred (e.g., compromised admin account, over-privileged service principal).
- Implement conditional access policies and PIM (Privileged Identity Management) to protect application management operations.
