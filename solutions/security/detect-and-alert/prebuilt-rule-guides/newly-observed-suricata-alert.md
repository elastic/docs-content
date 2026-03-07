---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Newly Observed High Severity Suricata Alert" prebuilt detection rule.'
---

# Newly Observed High Severity Suricata Alert

## Triage and analysis

### Investigating Newly Observed High Severity Suricata Alert

This rule surfaces newly observed, low-frequency high severity suricata alerts within the last 5 days.

Because the alert has not been seen previously for this rule and host, it should be prioritized for validation to determine
whether it represents a true compromise or rare benign activity.

### Investigation Steps

- Identify the source address, affected host and review the associated rule name to understand the behavior that triggered the alert.
- Validate the source address under which the activity occurred and assess whether it aligns with normal behavior.
- Refer to the specific alert details like event.original to get more context.

### False Positive Considerations

- Vulnerability scanners and pentesting.
- Administrative scripts or automation tools can trigger detections when first introduced.
- Development or testing environments may produce one-off behaviors that resemble malicious techniques.

### Response and Remediation

- If the activity is confirmed malicious, isolate the affected host to prevent further execution or lateral movement.
- Terminate malicious processes and remove any dropped files or persistence mechanisms.
- Collect forensic artifacts to understand initial access and execution flow.
- Patch or remediate any vulnerabilities or misconfigurations that enabled the behavior.
- If benign, document the finding and consider tuning or exception handling to reduce future noise.
- Continue monitoring the host and environment for recurrence of the behavior or related alerts.
