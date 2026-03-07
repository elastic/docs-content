---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID Excessive Account Lockouts Detected" prebuilt detection rule.
---

# Entra ID Excessive Account Lockouts Detected

## Triage and analysis

### Investigating Entra ID Excessive Account Lockouts Detected

This rule detects a high number of sign-in failures due to account lockouts (error code `50053`) in Microsoft Entra ID sign-in logs. These lockouts are typically caused by repeated authentication failures, often as a result of brute-force tactics such as password spraying, credential stuffing, or automated guessing. This detection is time-bucketed and aggregates attempts to identify bursts or coordinated campaigns targeting multiple users. Error code `50053` indicates Entra ID Smart Lockout, which is IP-based and tracks "unfamiliar" vs "familiar" locations. Familiar IPs have a higher threshold before lockout, so if lockouts are occurring, the source IP was unfamiliar to those accounts.

### Possible investigation steps

- This is a threshold rule that aggregates events, so the alert document won't contain individual sign-in attempts. Pivot to the raw logs in Discover or Timeline using: `event.dataset: "azure.signinlogs" and azure.signinlogs.properties.status.error_code: 50053`. Match the time range to the alert window (rule lookback is 30 minutes).
- Add relevant columns: `@timestamp`, `user.name`, `source.ip`, `user_agent.original`, `azure.signinlogs.properties.app_display_name`, `azure.signinlogs.properties.client_app_used`, `source.as.organization.name`, `geo.country_iso_code`, `azure.signinlogs.properties.authentication_details`.
- Aggregate by `source.ip` and `user.name` to identify the attack pattern: password spray (single/small set of IPs targeting many accounts), credential stuffing (many source IPs, may target specific users with leaked credentials), targeted brute force (focused on single high-value account), or misconfigured service (single source IP with consistent user-agent matching legitimate application).
- Analyze `user_agent.original` for indicators of automation. Values like `curl/*`, `python-requests/*`, `Go-http-client/*`, `axios/*` indicate scripted attacks. `BAV2ROPC` indicates Resource Owner Password Credential flow (legacy auth), commonly abused by spray tools like o365spray and MSOLSpray.
- Review `azure.signinlogs.properties.client_app_used`. `Other clients` indicates legacy auth (IMAP, SMTP, POP) which is high-risk. `Exchange ActiveSync` is legacy auth often targeted.
- Check `azure.signinlogs.properties.authentication_protocol` for `ropc` (Resource Owner Password Credential), a legacy flow where credentials are sent directly with no MFA interruption possible.
- Review `source.as.organization.name`. Cloud hosting providers (DigitalOcean, Vultr, Linode, AWS, Azure, GCP) or VPN providers (NordVPN, ExpressVPN, Mullvad) are high-risk as attackers use this infrastructure.
- Check `azure.signinlogs.properties.conditional_access_status`. `notApplied` means no CA policy evaluated, indicating a coverage gap. `failure` means CA policy blocked the sign-in.
- Determine if any accounts were compromised. Query for successful sign-ins from attacking infrastructure: `event.dataset: "azure.signinlogs" and event.outcome: "success" and source.ip: "<attacker_ip>"`. Also query for successful sign-ins for affected users from any source during the attack window.
- Check for MFA bypass: `event.dataset: "azure.signinlogs" and event.outcome: "success" and azure.signinlogs.properties.authentication_requirement: "singleFactorAuthentication" and source.ip: "<attacker_ip>"`
- Review Entra ID Protection risk events for affected users by checking `risk_level_during_signin`, `risk_level_aggregated`, and `risk_state` for values other than `none`.
- Check for username enumeration preceding the spray. Error code `50034` (user not found) indicates enumeration: `event.dataset: "azure.signinlogs" and azure.signinlogs.properties.status.error_code: 50034 and source.ip: "<attacker_ip>"`
- Query for other error codes from the same source: `50126` (invalid password), `50034` (user not found), `50057` (account disabled), `50055` (password expired), `53003` (blocked by CA), `50158` (MFA challenge not satisfied). A mix of `50126` and `50053` confirms password guessing.

### False positive analysis

- Misconfigured clients, scripts, or services with outdated credentials may inadvertently cause lockouts.
- Lockouts during credential rotation windows could be benign.
- Legacy applications without modern auth support may repeatedly fail and trigger Smart Lockout.
- Specific known user agents from corporate service accounts.
- Cloud-hosted automation with expected failure behavior.
- This rule can be customized. Adjust the threshold and/or interval/lookback window based on baselining efforts. Specific UPNs can be excluded if they generate known false positives.

### Response and remediation

- Confirm no successful authentications from attacking source.
- Query for successful sign-ins to affected users from any source during the attack window.
- If compromise confirmed: disable account, revoke refresh tokens (`Revoke-AzureADUserAllRefreshToken` or via portal), reset password, require MFA re-registration.
- Block source IP/ASN via Conditional Access named locations.
- If legacy auth was used: create CA policy blocking legacy authentication.
- If MFA wasn't required: review CA policy coverage for gaps.
- Document affected users for credential reset and monitoring.

