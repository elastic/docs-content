---
navigation_title: Requirements
description: "The settings, privileges, and dependencies AlertZero needs before you set it up."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} requirements [alertzero-requirements]

Check that these are in place before you [set up {{alertzero}}](set-up-alertzero.md).

## Subscription [alertzero-requirements-subscription]

- {applies_to}`serverless: ` The Security Complete [feature tier](https://www.elastic.co/pricing/serverless-security)
- {applies_to}`stack: ` An active Enterprise [subscription](https://www.elastic.co/subscriptions)

## Space [alertzero-requirements-space]

```{applies_to}
stack: preview 9.6
```

{{alertzero}} works only in spaces that use the **Security** solution view. In a space with any other solution view, including **Classic**, {{alertzero}} shows **AlertZero is not available in this space**. To set a space's solution view, refer to [Create a space](/deploy-manage/manage-spaces.md#spaces-managing).

## Advanced setting [alertzero-requirements-setting]

Turn on the **{{alertzero}}** advanced setting (`securitySolution:enableAlertZero`) in each space where you want {{alertzero}}. It's off by default. For the steps, refer to [Turn on {{alertzero}} for a space](set-up-alertzero.md#alertzero-turn-on). For the setting's details, refer to the [advanced settings reference](kibana://reference/advanced-settings.md#securitysolution-enablealertzero).

## AI model [alertzero-requirements-ai-model]

{{az-workers}} need an AI model to run. The space needs at least one model that {{alertzero}} can use, such as an [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) or an LLM connector, and you can't turn on {{az-workers}} until one is available. To connect a model, refer to [Connect to an LLM](/solutions/security/ai/set-up-ai-features.md#set-up-ai-llm).

To select which models {{alertzero}} uses for each type of call, go to **Feature Settings** and set the models under **{{alertzero}}**: **{{az-efficient-models}}**, **{{az-balanced-models}}**, **{{az-frontier-models}}**, and, optionally, **{{az-cyber-domain-models}}**. Refer to [Feature settings](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings).

## Privileges [alertzero-requirements-privileges]

To set up {{alertzero}}, you need these privileges:

| To | You need |
| --- | --- |
| Turn on the {{alertzero}} setting | The **Advanced Settings** privilege set to **All** |
| Get past the first onboarding step | The **{{alertzero}}** privilege set to **All** |
| Turn {{az-workers}} on or off | The **{{alertzero}}** privilege set to **All**<br>The `manage_security` cluster privilege<br>The **Workflows** sub-feature privileges **Update** and **Update managed workflows** |

Granting **All** for **Workflows** doesn't include **Update managed workflows**, so assign it explicitly.

The `manage_security` privilege also lets a user manage users and roles for the whole cluster. Have an admin who already has it set up {{alertzero}}, instead of granting it only for {{alertzero}}.

For the privileges people need to use {{alertzero}}, such as viewing the home page and deciding {{az-proposed-actions}}, refer to [{{alertzero}} privileges](alertzero-privileges.md).

## Data and detections [alertzero-requirements-data]

{{az-workers}} work on the data, alerts, and rules already in the space:

- Security data: Add the data sources you want {{az-workers}} to analyze. Refer to [](/solutions/security/get-started/ingest-data-to-elastic-security.md).
- Detection alerts and rules: The {{az-alert-triage}} and {{az-attack-discovery}} {{az-workers}} work on the alerts your detection rules create, and the {{az-detection-watch}} works on the rules themselves. Refer to [](/solutions/security/detect-and-alert/turn-on-detections.md).
- {{elastic-defend}} data: The {{az-endpoint-analysis}} {{az-worker}} needs {{elastic-defend}} data from the hosts it analyzes. Refer to [](/solutions/security/configure-elastic-defend/install-elastic-defend.md).

## {{az-worker}} dependencies [alertzero-requirements-dependencies]

Some {{az-workers}} work only on what another {{az-worker}} produces. Keep both on, or the dependent {{az-worker}} has nothing to work on.

| {{az-worker}} | Needs | Why |
| --- | --- | --- |
| {{az-rule-coverage}} | {{az-continuous-threat-hunt}} | It works on the detection gaps that {{az-continuous-threat-hunt}} finds. |
| {{az-endpoint-analysis}} | {{az-attack-discovery}} | It analyzes only the attacks that {{az-attack-discovery}} hands off. |
| {{az-attack-discovery}} | {{az-endpoint-analysis}} | It hands off attacks it can't rule out as false positives. Without {{az-endpoint-analysis}}, those attacks aren't analyzed, and their {{az-investigations}} stay open. |

If you turn off a {{az-worker}} that another one needs, {{alertzero}} asks you to confirm and shows a warning on both. It never turns a {{az-worker}} on or off for you.

Turning on {{az-continuous-threat-hunt}} also turns on the [{{az-threat-intel-supply}}](glossary.md#alertzero-glossary-threat-intel-supply) workflows that feed it {{az-threat-reports}}, and turning it off turns them off.
