---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Newly Observed High Severity Detection Alert" prebuilt detection rule.'
---

# Newly Observed High Severity Detection Alert

## Triage and analysis

### Investigating Newly Observed High Severity Detection Alert

This rule surfaces newly observed, low-frequency behavior high severity alerts affecting a single agent within the current day.

Because the alert has not been seen previously for this rule and host, it should be prioritized for validation to determine
whether it represents a true compromise or rare benign activity.

### Investigation Steps

- Identify the affected host, user and review the associated rule name to understand the behavior that triggered the alert.
- Validate the user context under which the activity occurred and assess whether it aligns with normal behavior for that account.
- Refer to the specific rule investiguation guide for further actions.

### False Positive Considerations

- Newly deployed or updated software may introduce behavior not previously observed on the host.
- Administrative scripts or automation tools can trigger behavior-based detections when first introduced.
- Security tooling, IT management agents, or EDR integrations may generate new behavior alerts during updates or configuration changes.
- Development or testing environments may produce one-off behaviors that resemble malicious techniques.

### Response and Remediation

- If the activity is confirmed malicious, isolate the affected host to prevent further execution or lateral movement.
- Terminate malicious processes and remove any dropped files or persistence mechanisms.
- Collect forensic artifacts to understand initial access and execution flow.
- Patch or remediate any vulnerabilities or misconfigurations that enabled the behavior.
- If benign, document the finding and consider tuning or exception handling to reduce future noise.
- Continue monitoring the host and environment for recurrence of the behavior or related alerts.
