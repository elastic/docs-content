---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Attempt to Deactivate an Okta Application" prebuilt detection rule.'
---

# Attempt to Deactivate an Okta Application

## Triage and analysis

### Investigating Attempt to Deactivate an Okta Application

This rule detects attempts to deactivate an Okta application. Unauthorized deactivation could lead to disruption of services and pose a significant risk to the organization.

#### Possible investigation steps:
- Identify the actor associated with the deactivation attempt by examining the `okta.actor.id`, `okta.actor.type`, `okta.actor.alternate_id`, and `okta.actor.display_name` fields.
- Determine the client used by the actor. Review the `okta.client.ip`, `okta.client.user_agent.raw_user_agent`, `okta.client.zone`, `okta.client.device`, and `okta.client.id` fields.
- If the client is a device, check the `okta.device.id`, `okta.device.name`, `okta.device.os_platform`, `okta.device.os_version`, and `okta.device.managed` fields.
- Understand the context of the event from the `okta.debug_context.debug_data` and `okta.authentication_context` fields.
- Check the `okta.outcome.result` and `okta.outcome.reason` fields to see if the attempt was successful or failed.
- Review the past activities of the actor involved in this action by checking their previous actions logged in the `okta.target` field.
- Analyze the `okta.transaction.id` and `okta.transaction.type` fields to understand the context of the transaction.
- Evaluate the actions that happened just before and after this event in the `okta.event_type` field to help understand the full context of the activity.

### False positive analysis:
- It might be a false positive if the action was part of a planned activity, performed by an authorized person, or if the `okta.outcome.result` field shows a failure.
- An unsuccessful attempt might also indicate an authorized user having trouble rather than a malicious activity.

### Response and remediation:
- If unauthorized deactivation attempts are confirmed, initiate the incident response process.
- Block the IP address or device used in the attempts if they appear suspicious, using the data from the `okta.client.ip` and `okta.device.id` fields.
- Reset the user's password and enforce MFA re-enrollment, if applicable.
- Conduct a review of Okta policies and ensure they are in accordance with security best practices.
- If the deactivated application was crucial for business operations, coordinate with the relevant team to reactivate it and minimize the impact.

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
