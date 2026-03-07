---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Multiple Rare Elastic Defend Behavior Rules by Host" prebuilt detection rule.
---

# Multiple Rare Elastic Defend Behavior Rules by Host

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Multiple Rare Elastic Defend Behavior Rules by Host

This rule correlates Elastic Defend behavior alerts by host and applies a global prevalence filter: only behavior rules that fire on a single host in the lookback window are considered. Hosts that trigger two or more such rare behavior rules are flagged, as this pattern is more likely to indicate real compromise than commonly seen behavior rules.

### Possible investigation steps

- Review the listed behavior rule names and the associated process command lines (and parent command lines) to understand what actions triggered the alerts.
- Identify the user(s) associated with the activity and confirm whether the behavior is expected for that role or host.
- Correlate with other endpoint and network data for the host (process, network, file events) to assess scope and persistence.
- Compare timestamps of the alerts to determine if activity is part of a single campaign or staged execution.

### False positive analysis

- The global prevalence filter (rules seen on only one host) reduces noise from behavior rules that fire widely (e.g., common software or policy). If legitimate single-host tools or scripts trigger multiple rare behavior rules, consider documenting and excluding known-good rule names or hosts.
- Development or testing hosts may exhibit multiple rare behaviors; consider lowering severity or excluding those hosts if appropriate.

### Response and remediation

- Isolate the host if triage indicates compromise, then follow standard incident response procedures.
- Collect and preserve artifacts (process hashes, command lines, files) for further analysis.
- Escalate to the security team for full investigation and potential containment or eradication actions.

