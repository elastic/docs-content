---
navigation_title: Examples and common scenarios
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Common action policy scenarios, including routing by severity, managing severity escalation, and controlling re-notification."
---

# Examples and common scenarios for action policies [common-action-policy-scenarios]

:::{include} /explore-analyze/alerting/v2/_snippets/v2-system-note.md
:::

This page covers common situations you encounter when setting up action policies and explains how to configure them to get the behavior you expect.

- [Route alert episodes by severity](route-by-severity.md) describes how to direct critical and non-critical alert episodes to different workflows based on severity level.
- [Manage severity escalation notifications](severity-escalation.md) explains how action policies match and re-match alert episodes as severity shifts, and how to control which notifications fire.
- [Re-notify for persistently active alert episodes](re-notification.md) covers how to configure action policies so a workflow sends follow-up notifications when an alert episode stays active without a status change.
