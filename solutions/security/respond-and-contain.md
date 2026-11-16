---
navigation_title: Respond and contain
description: Triage the detection alerts that Elastic Security generates, then isolate hosts and take other response actions on threats you confirm.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Respond and contain

When your detection rules find a threat, triage the alert, then act on the affected host to stop the threat from spreading. You can isolate a host, stop a process, collect a file for analysis, and take other actions without leaving {{elastic-sec}}.

To investigate an alert before you act, such as to find its root cause or its scope, refer to [Investigate](/solutions/security/investigate.md). To review alerts that AI has grouped into attacks, refer to [Attack Discovery](/solutions/security/ai/attack-discovery/index.md).

## How triage and response actions work together

You usually move from an alert to a response action in a few steps:

1. **Triage the alert**: On the **Alerts** page, filter alerts to focus on what matters, and change each alert's status as you work through it.
2. **Act on the host**: From the alert details flyout, select **Take action** → **Respond** to open the response console for the host that generated the alert. Enter commands in the console to isolate the host, stop processes, get files, and more.
3. **Check the results**: The response actions history records every action and its output, so you can confirm that an action completed.

## Where to start

| Your goal | Start here |
|---|---|
| View, filter, and change the status of detection alerts | [Manage detection alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md) |
| Run response actions on an endpoint from the response console | [Endpoint response actions](/solutions/security/endpoint-response-actions.md) |
| Block a host from communicating with your network | [Isolate a host](/solutions/security/endpoint-response-actions/isolate-host.md) |
| Run response actions automatically when a rule generates an alert | [Automated response actions](/solutions/security/endpoint-response-actions/automated-response-actions.md) |
| Respond on hosts that CrowdStrike, Microsoft Defender for Endpoint, or SentinelOne manage | [Configure third-party response actions](/solutions/security/endpoint-response-actions/configure-third-party-response-actions.md) → [Third-party response actions](/solutions/security/endpoint-response-actions/third-party-response-actions.md) |
| Review past response actions and their results | [Response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md) |

## Next steps

After you contain a threat, you can:

- Track the incident and coordinate with your team in [cases](/solutions/security/investigate/security-cases.md).
- [Add host isolation exceptions](/solutions/security/manage-elastic-defend/host-isolation-exceptions.md) for IP addresses that isolated hosts still need to reach.
- [Reduce noise and false positives](/solutions/security/detect-and-alert/reduce-noise-and-false-positives.md) by tuning the rules that generated the alerts.
