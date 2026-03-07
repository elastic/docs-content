---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "New Okta Identity Provider (IdP) Added by Admin" prebuilt detection rule.'
---

# New Okta Identity Provider (IdP) Added by Admin

## Triage and analysis

### Investigating New Okta Identity Provider (IdP) Added by Admin

This rule detects the creation of a new Identity Provider (IdP) by a Super Administrator or Organization Administrator within Okta.

#### Possible investigation steps:
- Identify the actor associated with the IdP creation by examining the `okta.actor.id`, `okta.actor.type`, `okta.actor.alternate_id`, and `okta.actor.display_name` fields.
- Identify the IdP added by reviewing the `okta.target` field and determing if this IdP is authorized.
- Determine the client used by the actor. Review the `okta.client.ip`, `okta.client.user_agent.raw_user_agent`, `okta.client.zone`, `okta.client.device`, and `okta.client.id` fields.
- If the client is a device, check the `okta.device.id`, `okta.device.name`, `okta.device.os_platform`, `okta.device.os_version`, and `okta.device.managed` fields.
- Review the past activities of the actor involved in this action by checking their previous actions logged in the `okta.target` field.
- Examine the `okta.request.ip_chain` field to potentially determine if the actor used a proxy or VPN to perform this action.
- Evaluate the actions that happened just before and after this event in the `okta.event_type` field to help understand the full context of the activity.

### False positive analysis:
- It might be a false positive if the action was part of a planned activity or performed by an authorized person.
- Several unsuccessful attempts prior to this success, may indicate an adversary attempting to add an unauthorized IdP multiple times.

### Response and remediation:
- If the IdP is unauthorized, deactivate it immediately via the Okta console.
- If the IdP is authorized, ensure that the actor who created it is authorized to do so.
- If the actor is unauthorized, deactivate their account via the Okta console.
- If the actor is authorized, ensure that the actor's account is not compromised.
- Reset the user's password and enforce MFA re-enrollment, if applicable.
- Block the IP address or device used in the attempts if they appear suspicious, using the data from the `okta.client.ip` and `okta.device.id` fields.
- Conduct a review of Okta policies and ensure they are in accordance with security best practices.
- If the deactivated IdP was crucial to the organization, consider adding a new IdP and removing the unauthorized IdP.

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
