---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Newly Observed Elastic Defend Behavior Alert" prebuilt detection rule.'
---

# Newly Observed Elastic Defend Behavior Alert

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Newly Observed Elastic Defend Behavior Alert

Elastic Defend behavior alerts indicate suspicious activity observed on an endpoint that may not yet be widespread or repeated.
This rule surfaces newly observed, low-frequency behavior alerts affecting a single agent within the current day, which can
represent early-stage malware execution, initial persistence attempts, or hands-on-keyboard activity.

Because the alert has not been seen previously for this rule and host, it should be prioritized for validation to determine
whether it represents a true compromise or rare benign activity.

### Investigation Steps

- Identify the affected host and review the associated Elastic Defend rule name to understand the behavior that triggered the alert.
- Review the process details, including executable path, parent process, command line, and SHA-256 hash.
- Determine whether the process is expected on the host by validating its origin, signer, and execution context.
- Examine the alert timeline to confirm that all activity occurred within a short time window and assess whether behavior escalated.
- Correlate with additional endpoint telemetry such as:
  - Process creation and termination
  - File modifications
  - Network connections
  - Registry or persistence-related activity
- Check whether the process hash, command line, or related indicators are known malicious or associated with recent campaigns.
- Validate the user context under which the activity occurred and assess whether it aligns with normal behavior for that account.

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
