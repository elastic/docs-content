---
navigation_title: Manage
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: "Use role privileges to control who can create rules and triage alert episodes, and see which API keys authorize rules, action policies, and workflows."
---

# Manage [manage]

:::{include} /explore-analyze/alerting/v2/_snippets/v2-system-note.md
:::

Access works at two levels. Role privileges control what each person can do in {{kib}}, such as create rules or triage alert episodes. Stored API keys control what rules, action policies, and workflows can do when they run in the background. For example, a rule runs with the API key of the user who last saved it. That user's privileges determine what data the rule can query.

Use the following pages to set up access for your team and keep those background runs authorized.

- [Configure access](manage/configure-access.md): Set up a role with the {{kib}} feature privileges needed to create rules, triage alert episodes, and query alert episode data.
- [Authorization](manage/authorization.md): Understand which credential authorizes each rule, action policy, and workflow run, and how to diagnose and fix authorization errors.
