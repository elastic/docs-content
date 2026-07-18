---
navigation_title: Get started
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Get started with the experimental alerting system in Kibana: review requirements, enable the system, configure role access, and follow a tutorial to create a rule and observe the alert lifecycle."
---

# Get started with the {{alerting-v2-system}} [get-started]

Use the following guides to get the {{alerting-v2-system}} running in your space, set up role access for your team, and create your first rule.

- [Set up the {{alerting-v2-system}}](get-started/setup.md): Review requirements, enable the `alerting:v2:enabled` advanced setting, and confirm the system is accessible in your space.
- [Configure access](get-started/configure-access.md): Set up a role with the {{kib}} feature privileges needed to create rules, triage alerts, and query alert data.
- [Create your first rule](get-started/create-your-first-rule.md): A hands-on tutorial that walks you through loading sample data, creating a rule, and observing the alert lifecycle from breach through automatic recovery.

## Explore the documentation [explore-documentation]

Once you're comfortable with the basics, use the following pages as your entry points into the rest of the {{alerting-v2-system}} docs. They contain deeper explanations of core concepts, configuration guidance, and reference material for rules, alerts, and notifications.

- [Rules](rules.md) shows you how to define what to detect in {{esql}}, and how to choose and configure the right creation path for your use case.
- [Alerts](alerts.md) explains how alert episodes track a problem from first detection through recovery, and how to triage them as they come in.
- [Notifications and actions](notifications-actions.md) shows you how to connect workflows and action policies so the right people hear about the right problems, at the right time.

:::{important} - How to use the {{alerting-v2-system}} docs
The docs for the {{alerting-v2-system}} don't always name a specific button or menu. When that's the case, look for the closest matching label in the {{kib}} UI. Even if the in-application wording differs slightly, the concepts and behaviors described in the docs still apply.
:::
