---
navigation_title: Tags and runbooks (Alert mode only)
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Add tags and runbooks to Alert-mode rules in Kibana's experimental alerting system for filtering and investigation context."
---

# Tags and runbooks in the {{alerting-v2-system}} (Alert mode only) [experimental-alerting-system-tags-investigation]

Tags and runbooks are optional artifacts for Alert-mode rules in the {{alerting-v2-system}}.

- **Tags**: Free-form labels for filtering and organization. Maximum 20 tags per rule. Each tag can be up to 128 characters.
- **Runbooks**: An investigation guide stored with the rule so responders have context when alerts are generated.

## When to configure tags and runbooks [tags-when-to-use]

Configure tags when:

* You want to filter the Alerts UI by team, environment, or severity tier without writing ad hoc KQL queries each time.
* You are using action policies and want to match episodes by ownership or category rather than by rule name. Tags are inherited by alert episodes, so any tag you add to a rule is available as a KQL matcher in action policies.
* You manage many rules and need a consistent labeling scheme to track which team owns which alerts.

Configure a runbook when:

* Responders who aren't familiar with the service might need to triage the alert. A runbook surfaces triage steps directly alongside the alert without requiring a separate search.
* The alert requires a consistent response process that you want encoded and version-controlled alongside the rule.

Skip tags and runbooks when:

* The rule is in Signal mode. Tags and runbooks are Alert-mode-only artifacts and have no effect on signal document output.
* The rule is experimental or not yet part of a monitored production system.

## Examples

### Tag a rule for team ownership and severity

Tags let you filter alerts by team, environment, or severity tier. For a checkout service rule, you might add tags like:

- `team:payments`
- `env:production`
- `sev:p1`

On-call engineers can then narrow the alerts view to rules their team owns without scanning every active episode.

### Add a runbook with triage steps

A runbook gives responders immediate context when an alert fires. Write it as plain text in the rule's description field. Include enough detail that an engineer unfamiliar with the service can triage without asking for help.

```
Fires when checkout error rate exceeds 10% for 3 consecutive evaluations.

Triage steps:
1. Check the checkout service deployment history in the last 30 minutes.
2. Review the error breakdown dashboard: https://kibana.example.com/dashboards/checkout-errors
3. If errors are concentrated in one region, escalate to the infra team.
4. If errors are global, page the payments on-call lead.
```
