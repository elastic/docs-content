---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Deactivate an Okta Policy Rule" prebuilt detection rule.
---

# Attempt to Deactivate an Okta Policy Rule

## Triage and analysis

### Investigating Attempt to Deactivate an Okta Policy Rule

Identity and Access Management (IAM) systems like Okta serve as the first line of defense for an organization's network, and are often targeted by adversaries. By disabling security rules, adversaries can circumvent multi-factor authentication, access controls, or other protective measures enforced by these policies, enabling unauthorized access, privilege escalation, or other malicious activities.

This rule detects attempts to deactivate a rule within an Okta policy, which could be indicative of an adversary's attempt to weaken an organization's security controls. A threat actor may do this to remove barriers to their activities or enable future attacks.

#### Possible investigation steps:

- Identify the actor related to the alert by reviewing `okta.actor.id`, `okta.actor.type`, `okta.actor.alternate_id`, or `okta.actor.display_name` fields in the alert.
- Review the `okta.client.user_agent.raw_user_agent` field to understand the device and software used by the actor.
- Examine the `okta.outcome.reason` field for additional context around the deactivation attempt.
- Check the `okta.outcome.result` field to confirm the policy rule deactivation attempt.
- Check if there are multiple policy rule deactivation attempts from the same actor or IP address (`okta.client.ip`).
- Check for successful logins immediately following the policy rule deactivation attempt.
- Verify whether the actor's activity aligns with typical behavior or if any unusual activity took place around the time of the deactivation attempt.

### False positive analysis:

- Check if there were issues with the Okta system at the time of the deactivation attempt. This could indicate a system error rather than a genuine threat activity.
- Check the geographical location (`okta.request.ip_chain.geographical_context`) and time of the deactivation attempt. If these match the actor's normal behavior, it might be a false positive.
- Verify the actor's administrative rights to ensure they are correctly configured.

### Response and remediation:

- If unauthorized policy rule deactivation is confirmed, initiate the incident response process.
- Immediately lock the affected actor account and require a password change.
- Consider resetting MFA tokens for the actor and require re-enrollment.
- Check if the compromised account was used to access or alter any sensitive data or systems.
- If a specific deactivation technique was used, ensure your systems are patched or configured to prevent such techniques.
- Assess the criticality of affected services and servers.
- Work with your IT team to minimize the impact on users and maintain business continuity.
- If multiple accounts are affected, consider a broader reset or audit of MFA tokens.
- Implement security best practices [outlined](https://www.okta.com/blog/2019/10/9-admin-best-practices-to-keep-your-org-secure/) by Okta.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
