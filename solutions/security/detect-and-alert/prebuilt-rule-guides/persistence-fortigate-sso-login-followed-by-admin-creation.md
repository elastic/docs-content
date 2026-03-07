---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "FortiGate SSO Login Followed by Administrator Account Creation" prebuilt detection rule.'
---

# FortiGate SSO Login Followed by Administrator Account Creation

## Triage and analysis

### Investigating FortiGate SSO Login Followed by Administrator Account Creation

This alert indicates that a FortiCloud SSO login was followed by an administrator account creation event on the same FortiGate device within 15 minutes. This two-event sequence is the core attack pattern observed in the FG-IR-26-060 campaign.

The attack flow is: authenticate via FortiCloud SSO using a crafted SAML assertion, then immediately create local administrator accounts to maintain access even after the SSO vulnerability is patched.

### Possible investigation steps

- Review the SSO login event for the FortiCloud account used and the source IP. Determine whether the SSO account belongs to the organization.
- Check the admin creation event for the names of accounts created and the access profiles assigned (especially super_admin).
- Assess the timing between events. In the observed campaign, admin creation occurs within seconds of SSO login. A tight time correlation is a strong indicator of compromise.
- Review `observer.name` to identify the targeted device and verify whether FortiCloud SSO is intentionally enabled. Run `get system admin` to list all current administrator accounts.
- Check whether the same SSO account or source IP targeted other devices. Look for configuration exports, firewall policy changes, or VPN modifications following the admin creation.

### False positive analysis

- An authorized administrator logging in via FortiCloud SSO and creating a new admin account as part of normal operations.
- Initial device onboarding where SSO login and account setup occur in the same session.

### Response and remediation

- If unauthorized, delete all administrator accounts created during the session and disable FortiCloud SSO immediately.
- Restore configuration from a known-clean backup and rotate all credentials including LDAP/AD accounts connected to the device.
- Upgrade FortiOS to a patched version and engage incident response for the affected device and any downstream systems.
- If the activity is expected, document the administrative session and verify it was authorized. Consider creating accounts through a separate session to avoid triggering this correlation.
