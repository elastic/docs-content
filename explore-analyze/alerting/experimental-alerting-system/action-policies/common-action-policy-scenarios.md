---
navigation_title: Examples and common scenarios
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Common action policy scenarios for the experimental alerting system, including routing by severity, managing severity escalation, and controlling re-notification."
---

# Examples and common scenarios for action policies in the {{alerting-v2-system}} [common-action-policy-scenarios]

This section covers common situations you encounter when setting up action policies in the {{alerting-v2-system}} and explains how to configure them to get the behavior you expect.

- [Route alert episodes by severity](route-by-severity.md) describes how to direct critical and non-critical episodes to different workflows based on severity level.
- [Manage severity escalation notifications](severity-escalation.md) explains how action policies match and re-match episodes as severity shifts, and how to control which notifications fire.
- [Re-notify for persistently active episodes](re-notification.md) covers how to configure action policies to send follow-up notifications when an episode stays active without a status change.
