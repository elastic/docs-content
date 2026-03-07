---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unauthorized Scope for Public App OAuth2 Token Grant with Client Credentials" prebuilt detection rule.
---

# Unauthorized Scope for Public App OAuth2 Token Grant with Client Credentials

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unauthorized Scope for Public App OAuth2 Token Grant with Client Credentials

OAuth 2.0 is a protocol for authorization, allowing apps to access resources on behalf of users. Public client apps, lacking secure storage, use client credentials for token grants. Adversaries may exploit compromised credentials to request unauthorized scopes. The detection rule identifies failed token grants due to scope mismatches, signaling potential misuse of client credentials.

### Possible investigation steps

- Review the `okta.actor.display_name` field to identify the public client app involved in the failed token grant attempt and determine if it is a known or expected application.
- Examine the `okta.debug_context.debug_data.flattened.requestedScopes` field to understand which unauthorized scopes were requested and assess their potential impact if accessed.
- Investigate the `okta.actor.type` field to confirm that the actor is indeed a public client app, which lacks secure storage, and evaluate the risk of compromised credentials.
- Check the `okta.outcome.reason` field for "no_matching_scope" to verify that the failure was due to a scope mismatch, indicating an attempt to access unauthorized resources.
- Analyze the `okta.client.user_agent.raw_user_agent` field to ensure the request did not originate from known Okta integrations, which are excluded from the rule, to rule out false positives.
- Correlate the event with other security logs or alerts to identify any patterns or additional suspicious activities related to the same client credentials or IP address.

### False positive analysis

- Frequent legitimate access attempts by known public client apps may trigger false positives. To manage this, consider creating exceptions for specific `okta.actor.display_name` values that are known to frequently request scopes without malicious intent.
- Automated processes or integrations that use client credentials might occasionally request scopes not typically associated with their function. Review these processes and, if deemed non-threatening, exclude their `okta.client.user_agent.raw_user_agent` from triggering the rule.
- Development or testing environments often simulate various OAuth 2.0 token grant scenarios, which can result in false positives. Identify and exclude these environments by their `okta.actor.display_name` or other distinguishing attributes.
- Regularly review and update the list of non-threatening scopes in `okta.debug_context.debug_data.flattened.requestedScopes` to ensure that legitimate scope requests are not flagged as unauthorized.

### Response and remediation

- Immediately revoke the compromised client credentials to prevent further unauthorized access attempts.
- Conduct a thorough review of the affected public client app's access logs to identify any successful unauthorized access or data exfiltration attempts.
- Notify the application owner and relevant security teams about the incident to ensure coordinated response efforts.
- Implement additional monitoring on the affected app and associated user accounts to detect any further suspicious activities.
- Update and enforce stricter access controls and scope permissions for public client apps to minimize the risk of unauthorized scope requests.
- Consider implementing multi-factor authentication (MFA) for accessing sensitive resources to add an additional layer of security.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if broader organizational impacts exist.
