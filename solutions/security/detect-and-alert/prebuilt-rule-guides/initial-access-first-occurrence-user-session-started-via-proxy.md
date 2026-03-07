---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "First Occurrence of Okta User Session Started via Proxy" prebuilt detection rule.'
---

# First Occurrence of Okta User Session Started via Proxy

## Triage and analysis

### Investigating First Occurrence of Okta User Session Started via Proxy

This rule detects the first occurrence of an Okta user session started via a proxy. This rule is designed to help identify suspicious authentication behavior that may be indicative of an attacker attempting to gain access to an Okta account while remaining anonymous. This rule leverages the New Terms rule type feature where the `okta.actor.id` value is checked against the previous 7 days of data to determine if the value has been seen before for this activity.

#### Possible investigation steps:
- Identify the user involved in this action by examining the `okta.actor.id`, `okta.actor.type`, `okta.actor.alternate_id`, and `okta.actor.display_name` fields.
- Determine the client used by the actor. Review the `okta.client.ip`, `okta.client.user_agent.raw_user_agent`, `okta.client.zone`, `okta.client.device`, and `okta.client.id` fields.
- Examine the `okta.debug_context.debug_data.flattened` field for more information about the proxy used.
- Review the `okta.request.ip_chain` field for more information about the geographic location of the proxy.
- Review the past activities of the actor involved in this action by checking their previous actions.
- Evaluate the actions that happened just before and after this event in the `okta.event_type` field to help understand the full context of the activity.

### False positive analysis:
- A user may have legitimately started a session via a proxy for security or privacy reasons.

### Response and remediation:
- Review the profile of the user involved in this action to determine if proxy usage may be expected.
- If the user is legitimate and the authentication behavior is not suspicious, no action is required.
- If the user is legitimate but the authentication behavior is suspicious, consider resetting the user's password and enabling multi-factor authentication (MFA).
    - If MFA is already enabled, consider resetting MFA for the user.
- If the user is not legitimate, consider deactivating the user's account.
- Conduct a review of Okta policies and ensure they are in accordance with security best practices.
