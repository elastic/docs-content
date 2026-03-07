---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Sign-In Console Login with Federated User" prebuilt detection rule.
---

# AWS Sign-In Console Login with Federated User

## Triage and analysis

### Investigating AWS Sign-In Console Login with Federated User

Federated users in AWS are granted temporary credentials to access resources, often without the need for a permanent account. This setup is convenient but can be risky if not properly secured with multi-factor authentication (MFA). Adversaries might exploit this by using stolen or misconfigured credentials to gain unauthorized access. CloudTrail alone cannot reliably indicate MFA usage for federated logins. This rule surfaces potentially risky access for analyst review and IdP correlation.

### Possible investigation steps

- **Identify the prinicipal involved**
  - `aws.cloudtrail.user_identity.arn` (federated session ARN)
  - `aws.cloudtrail.user_identity.session_context.session_issuer.*` (role ARN/name, account) of the identity that created the federated session.
  - Find the corresponding IdP login around the same time and verify MFA was required and passed. If IdP shows **no MFA**, raise severity.

- **Investigate the source context**
  - examine `source.ip`, ASN, `geo` fields, and `user_agent.original`
  - Compare against normal IP ranges, known user-agents and expected locations for this identity

- **Federation token pivot:** Look for a nearby `signin.amazonaws.com` `GetSigninToken` API call.
  - **More suspicious:** token creation and console login from different public IPs/ASNs/geo fields.
  - **Less suspicious:** same IP and expected user agents within ~10–15 minutes (typical operator behavior).

- **Rareness/anomaly signals:** new/rare role or session issuer, rare source IP/ASN/geo, unusual time-of-day, multiple ConsoleLogin events from disparate networks in a short window.

- Review recent activity associated with the federated user to identify any unusual or unauthorized actions that may have occurred following the login event.

- Assess the configuration and policies of the Identity Provider (IdP) used for federated access to ensure MFA is enforced and properly configured for all users.


### False positive analysis
- Organizations using SSO for console access will routinely see federated `ConsoleLogin` where CloudTrail shows `MFAUsed: "No"` — this is expected due to IdP-side MFA.
- Internal tools/automation that create federation links (`GetSigninToken`) for operators.
- Maintain allow-lists for corp/VPN CIDRs, approved ASNs, and known automation user-agents.

### Response and remediation
- If IdP confirms MFA and the source context is expected: document and close.
- If IdP shows no MFA or context is suspicious:
  - Notify the security team and relevant stakeholders about the potential security breach to ensure coordinated response efforts.
  - Disable/lock the IdP account pending review; invalidate IdP sessions if supported.
  - Temporarily restrict access (e.g., SCPs, session policies, IP-based conditions).
  - Conduct a thorough review of AWS CloudTrail logs to identify any suspicious activities or unauthorized access attempts associated with both the intitiating user and the federated user account.
  - Hunt for a preceding `GetSigninToken` from a different IP/ASN/UA (possible token relay).
  - Ensure IdP policy enforces MFA for AWS app access; re-verify role trust and least-privilege policies.
- Implement or enforce multi-factor authentication (MFA) for all federated user accounts to enhance security and prevent similar incidents in the future.
- Review and update IAM policies and roles associated with federated users to ensure they follow the principle of least privilege.

