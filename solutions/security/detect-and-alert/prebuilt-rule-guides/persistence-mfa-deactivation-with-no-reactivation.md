---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "MFA Deactivation with no Re-Activation for Okta User Account" prebuilt detection rule.
---

# MFA Deactivation with no Re-Activation for Okta User Account

## Triage and analysis

### Investigating MFA Deactivation with no Re-Activation for Okta User Account

MFA is used to provide an additional layer of security for user accounts. An adversary may achieve MFA deactivation for an Okta user account to achieve persistence.

This rule fires when an Okta user account has MFA deactivated and no subsequent MFA reactivation is observed within 12 hours.

#### Possible investigation steps:

- Identify the entity related to the alert by reviewing `okta.target.alternate_id`, `okta.target.id` or `user.target.full_name` fields. This should give the username of the account being targeted. Verify if MFA is deactivated for the target entity.
- Using the `okta.target.alternate_id` field, search for MFA re-activation events where `okta.event_type` is `user.mfa.factor.activate`. Note if MFA re-activation attempts were made against the target.
- Identify the actor performing the deactivation by reviewing `okta.actor.alternate_id`, `okta.actor.id` or `user.full_name` fields. This should give the username of the account performing the action. Determine if deactivation was performed by a separate user.
- Review events where `okta.event_type` is `user.authenticate*` to determine if the actor or target accounts had suspicious login activity.
    - Geolocation details found in `client.geo*` related fields may be useful in determining if the login activity was suspicious for this user.
- Examine related administrative activity by the actor for privilege misuse or suspicious changes.

#### False positive steps:

- Determine with the target user if MFA deactivation was expected.
- Determine if MFA is required for the target user account.

#### Response and remediation:

- If the MFA deactivation was not expected, consider deactivating the user
    - This should be followed by resetting the user's password and re-enabling MFA.
- If the MFA deactivation was expected, consider adding an exception to this rule to filter false positives.
- Investigate the source of the attack. If a specific machine or network is compromised, additional steps may need to be taken to address the issue.
- Encourage users to use complex, unique passwords and consider implementing multi-factor authentication.
- Check if the compromised account was used to access or alter any sensitive data, applications or systems.
- Review the client user-agent to determine if it's a known custom application that can be whitelisted.

