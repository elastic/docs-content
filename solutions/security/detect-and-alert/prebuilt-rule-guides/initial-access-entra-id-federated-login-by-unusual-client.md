---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID Service Principal Federated Credential Authentication by Unusual Client" prebuilt detection rule.'
---

# Entra ID Service Principal Federated Credential Authentication by Unusual Client

## Triage and analysis

### Investigating Entra ID Service Principal Federated Credential Authentication by Unusual Client

If this rule triggers, it indicates that a service principal has authenticated using a federated identity credential for the first time within the historical window. This means that Entra ID validated a JWT token potentially issued by an external OIDC identity provider and issued an access token for the service principal. While this can be legitimate for CI/CD workflows (e.g., GitHub Actions, Azure DevOps, Kubernetes OIDC), it can also indicate abuse by adversaries who have configured rogue identity providers (BYOIDP) to authenticate as compromised applications. For BYOIDP attacks, this is the moment the adversary's rogue identity provider is used to authenticate as the
compromised application for the first time.

### Possible investigation steps

- Identify the service principal using `azure.signinlogs.properties.app_id` and `app_display_name`.
- Critical: Check the application's federated credential configuration in Entra ID:
  - What is the issuer URL? Is it a known legitimate provider (GitHub Actions, Azure DevOps, Kubernetes)?
  - When was the federated credential added? Was it recent?
  - Who added the federated credential?
- Review the `service_principal_credential_thumbprint` - does it match expected certificates?
- Investigate the source IP (`azure.signinlogs.caller_ip_address`) - is it from expected CI/CD infrastructure?
- Check what resources were accessed after authentication using `azure.signinlogs.properties.resource_display_name`.
- Correlate with Graph Activity logs to see what API calls were made with this token.
- Use the `correlation_id` to find related sign-in and activity events.
- Review audit logs for recent changes to this application's federated credentials.

### False positive analysis

- Legitimate CI/CD pipelines using GitHub Actions, Azure DevOps, or Kubernetes OIDC will trigger this rule on first use.
- New application deployments with workload identity federation are expected to show as new behavior.
- Validate the issuer URL against approved identity providers before dismissing.
- Create baseline of applications expected to use federated credentials.

### Response and remediation

- If this is unexpected federated auth for the application, immediately investigate the federated credential configuration.
- Review the external IdP issuer URL configured on the application - is it legitimate?
- If BYOIDP is confirmed:
    - Remove the malicious federated credential immediately.
    - Revoke active sessions and tokens for the affected service principal.
    - Audit what actions were performed using the compromised identity.
    - Investigate how the federated credential was added (compromised admin account).
