---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID OAuth Flow by Microsoft Authentication Broker to Device Registration Service (DRS)" prebuilt detection rule.'
---

# Entra ID OAuth Flow by Microsoft Authentication Broker to Device Registration Service (DRS)

## Triage and analysis

### Investigating Entra ID OAuth Flow by Microsoft Authentication Broker to Device Registration Service (DRS)

This rule identifies potential OAuth phishing behavior in Microsoft Entra ID where two OAuth authorization flows are observed in quick succession, sharing the same user principal and session ID but originating from different IP addresses. The client application is the Microsoft Authentication Broker, and the target resource is the Device Registration Service (DRS). This pattern is indicative of adversaries attempting to phish targets for OAuth sessions by tricking users into authenticating through a crafted URL, which then allows the attacker to obtain an authorization code and exchange it for access and refresh tokens.

### Possible Investigation Steps:

- `target`: The user principal name targeted by the authentication broker. Investigate whether this user has recently registered a device, signed in from new IPs, or had password resets or MFA changes.
- `session_id`: Used to correlate all events in the OAuth flow. All sign-ins in the alert share the same session, suggesting shared or hijacked state.
- `unique_token_id`: Lists tokens generated in the flow. If multiple IDs exist in the same session, this indicates token issuance from different locations.
- `source_ip`, `city_name`, `country_name`, `region_name`: Review the IPs and geolocations involved. A mismatch in geographic origin within minutes can signal adversary involvement.
- `user_agent`: Conflicting user agents (e.g., `python-requests` and `Chrome`) suggest one leg of the session was scripted or automated.
- `os`: If multiple operating systems are observed in the same short session (e.g., macOS and Windows), this may suggest activity from different environments.
- `incoming_token_type`: Look for values like `"none"` or `"refreshToken"` that can indicate abnormal or re-authenticated activity.
- `token_session_status`: A value of `"unbound"` means the issued token is not tied to a device or CAE session, making it reusable from another IP.
- `conditional_access_status`: If this is `"notApplied"`, it may indicate that expected access policies were not enforced.
- `auth_count`: Number of events in the session. More than one indicates the session was reused within the time window.
- `target_time_window`: Use this to pivot into raw sign-in logs to review the exact sequence and timing of the activity.
- Search `azure.auditlogs` for any device join or registration activity around the `target_time_window`.
- Review `azure.identityprotection` logs for anonymized IPs, impossible travel, or token replay alerts.
- Search for other activity from the same IPs across all users to identify horizontal movement.

### False Positive Analysis

- A legitimate device join from a user switching networks (e.g., mobile hotspot to Wi-Fi) could explain multi-IP usage.
- Some identity management agents or EDR tools may use MAB for background device registration flows.
- Developers or IT administrators may access DRS across environments when testing.

### Response and Remediation

- If confirmed unauthorized, revoke all refresh tokens for the user and disable any suspicious registered devices.
- Notify the user and verify if the authentication or device join was expected.
- Review Conditional Access policies for the Microsoft Authentication Broker (`29d9ed98-a469-4536-ade2-f981bc1d605e`) to ensure enforcement of MFA and device trust.
- Consider restricting token-based reauthentication from anonymized infrastructure or unusual user agents.
- Continue monitoring for follow-on activity, such as privilege escalation, token misuse, or lateral movement.
