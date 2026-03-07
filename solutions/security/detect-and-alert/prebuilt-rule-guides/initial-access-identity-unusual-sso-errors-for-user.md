---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Identity Unusual SSO Authentication Errors for User" prebuilt detection rule.
---

# M365 Identity Unusual SSO Authentication Errors for User

## Triage and analysis

### Investigating M365 Identity Unusual SSO Authentication Errors for User

SSO, SAML, and federated authentication mechanisms are critical infrastructure for modern identity access. Adversaries increasingly
target these systems through token manipulation, SAML response tampering, OAuth phishing, and exploitation of federated trust
relationships rather than traditional credential brute forcing. This detection identifies when a user experiences SSO-related
authentication errors that are unusual for their typical behavior, which may indicate an attacker attempting to abuse stolen tokens or manipulate
authentication flows.

### Possible investigation steps

- Review the specific error code(s) in the `o365.audit.ErrorNumber` field to understand the nature of the authentication failure
  (e.g., token signature failure, SAML assertion tampering, cross-tenant token misuse). Reference Microsoft's AADSTS error codes
  at https://login.microsoftonline.com/error?code=<ErrorNumber> for detailed descriptions.
- Examine the source IP address and geolocation of the authentication attempt - compare against the user's typical login patterns.
- Check for concurrent authentication activity from the same user - multiple SSO errors alongside successful logins may indicate
  token replay or session hijacking attempts.
- Investigate recent OAuth application consent activity for this user - OAuth phishing campaigns often precede SSO manipulation attempts.
- Review the target application or service principal being accessed during the failed authentication to identify potential attacker objectives.
- Analyze the user's recent mailbox activity, particularly for phishing emails with OAuth consent links or suspicious authentication requests.
- Check for any recent changes to the user's federation settings, registered devices, or authentication methods.
- Correlate with Entra ID risky sign-in detections and risky user alerts for the same account.

### False positive analysis

- First-time SSO setup: Users configuring SSO access to a new federated application may encounter initial authentication errors.
  Validate whether the errors occurred during expected onboarding windows.
- Federation service outages: Widespread SSO errors affecting multiple users simultaneously often indicate infrastructure issues
  rather than targeted attacks. Check for service health incidents in the same timeframe.
- Certificate rotation: Federated authentication certificate renewals can temporarily cause signature validation errors. Verify
  if the errors align with planned certificate maintenance.
- Legitimate cross-tenant access: Users with business relationships across multiple tenants may encounter cross-tenant policy
  errors during authorized access attempts.

### Response and remediation

- If token manipulation or SAML tampering is suspected, immediately revoke all active sessions and refresh tokens for the affected user.
- Review and audit all OAuth application consents granted by the user - remove any suspicious or unrecognized applications.
- Enable Conditional Access policies requiring compliant devices and MFA for SSO authentication if not already enforced.
- If cross-tenant token misuse is detected, review and restrict external collaboration settings and cross-tenant access policies.
- For SAML assertion or signature errors, validate the integrity of federation trust certificates and metadata.
- Investigate whether the user's credentials have been compromised - enforce password reset if credential theft is suspected.
- Review Entra ID audit logs for unusual application registrations, service principal modifications, or federation setting changes.
- Escalate to the security operations team if evidence suggests active token theft, SAML Golden Ticket techniques, or OAuth phishing campaigns.
