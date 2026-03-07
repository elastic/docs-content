---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Attempt to Revoke Okta API Token" prebuilt detection rule.'
---

# Attempt to Revoke Okta API Token

## Triage and analysis

### Investigating Attempt to Revoke Okta API Token

The rule alerts when attempts are made to revoke an Okta API token. The API tokens are critical for integration services, and revoking them may lead to disruption in services. Therefore, it's important to validate these activities.

#### Possible investigation steps:
- Identify the actor associated with the API token revocation attempt. You can use the `okta.actor.alternate_id` field for this purpose.
- Determine the client used by the actor. Review the `okta.client.device`, `okta.client.ip`, `okta.client.user_agent.raw_user_agent`, `okta.client.ip_chain.ip`, and `okta.client.geographical_context` fields.
- Verify if the API token revocation was authorized or part of some planned activity.
- Check the `okta.outcome.result` and `okta.outcome.reason` fields to see if the attempt was successful or failed.
- Analyze the past activities of the actor involved in this action. An actor who usually performs such activities may indicate a legitimate reason.
- Evaluate the actions that happened just before and after this event. It can help understand the full context of the activity.

### False positive analysis:
- It might be a false positive if the action was part of a planned activity or was performed by an authorized person.

### Response and remediation:
- If unauthorized revocation attempts are confirmed, initiate the incident response process.
- Block the IP address or device used in the attempts, if they appear suspicious.
- Reset the user's password and enforce MFA re-enrollment, if applicable.
- Conduct a review of Okta policies and ensure they are in accordance with security best practices.
- If the revoked token was used for critical integrations, coordinate with the relevant team to minimize the impact.

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
