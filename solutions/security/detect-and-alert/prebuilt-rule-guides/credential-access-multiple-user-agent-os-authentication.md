---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Okta Multiple OS Names Detected for a Single DT Hash" prebuilt detection rule.
---

# Okta Multiple OS Names Detected for a Single DT Hash

## Triage and analysis

### Investigating Okta Multiple OS Names Detected for a Single DT Hash

This rule detects when a single Okta device token hash (dt_hash) is associated with multiple operating system types. This is highly anomalous because a device token is tied to a specific device and its operating system. This alert strongly indicates that an attacker has stolen a device token token and is using it to impersonate a legitimate user from a different machine.

### Possible investigation steps
- Review the `okta.debug_context.debug_data.dt_hash` field to identify the specific device
trust hash associated with multiple operating systems.
- Examine the `user.email` field to determine which user account is associated with the suspicious activity
- Analyze the `source.ip` field to identify the IP addresses from which the different operating systems were reported. Look for any unusual or unexpected locations.
- Review the `user_agent.os.name` field to see the different operating systems reported for the
same dt_hash. This will help identify the nature of the anomaly.
- Check the `event.action` field to understand the context of the authentication events (e.g., MFA verification, standard authentication).
- Investigate the timeline of events to see when the different operating systems were reported for the same dt_hash. Look for patterns or sequences that may indicate malicious activity.
- Correlate this activity with other security events in your environment, such as failed login attempts, unusual access patterns, or alerts from endpoint security solutions.

### False positive analysis
- Applications will tag the operating system as null when the device is not recognized as a managed device
- In environments where users frequently switch between managed and unmanaged devices, this may lead to false positives.

### Response and remediation
- Immediately investigate the user account associated with the suspicious activity to determine if it has been compromised.
- If compromise is confirmed, reset the user's credentials and enforce multi-factor authentication (MFA)
- Revoke any active sessions associated with the compromised account to prevent further unauthorized access.
- Review and monitor the affected dt_hash for any further suspicious activity.
- Educate users about the importance of device security and the risks associated with device tokens.
- Implement additional monitoring for device token tokens and consider using conditional access policies to restrict access based on device compliance status.

