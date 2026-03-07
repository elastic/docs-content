---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Rare Connection to WebDAV Target" prebuilt detection rule.'
---

# Rare Connection to WebDAV Target

## Triage and analysis

### Investigating Rare Connection to WebDAV Target

### Possible investigation steps

- Examine the reputation of the destination domain or IP address.
- Verify if the target user opened any attachments or clicked links pointing to the same target within seconds from the alert timestamp.
- Correlate the findings with other security logs and alerts to identify any patterns or additional indicators of compromise related to the potential relay attack.

### False positive analysis

- User accessing legit WebDAV resources.

### Response and remediation

- Conduct a password reset for the target account that may have been compromised or are at risk, ensuring the use of strong, unique passwords.
- Verify whether other users were targeted but did not open the lure..
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the full scope of the breach.
- Conduct a post-incident review to identify any gaps in security controls and update policies or procedures to prevent recurrence, ensuring lessons learned are applied to improve overall security posture.
