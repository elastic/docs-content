---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Attempt to Deactivate an Okta Network Zone" prebuilt detection rule.'
---

# Attempt to Deactivate an Okta Network Zone

## Triage and analysis

### Investigating Attempt to Deactivate an Okta Network Zone

The Okta network zones can be configured to restrict or limit access to a network based on IP addresses or geolocations. Deactivating a network zone in Okta may remove or weaken the security controls of an organization, which might be an indicator of an adversary's attempt to evade defenses.

#### Possible investigation steps

- Identify the actor related to the alert by reviewing the `okta.actor.id`, `okta.actor.type`, `okta.actor.alternate_id`, or `okta.actor.display_name` fields.
- Examine the `event.action` field to confirm the deactivation of a network zone.
- Check the `okta.target.id`, `okta.target.type`, `okta.target.alternate_id`, or `okta.target.display_name` to identify the network zone that was deactivated.
- Investigate the `event.time` field to understand when the event happened.
- Review the actor's activities before and after the event to understand the context of this event.

### False positive analysis

- Check the `okta.client.user_agent.raw_user_agent` field to understand the device and software used by the actor. If these match the actor's normal behavior, it might be a false positive.
- Check if the actor is a known administrator or part of the IT team who might have a legitimate reason to deactivate a network zone.
- Verify the actor's actions with any known planned changes or maintenance activities.

### Response and remediation

- If unauthorized access or actions are confirmed, immediately lock the affected actor account and require a password change.
- Re-enable the deactivated network zone if it was deactivated without authorization.
- Review and update the privileges of the actor who initiated the deactivation.
- Check the security policies and procedures to identify any gaps and update them as necessary.
- Implement additional monitoring and logging of Okta events to improve visibility of user actions.
- Communicate and train the employees about the importance of following proper procedures for modifying network zone settings.

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
