---
navigation_title: Set up
applies_to:
  stack: ga 9.6+
  serverless:
    observability: ga
products:
  - id: kibana
  - id: cloud-serverless
description: "License, connector, data, and space requirements, plus how to turn on optional features or opt out of the system."
---

# Set up {{alerting-v2-system}} [setup]

{{alerting-v2-system}} is on by default. Check that you have what you need to create rules, then turn on any optional features you want.

:::{note}
If you tried {{alerting-v2-system-short}} while it was experimental in {{stack}} 9.5, upgrade to 9.6 or later. The system changed a lot before it became generally available, and these docs cover only the generally available version.
:::

## Before you begin [alerting-setup-requirements]

- **An {{observability}} project, if you use {{serverless-short}}**: {{alerting-v2-system-short}} isn't available in {{es-serverless}}, {{sec-serverless}}, or {{vectordb}} projects.
- **Data to query**: Rules can only find conditions in data that's already in {{es}}. [Ingest your data](/manage-data/ingest.md) before you create rules.
- **A space to work in**: Rules, [action policies](action-policies/about-action-policies.md), and the privileges that control them belong to a single space. [Create or switch spaces](/deploy-manage/manage-spaces.md) if you need to.
- **A connector, if you want notifications**: [Workflows](workflows-alerting.md) send notifications through [connectors](/deploy-manage/manage-connectors.md), such as Slack, email, or PagerDuty.
- **An Enterprise license, if you want notifications on {{stack}}**: Compare subscriptions for [{{ecloud}}](https://www.elastic.co/subscriptions/cloud) and [self-managed](https://www.elastic.co/subscriptions) deployments.

## Adjust {{alerting-v2-system-short}} settings [alerting-setup-settings]

Three advanced settings change how {{alerting-v2-system-short}} works. A space setting applies only to the space where you change it. A global setting applies to every space.

| Setting | Scope | Default | Use it to |
|---|---|---|---|
| **Universal Alerting: Experimental Features** (`alerting:v2:experimentalFeatures`) | Space | Off | [Try experimental features](#alerting-setup-experimental-features) |
| **Classic Alerting: Show Classic Alerts table** (`alerting:v1:showV1ObservabilityAlertsTable`) | Space | Off | [Keep the {{observability}} Alerts page](#alerting-setup-v1-alerts-page) |
| **Universal Alerting** (`alerting:v2:enabled`) | Global | On | [Opt out of {{alerting-v2-system-short}}](#alerting-setup-turn-off) |

### Try experimental features in a space [alerting-setup-experimental-features]

```yaml {applies_to}
serverless:
  observability: experimental
stack: experimental 9.6+
```

Experimental features are new {{alerting-v2-system-short}} capabilities that are still in development. They can change or be removed in a future release, so avoid relying on them in production.

When the setting is on, you can chain rules into a sequence and detect multi-step alert patterns. On the **Rules** page, select **Build a sequence**.

To turn them on:

1. Switch to the space where you want the features.
2. Go to the **Advanced Settings** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. On the **Space Settings** tab, turn on **Universal Alerting: Experimental Features**.
4. Select **Save changes**, then reload {{kib}}.

You can create rules and action policies with {{agent-builder}} while this setting is off.

- On the **Rules** page, select **Create rule** → **Create with agent**. When the Rules list is empty, select **With AI Agent**.
- On the **Action Policies** page, select **Create policy** → **Create with agent**. When the Action Policies list is empty, select **Create with AI Agent**.

{{agent-builder}} has [its own requirements](rules/create-rules-action-policies-agent-builder.md#create-ai-agent-requirements).

### Keep the {{observability}} Alerts page for {{alerting-v1-system}} [alerting-setup-v1-alerts-page]

With {{alerting-v2-system-short}} on, a new **Alerts** page that shows alerts from both systems replaces the {{observability}} **Alerts** page, which shows only {{alerting-v1-system-short}} alerts. You can find the new page in the **Alerting** menu. To keep the old page as well, turn on the **Classic Alerting: Show Classic Alerts table** setting. The old page then appears as **Alerts (Classic)** in the **Alerting** menu.

To show the **Alerts (Classic)** page:

1. Switch to the space where you want the page.
2. Go to the **Advanced Settings** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. On the **Space Settings** tab, turn on **Classic Alerting: Show Classic Alerts table**.
4. Select **Save changes**, then reload {{kib}}.

### Opt out of {{alerting-v2-system-short}} [alerting-setup-turn-off]

To turn off {{alerting-v2-system-short}} in every space:

1. Go to the **Advanced Settings** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Global Settings** tab, turn off [**Universal Alerting**](kibana://reference/advanced-settings.md#alerting-v2-enabled).
3. Select **Save changes**, then reload {{kib}}.

This hides the UI and turns off the APIs. Your rules, action policies, and alert history stay in place, and the setting stays off after upgrades.

Rules and action policies keep running after you turn off the setting. To stop them:

- On {{serverless-short}}, [contact Elastic support](/troubleshoot/index.md#contact-us).
- On {{stack}}, set [`xpack.alerting_v2.enabled`](kibana://reference/configuration-reference/alerting-settings.md) to `false` in `kibana.yml`, then restart {{kib}}.

## Next steps [alerting-setup-next-steps]

[Create your first rule](get-started/create-your-first-rule.md) to try {{alerting-v2-system-short}} with sample data.
