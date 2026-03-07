---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "FortiGate Administrator Login from Multiple IP Addresses" prebuilt detection rule.'
---

# FortiGate Administrator Login from Multiple IP Addresses

## ## Triage and Analysis

### Investigating FortiGate Administrator Login from Multiple IP Addresses

This alert indicates that the same **Administrator** account successfully logged in to the FortiGate management interface from **multiple distinct source IP addresses** within an 24-hour period.

Because FortiGate administrator credentials grant full control over network security infrastructure, this behavior may indicate credential compromise, account sharing, or misuse of administrative access.

### Investigation Steps

- **Review the affected account**
  - Identify the administrator account in `source.user.name`.
  - Confirm whether the account is shared, personal, or service-related.
  - Validate whether concurrent or near-concurrent access is expected.

- **Analyze source IP addresses**
  - Review the list of `source.ip` values associated with the logins.
  - Determine whether the IPs belong to trusted management networks, VPN pools, or jump hosts.
  - Investigate geolocation differences using `source.geo.country_name`.

- **Assess timing and session behavior**
  - Check whether logins occurred close together in time or overlapped.
  - Identify whether access patterns suggest session hopping or credential reuse.

- **Review post-authentication activity**
  - Examine FortiGate logs for configuration changes, policy updates, or administrative actions following the logins.
  - Look for additional authentication attempts (successful or failed) from the same IPs or user.

- **Correlate with environment context**
  - Verify maintenance windows, incident response activity, or operational tasks that could explain the behavior.
  - Confirm whether administrators commonly access FortiGate via multiple networks or devices.

### False Positive Considerations

- Administrators connecting through VPNs with dynamic or rotating IP addresses.
- Access via bastion hosts, load-balanced management interfaces, or cloud-based management tools.
- Automation or orchestration systems using shared administrator credentials.
- Incident response or troubleshooting activity involving multiple access points.

### Response and Remediation

- **If the activity is expected**
  - Document the behavior and consider tuning the rule or adding exceptions for known IP ranges or accounts.
  - Encourage use of named accounts and centralized access paths.

- **If the activity is suspicious**
  - Reset or rotate credentials for the affected administrator account.
  - Review FortiGate configuration changes made during the session(s).
  - Restrict administrative access to trusted IP ranges.
  - Enforce MFA for administrative logins if not already enabled.
  - Monitor for additional signs of lateral movement or persistence.
