---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "First-Time FortiGate Administrator Login" prebuilt detection rule.'
---

# First-Time FortiGate Administrator Login

## Triage and Analysis

### Investigating First-Time FortiGate Administrator Login

This alert indicates that a user with the **Administrator** role has successfully logged in to the FortiGate management interface for the first time within the last 5 days of observed data.

Because administrator access provides full control over network security devices, any newly observed admin login should be validated to confirm it is expected and authorized.

### Investigation Steps

- **Identify the account**
  - Review `source.user.name` and confirm whether the account is known and officially provisioned.
  - Determine whether this is a newly created administrator or an existing account logging in for the first time.

- **Validate the source**
  - Review `source.ip` and confirm whether it originates from a trusted management network, VPN, or jump host.
  - Investigate geolocation or ASN if the source IP is external or unusual.

- **Review login context**
  - Examine associated FortiGate log messages for details such as login method, interface, or authentication source.
  - Check for additional administrative actions following the login (policy changes, user creation, configuration exports).

- **Correlate with recent changes**
  - Verify whether there were recent change requests, onboarding activities, or maintenance windows that explain the login.
  - Look for other authentication attempts (failed or successful) from the same source or user.

### False Positive Considerations

- Newly onboarded administrators or service accounts.
- First-time logins after log retention changes or data source onboarding.
- Automation, backup, or monitoring tools introduced recently.
- Lab, development, or test FortiGate devices.

### Response and Remediation

- **If authorized**
  - Document the activity and consider adding an exception if the behavior is expected.
  - Ensure the account follows least-privilege and MFA best practices.

- **If suspicious or unauthorized**
  - Disable or restrict the administrator account immediately.
  - Rotate credentials and review authentication sources.
  - Audit recent FortiGate configuration changes.
  - Review surrounding network activity for lateral movement or persistence attempts.
