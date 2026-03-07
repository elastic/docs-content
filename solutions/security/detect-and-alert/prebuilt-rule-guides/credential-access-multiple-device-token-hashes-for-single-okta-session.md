---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Multiple Device Token Hashes for Single Okta Session" prebuilt detection rule.
---

# Multiple Device Token Hashes for Single Okta Session

## Triage and analysis

### Investigating Multiple Device Token Hashes for Single Okta Session

This rule detects when a specific Okta actor has multiple device token hashes for a single Okta session. This may indicate an authenticated session has been hijacked or is being used by multiple devices. Adversaries may hijack a session to gain unauthorized access to Okta admin console, applications, tenants, or other resources.

#### Possible investigation steps:
- Since this is an ESQL rule, the `okta.actor.alternate_id` and `okta.authentication_context.external_session_id` values can be used to pivot into the raw authentication events related to this alert.
- Identify the users involved in this action by examining the `okta.actor.id`, `okta.actor.type`, `okta.actor.alternate_id`, and `okta.actor.display_name` fields.
- Determine the device client used for these actions by analyzing `okta.client.ip`, `okta.client.user_agent.raw_user_agent`, `okta.client.zone`, `okta.client.device`, and `okta.client.id` fields.
- With Okta end users identified, review the `okta.debug_context.debug_data.dt_hash` field.
    - Historical analysis should indicate if this device token hash is commonly associated with the user.
- Review the `okta.event_type` field to determine the type of authentication event that occurred.
    - Authentication events have been filtered out to focus on Okta activity via established sessions.
- Review the past activities of the actor(s) involved in this action by checking their previous actions.
- Evaluate the actions that happened just before and after this event in the `okta.event_type` field to help understand the full context of the activity.
    - This may help determine the authentication and authorization actions that occurred between the user, Okta and application.
- Aggregate by `okta.actor.alternate_id` and `event.action` to determine the type of actions that are being performed by the actor(s) involved in this action.
    - If various activity is reported that seems to indicate actions from separate users, consider deactivating the user's account temporarily.

### False positive analysis:
- It is very rare that a legitimate user would have multiple device token hashes for a single Okta session as DT hashes do not change after an authenticated session is established.

### Response and remediation:
- Consider stopping all sessions for the user(s) involved in this action.
- If this does not appear to be a false positive, consider resetting passwords for the users involved and enabling multi-factor authentication (MFA).
    - If MFA is already enabled, consider resetting MFA for the users.
- If any of the users are not legitimate, consider deactivating the user's account.
- Conduct a review of Okta policies and ensure they are in accordance with security best practices.
- Check with internal IT teams to determine if the accounts involved recently had MFA reset at the request of the user.
    - If so, confirm with the user this was a legitimate request.
    - If so and this was not a legitimate request, consider deactivating the user's account temporarily.
        - Reset passwords and reset MFA for the user.
- Alternatively adding `okta.client.ip` or a CIDR range to the `exceptions` list can prevent future occurrences of this event from triggering the rule.
    - This should be done with caution as it may prevent legitimate alerts from being generated.

