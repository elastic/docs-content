---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Okta Admin Console Login Failure" prebuilt detection rule.
---

# Okta Admin Console Login Failure

## Triage and analysis

### Investigating Okta Admin Console Login Failure

This rule detects failed authentication attempts specifically targeting the Okta Admin Console. The Admin Console provides privileged access to manage Okta configurations, users, and policies, making it a high-value target for adversaries.

Threat actors like ShinyHunters have been observed probing for valid admin credentials as part of their attack chain. Failed Admin Console access attempts often precede successful compromise through vishing (voice phishing) or credential harvesting.

#### Possible investigation steps:
- Identify the user involved by examining the `okta.actor.id`, `okta.actor.type`, `okta.actor.alternate_id`, and `okta.actor.display_name` fields.
- Review the `okta.outcome.reason` field to understand why the authentication failed (e.g., invalid credentials, MFA failure, policy violation).
- Determine the client used by the actor. Review the `okta.client.ip`, `okta.client.user_agent.raw_user_agent`, `okta.client.zone`, `okta.client.device`, and `okta.client.id` fields.
- Check if the source IP is associated with known malicious activity, VPN/proxy services, or unusual geolocations.
- Examine the `okta.request.ip_chain` field to determine if the actor used a proxy or VPN.
- Correlate with other failed login attempts from the same IP or user to identify patterns.
- Review if the targeted user has administrative privileges that would make them a high-value target.
- Check for any recent vishing or phishing reports targeting users in your organization.

### False positive analysis:
- Administrators may legitimately mistype passwords or have MFA issues.
- Automated systems or scripts may fail authentication due to expired credentials.
- Users may accidentally attempt to access the Admin Console without proper permissions.

### Response and remediation:
- If repeated failures are observed from the same IP, consider blocking the IP address at the network perimeter.
- Alert the targeted administrator about the failed access attempts.
- If the user reports not attempting to access the Admin Console, treat this as a potential account compromise attempt.
- Review and strengthen MFA requirements for Admin Console access.
- Consider implementing conditional access policies to restrict Admin Console access to trusted networks.
- If vishing is suspected, remind users of social engineering awareness and verification procedures.

