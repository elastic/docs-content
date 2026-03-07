---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "FortiGate SSL VPN Login Followed by SIEM Alert by User" prebuilt detection rule.
---

# FortiGate SSL VPN Login Followed by SIEM Alert by User

## Triage and analysis

### Investigating FortiGate SSL VPN Login Followed by SIEM Alert by User

This rule correlates a FortiGate SSL VPN login with a subsequent security alert for the same user name, highlighting possible abuse of VPN access or activity shortly after remote access.

### Possible investigation steps

- Review the FortiGate login event (source IP, user, time) and the SIEM alert(s) that followed for the same user.
- Determine whether the user is expected to use VPN and whether the subsequent alert is related to legitimate work (e.g. admin tools, updates).
- Check for other alerts or logins for the same user in the same time window to assess scope.
- Correlate with authentication logs to identify impossible travel or credential reuse from the VPN session.

### False positive analysis

- Legitimate VPN users triggering detections (e.g. scripted tasks, admin tooling) after login.
- Security scans or automated jobs that run in the context of a VPN-authenticated user.

### Response and remediation

- If abuse or compromise is suspected, disable or reset the user’s VPN access and credentials.
- Investigate the host and process associated with the SIEM alert.
- Escalate to the security or incident response team if the alert indicates malicious activity.

