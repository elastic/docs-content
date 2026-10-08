---
navigation_title: Examples and common scenarios
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Common action policy scenarios, including routing by severity, managing severity escalation, and controlling re-notification."
---

# Examples and common scenarios for action policies [common-action-policy-scenarios]

This page covers common situations you encounter when setting up action policies in {{alerting-v2-system}} and explains how to configure them to get the behavior you expect.

- [Route alerts by severity](route-by-severity.md) describes how to direct critical and non-critical alerts to different workflows based on severity level.
- [Manage severity escalation notifications](severity-escalation.md) explains how action policies match and re-match alerts as severity shifts, and how to control which notifications fire.
- [Re-notify for persistently active alerts](re-notification.md) covers how to configure action policies so a workflow sends follow-up notifications when an alert stays active without a status change.
