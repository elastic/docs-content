---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Azure Activity Logs Event for a User" prebuilt detection rule.'
---

# Unusual Azure Activity Logs Event for a User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Azure Activity Logs Event for a User

This rule flags an Azure Activity Logs event when a user performs an action they don’t normally execute, highlighting potential misuse of valid credentials. It matters because attackers often blend in by operating under legitimate identities to persist, escalate, move laterally, or exfiltrate without tripping simple allowlists. A common pattern is a compromised account creating a new role assignment to grant itself elevated rights, then using that access to enumerate resources and pull data from storage.

### Possible investigation steps

- Reconstruct the timeline by pivoting on the user and ±60 minutes to collect all related Azure Activity Log entries (including those sharing the same correlation ID) and map any subsequent privilege changes, resource modifications, or data access. 
- Validate identity context by reviewing Entra ID sign-in logs for IP/ASN, geolocation, device compliance, MFA outcome, authentication protocol, and client app to spot first-time usage or impossible travel. 
- Determine whether the caller is a human account, service principal, or managed identity and confirm legitimate need by checking current and recently changed role assignments and group memberships within the affected scope. 
- Correlate the activity with approved change records and CI/CD runs (e.g., Azure DevOps, GitHub Actions, Terraform) by matching service principal/user agent and verify the pipeline or requestor was authorized and correctly scoped.

### False positive analysis

- The user temporarily covered an admin role and performed uncommon RBAC changes or resource provider registrations that are legitimate but deviate from their historical baseline.
- A scheduled maintenance or setup task ran under the user’s credentials and invoked management APIs they rarely call, generating Azure Activity Logs that appear unusual for this identity.

### Response and remediation

- Immediately revoke the user’s refresh tokens and active sessions, force a password reset, and apply a temporary Conditional Access policy to block the source IPs and device observed during the unusual operation.
- Remove any RBAC role assignments or resource policy changes created by this identity during the event window (including Owner/Contributor grants on subscriptions or resource groups) and require approvals through Privileged Identity Management before restoring access.
- If a service principal or managed identity executed the action, rotate its client secret/certificate, invalidate issued SAS tokens and storage account keys, and delete any unauthorized app registrations or automation accounts created.
- Restore affected configurations to baseline by reapplying IaC templates and verifying Key Vault access policies, storage account firewalls, and NSG rules match approved standards before re-enabling routine operations.
- Escalate to incident response and notify cloud security leadership if the unusual action involved new role assignments granting elevated rights, access to Key Vault secrets, listing storage account keys, disabling logs, or activity across multiple subscriptions.
- Implement hardening by enforcing MFA with phishing-resistant methods, enabling risk-based Conditional Access, requiring just-in-time elevation via PIM, restricting management-plane access to approved network locations, and adding alerts for role assignment writes, secret reads, and key listings.
