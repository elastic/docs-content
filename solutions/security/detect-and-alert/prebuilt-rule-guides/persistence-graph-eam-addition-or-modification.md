---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID External Authentication Methods (EAM) Modified" prebuilt detection rule.
---

# Entra ID External Authentication Methods (EAM) Modified

## Triage and analysis

### Investigating Entra ID External Authentication Methods (EAM) Modified

This rule detects suspicious modifications to external authentication methods (EAMs) in Microsoft Entra ID via Microsoft Graph API. Adversaries may abuse this capability to bypass multi-factor authentication (MFA), enabling persistence or unauthorized access through bring-your-own identity provider (BYOIDP) methods.

### Possible investigation steps
- Validate that `event.action` is `"Microsoft Graph Activity"` and that `http.request.method` is `"PATCH"`, indicating a configuration change was made.
- Confirm that `url.path` contains the string `authenticationMethodsPolicy`, which is associated with external authentication settings in Entra ID.
- Review `user.id` to identify the Azure AD object ID of the user or service principal that initiated the change.
- Examine `azure.graphactivitylogs.properties.app_id` to determine the application ID that performed the action.
- Analyze `azure.graphactivitylogs.properties.scopes[]` to assess whether the request used privileged scopes such as `AuthenticationMethod.ReadWrite.All`.
- Review the geographic origin of the request using `source.geo.*` and the `source.ip` field to identify anomalous locations.
- Examine `user_agent.original` to determine whether the request was made through a browser or automation (e.g., scripted activity).
- Correlate `azure.graphactivitylogs.properties.token_issued_at` and `azure.graphactivitylogs.properties.time_generated` to assess whether the change occurred shortly after token issuance.
- Investigate additional activity by the same `user.id` or `app_id` within a short timeframe (e.g., 30 minutes) to detect related suspicious behavior.
- Use the `operation_id` or `correlation_id` to pivot across related Graph API or Entra ID activity logs, if available.

### False positive analysis
- Legitimate administrative activity may trigger this rule, such as configuring FIDO2 or enabling passwordless sign-in methods during onboarding or security upgrades.
- Some enterprise integrations or federated identity providers may programmatically update EAM settings as part of legitimate operations.
- Routine security assessments or red team exercises may include changes to authentication policies. Validate with internal teams when in doubt.
- If appropriate, filter or suppress alerts originating from known trusted service principals or administrative accounts.

### Response and remediation
- Confirm whether the user or application that made the change was authorized to do so. If not, immediately revoke access and reset credentials as needed.
- Review the application or automation that triggered the change to ensure it is legitimate. If unauthorized, disable or remove it and rotate secrets or tokens it may have accessed.
- Audit current external authentication configurations and conditional access policies to ensure no persistent backdoors were introduced.
- Revoke session tokens associated with the change using Entra ID's portal or Microsoft Graph API, and enforce reauthentication where appropriate.
- Implement stricter RBAC or conditional access policies to prevent unauthorized EAM changes in the future.
- Monitor for repeat or similar activity from the same source or identity as part of an ongoing compromise assessment.

