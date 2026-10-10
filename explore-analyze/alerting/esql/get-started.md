---
navigation_title: Get started
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: "Learn what happens after a rule runs, look up key terms, and follow a hands-on tutorial to create a rule and observe the alert lifecycle."
---

# Get started [get-started]

:::{include} /explore-analyze/alerting/esql/_snippets/v2-system-note.md
:::

- [How it works](get-started/how-it-works.md): Walk through what happens after a rule runs, including how a rule's configuration determines whether matches open an alert or remain available for later analysis.
- [Glossary](get-started/glossary.md): Look up key terms, such as alert, action policy, and rule event.
- [Create your first rule](get-started/create-your-first-rule.md): Load sample data, create a rule, and watch an alert move from breach through automatic recovery.

Before you start the tutorial, [set up {{alerting-v2-system}}](setup.md) and [configure access](manage/configure-access.md) for your role.

## Explore the documentation [explore-documentation]

- [Rules](rules.md): Define what to detect in {{esql}}, and select the creation path that fits your use case.
- [Alerts](alerts.md): Learn how alerts track a problem from first detection through recovery, and how to triage them.
- [Notifications and actions](notifications-actions.md): Set up action policies that invoke workflows to notify your team.
