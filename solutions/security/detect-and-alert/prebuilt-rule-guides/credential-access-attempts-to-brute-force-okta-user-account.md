---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempts to Brute Force an Okta User Account" prebuilt detection rule.
---

# Attempts to Brute Force an Okta User Account

## Triage and analysis

### Investigating Attempts to Brute Force an Okta User Account

Brute force attacks aim to guess user credentials through exhaustive trial-and-error attempts. In this context, Okta accounts are targeted.

This rule fires when an Okta user account has been locked out 3 times within a 3-hour window. This could indicate an attempted brute force or password spraying attack to gain unauthorized access to the user account. Okta's default authentication policy locks a user account after 10 failed authentication attempts.

#### Possible investigation steps:

- Identify the actor related to the alert by reviewing `okta.actor.alternate_id` field in the alert. This should give the username of the account being targeted.
- Review the `okta.event_type` field to understand the nature of the events that led to the account lockout.
- Check the `okta.severity` and `okta.display_message` fields for more context around the lockout events.
- Look for correlation of events from the same IP address. Multiple lockouts from the same IP address might indicate a single source for the attack.
- If the IP is not familiar, investigate it. The IP could be a proxy, VPN, Tor node, cloud datacenter, or a legitimate IP turned malicious.
- Determine if the lockout events occurred during the user's regular activity hours. Unusual timing may indicate malicious activity.
- Examine the authentication methods used during the lockout events by checking the `okta.authentication_context.credential_type` field.

### False positive analysis:

- Determine whether the account owner or an internal user made repeated mistakes in entering their credentials, leading to the account lockout.
- Ensure there are no known network or application issues that might cause these events.

### Response and remediation:

- Alert the user and your IT department immediately.
- If unauthorized access is confirmed, initiate your incident response process.
- Investigate the source of the attack. If a specific machine or network is compromised, additional steps may need to be taken to address the issue.
- Require the affected user to change their password.
- If the attack is ongoing, consider blocking the IP address initiating the brute force attack.
- Implement account lockout policies to limit the impact of brute force attacks.
- Encourage users to use complex, unique passwords and consider implementing multi-factor authentication.
- Check if the compromised account was used to access or alter any sensitive data or systems.

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
