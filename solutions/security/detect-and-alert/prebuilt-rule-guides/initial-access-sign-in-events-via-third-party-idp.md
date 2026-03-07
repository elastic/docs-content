---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Okta Sign-In Events via Third-Party IdP" prebuilt detection rule.
---

# Okta Sign-In Events via Third-Party IdP

## Triage and analysis

### Investigating Okta Sign-In Events via Third-Party IdP

This rule detects sign-in events where authentication is carried out via a third-party Identity Provider (IdP).

Adversaries may attempt to add an unauthorized IdP to an Okta tenant to gain access to the tenant. Following this action, adversaries may attempt to sign in to the tenant using the unauthorized IdP. This rule detects both the addition of an unauthorized IdP and the subsequent sign-in attempt.

#### Possible investigation steps:
- Identify the third-party IdP by examining the `okta.authentication_context.issuer.id` field.
- Once the third-party IdP is identified, determine if this IdP is authorized to be used by the tenant.
- If the IdP is unauthorized, deactivate it immediately via the Okta console.
- Identify the actor associated with the IdP creation by examining the `okta.actor.id`, `okta.actor.type`, `okta.actor.alternate_id`, and `okta.actor.display_name` fields in historical data.
    - The `New Okta Identity Provider (IdP) Added by Admin` rule may be helpful in identifying the actor and the IdP creation event.
- Determine the client used by the actor. Review the `okta.client.ip`, `okta.client.user_agent.raw_user_agent`, `okta.client.zone`, `okta.client.device`, and `okta.client.id` fields.
- If the client is a device, check the `okta.device.id`, `okta.device.name`, `okta.device.os_platform`, `okta.device.os_version`, and `okta.device.managed` fields.
- Review the past activities of the actor involved in this action by checking their previous actions logged in the `okta.target` field.
- Examine the `okta.request.ip_chain` field to potentially determine if the actor used a proxy or VPN to perform this action.
- Evaluate the actions that happened just before and after this event in the `okta.event_type` field to help understand the full context of the activity.

### False positive analysis:
- It might be a false positive if this IdP is authorized to be used by the tenant.
- This may be a false positive if an authorized third-party IdP is used to sign in to the tenant but failures occurred due to an incorrect configuration.

### Response and remediation:
- If the IdP is unauthorized, deactivate it immediately via the Okta console.
- Reset the effected user's password and enforce MFA re-enrollment, if applicable.
- Mobile device forensics may be required to determine if the user's device is compromised.
- If the IdP is authorized, ensure that the actor who created it is authorized to do so.
- If the actor is unauthorized, deactivate their account via the Okta console.
- If the actor is authorized, ensure that the actor's account is not compromised.

- Block the IP address or device used in the attempts if they appear suspicious, using the data from the `okta.client.ip` and `okta.device.id` fields.
- Conduct a review of Okta policies and ensure they are in accordance with security best practices.
- If the deactivated IdP was crucial to the organization, consider adding a new IdP and removing the unauthorized IdP.

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.

