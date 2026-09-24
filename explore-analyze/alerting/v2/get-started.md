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

:::{include} /explore-analyze/alerting/v2/_snippets/v2-system-note.md
:::

Use the following pages to learn how the system works, look up the terms used throughout its documentation, and create your first rule.

- [How it works](get-started/how-it-works.md): Walk through what happens after a rule runs, including how a rule's configuration determines whether matches open an alert episode or remain available for later analysis.
- [Glossary](get-started/glossary.md): Look up definitions of key terms used throughout the {{alerting-v2-system}} documentation, such as alert episode, action policy, and rule event.
- [Create your first rule](get-started/create-your-first-rule.md): A hands-on tutorial that walks you through loading sample data, creating a rule, and observing the alert lifecycle from breach through automatic recovery.

Before you start the tutorial, [set up the {{alerting-v2-system}}](setup.md) and [configure access](manage/configure-access.md) for your role.

## Explore the documentation [explore-documentation]

Once you're comfortable with the basics, use the following pages as your entry points into the rest of the {{alerting-v2-system}} docs. They contain deeper explanations of core concepts, configuration guidance, and reference material for rules, alerts, and notifications.

- [Rules](rules.md) shows you how to define what to detect in {{esql}}, and how to choose and configure the right creation path for your use case.
- [Alerts](alerts.md) explains how alert episodes track a problem from first detection through recovery, and how to triage them as they come in.
- [Notifications and actions](notifications-actions.md) shows you how action policies invoke workflows so the right people hear about the right problems, at the right time.
