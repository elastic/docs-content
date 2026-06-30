---
navigation_title: Tags and runbooks (Alert mode only)
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Add tags and runbooks to Alert-mode rules in Kibana's experimental alerting system for filtering and investigation context."
---

# Tags and runbooks in the {{alerting-v2-system}} (Alert mode only) [tags-investigation]

Tags and runbooks are optional metadata fields for Alert-mode rules in the {{alerting-v2-system}}.

- **Tags**: Free-form labels for filtering and organization. Maximum 20 tags per rule; each tag can be up to 128 characters.
- **Runbooks**: An investigation guide stored with the rule so responders have context when alerts are generated.

## Examples

### Tag a rule for team ownership and severity

Tags let you filter alerts by team, environment, or severity tier. For a checkout service rule, you might add tags like:

- `team:payments`
- `env:production`
- `sev:p1`

On-call engineers can then narrow the alerts view to rules their team owns without scanning every active episode.

### Add a runbook with triage steps

A runbook gives responders immediate context when an alert fires. Write it as plain text in the rule's description field. Include enough detail that an engineer unfamiliar with the service can triage without asking for help:

```
Fires when checkout error rate exceeds 10% for 3 consecutive evaluations.

Triage steps:
1. Check the checkout service deployment history in the last 30 minutes.
2. Review the error breakdown dashboard: https://kibana.example.com/dashboards/checkout-errors
3. If errors are concentrated in one region, escalate to the infra team.
4. If errors are global, page the payments on-call lead.
```
