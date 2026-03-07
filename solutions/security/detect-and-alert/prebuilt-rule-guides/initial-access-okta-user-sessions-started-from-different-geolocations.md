---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Okta User Sessions Started from Different Geolocations" prebuilt detection rule.'
---

# Okta User Sessions Started from Different Geolocations

## Triage and analysis

### Investigating Okta User Sessions Started from Different Geolocations

This rule detects when a specific Okta actor has multiple sessions started from different geolocations. Adversaries may attempt to launch an attack by using a list of known usernames and passwords to gain unauthorized access to user accounts from different locations.

#### Possible investigation steps:
- Since this is an ESQL rule, the `okta.actor.alternate_id` and `okta.client.id` values can be used to pivot into the raw authentication events related to this alert.
- Identify the users involved in this action by examining the `okta.actor.id`, `okta.actor.type`, `okta.actor.alternate_id`, and `okta.actor.display_name` fields.
- Determine the device client used for these actions by analyzing `okta.client.ip`, `okta.client.user_agent.raw_user_agent`, `okta.client.zone`, `okta.client.device`, and `okta.client.id` fields.
- With Okta end users identified, review the `okta.debug_context.debug_data.dt_hash` field.
    - Historical analysis should indicate if this device token hash is commonly associated with the user.
- Review the `okta.event_type` field to determine the type of authentication event that occurred.
    - If the event type is `user.authentication.sso`, the user may have legitimately started a session via a proxy for security or privacy reasons.
    - If the event type is `user.authentication.password`, the user may be using a proxy to access multiple accounts for password spraying.
    - If the event type is `user.session.start`, the source may have attempted to establish a session via the Okta authentication API.
- Review the past activities of the actor(s) involved in this action by checking their previous actions.
- Evaluate the actions that happened just before and after this event in the `okta.event_type` field to help understand the full context of the activity.
    - This may help determine the authentication and authorization actions that occurred between the user, Okta and application.

### False positive analysis:
- It is very rare that a legitimate user would have multiple sessions started from different geo-located countries in a short time frame.

### Response and remediation:
- If the user is legitimate and the authentication behavior is not suspicious based on device analysis, no action is required.
- If the user is legitimate but the authentication behavior is suspicious, consider resetting passwords for the users involves and enabling multi-factor authentication (MFA).
    - If MFA is already enabled, consider resetting MFA for the users.
- If any of the users are not legitimate, consider deactivating the user's account.
- Conduct a review of Okta policies and ensure they are in accordance with security best practices.
- Check with internal IT teams to determine if the accounts involved recently had MFA reset at the request of the user.
    - If so, confirm with the user this was a legitimate request.
    - If so and this was not a legitimate request, consider deactivating the user's account temporarily.
        - Reset passwords and reset MFA for the user.
- If this is a false positive, consider adding the `okta.debug_context.debug_data.dt_hash` field to the `exceptions` list in the rule.
    - This will prevent future occurrences of this event for this device from triggering the rule.
    - Alternatively adding `okta.client.ip` or a CIDR range to the `exceptions` list can prevent future occurrences of this event from triggering the rule.
        - This should be done with caution as it may prevent legitimate alerts from being generated.
