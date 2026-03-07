---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID OAuth User Impersonation to Microsoft Graph" prebuilt detection rule.
---

# Entra ID OAuth User Impersonation to Microsoft Graph

## Triage and analysis

### Investigating Entra ID OAuth User Impersonation to Microsoft Graph

Identifies potential phishing, session hijacking or token replay in Microsoft Entra ID. This rule detects cases where a user signs in and subsequently accesses Microsoft Graph from a different IP address using the same session ID and client application. This may indicate a successful OAuth phishing attack, session hijacking, or token replay attack, where an adversary has stolen a session cookie or refresh/access token and is impersonating the user from an alternate host or location.

This rule uses ESQL aggregations and thus has dynamically generated fields. Correlation of the values in the alert document may need to be
performed to the original sign-in and Graph events for further context.

### Possible investigation steps

- This rule relies on an aggregation-based ESQL query, therefore the alert document will contain dynamically generated fields.
    - To pivot into the original events, it is recommended to use the values captured to filter in timeline or discovery for the original sign-in and Graph events.
- Review the session ID and user ID to identify the user account involved in the suspicious activity.
- Check the source addresses involved in the sign-in and Graph access to determine if they are known or expected locations for the user.
    - The sign-in source addresses should be two, one for the initial phishing sign-in and the other when exchanging the auth code for a token by the adversary.
    - The Graph API source address should identify the IP address used by the adversary to access Microsoft Graph.
- Review the user agent strings for the sign-in and Graph access events to identify any anomalies or indicators of compromise.
- Analyze the Graph permission scopes to identify what resources were accessed and whether they align with the user's expected behavior.
- Check the timestamp difference between the sign-in and Graph access events to determine if they occurred within a reasonable time frame that would suggest successful phishing to token issuance and then Graph access.
- Identify the original sign-in event to investigation if conditional access policies were applied, such as requiring multi-factor authentication or blocking access from risky locations. In phishing scenarios, these policies likely were applied as the victim user would have been prompted to authenticate.

### False positive analysis
- This pattern may occur during legitimate device switching or roaming between networks (e.g., corporate to mobile).
- Developers or power users leveraging multiple environments may also trigger this detection if session persistence spans IP ranges. Still, this behavior is rare and warrants investigation when rapid IP switching and Graph access are involved.

### Response and remediation

- If confirmed malicious, revoke all refresh/access tokens for the user principal.
- Block the source IP(s) involved in the Graph access.
- Notify the user and reset credentials.
- Review session control policies and conditional access enforcement.
- Monitor for follow-on activity, such as lateral movement or privilege escalation.
- Review conditional access policies to ensure they are enforced correctly.

