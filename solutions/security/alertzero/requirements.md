---
navigation_title: Requirements
description: "Check the subscription, space, advanced setting, AI model, privileges, and data that AlertZero needs before you set it up in Elastic Security."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} requirements [alertzero-requirements]

Before you [set up {{alertzero}}](set-up-alertzero.md), check that your deployment meets the following requirements. Without an AI model or the setup privileges, you can't turn on {{az-workers}}.

## Subscription [alertzero-requirements-subscription]

- {applies_to}`serverless: preview` The Security Analytics Complete [feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#elastic-sec-project-features)
- {applies_to}`stack: preview 9.6` An active Enterprise [subscription](https://www.elastic.co/subscriptions)

## Space [alertzero-requirements-space]
```{applies_to}
serverless: unavailable
```

{{alertzero}} works only in spaces that use the **Security** solution view. In a space with any other solution view, including the **Classic** view, {{alertzero}} shows **{{alertzero}} is not available in this space**. To set a space's solution view, refer to [Create a space](/deploy-manage/manage-spaces.md#spaces-managing).

## Advanced setting [alertzero-requirements-setting]

{{alertzero}} is off by default. You turn it on in each space with the {{alertzero}} advanced setting (`securitySolution:enableAlertZero`). For the steps, refer to [Turn on {{alertzero}} for a space](set-up-alertzero.md#alertzero-turn-on). For the setting's details, refer to the [advanced settings reference](kibana://reference/advanced-settings.md#securitysolution-enablealertzero).

## AI model [alertzero-requirements-ai-model]

{{az-workers}} need an AI model to run. The space needs at least one model that {{alertzero}} can use, such as an [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) or an [External Inference](/explore-analyze/elastic-inference/external.md) model. You can't turn on {{az-workers}} until a model is available. To connect a model, refer to [Connect to an LLM](/solutions/security/ai/set-up-ai-features.md#set-up-ai-llm).

Optionally, you can select which models {{alertzero}} uses for each kind of task. Find **Feature Settings** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then set the models under **{{alertzero}}**: **{{az-efficient-models}}**, **{{az-balanced-models}}**, **{{az-frontier-models}}**, and **{{az-cyber-domain-models}}**. Refer to [Feature settings](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings).

## Privileges [alertzero-requirements-privileges]

To set up {{alertzero}}, you need these privileges:

| To | You need |
| --- | --- |
| Turn on the {{alertzero}} advanced setting | The **Advanced Settings** privilege set to **All** |
| Select **Continue** on the first onboarding step | The **{{alertzero}}** privilege set to **All** |
| Turn {{az-workers}} on or off | The **{{alertzero}}** privilege set to **All**<br>The `manage_security` cluster privilege<br>The **Workflows** sub-feature privileges **Update** and **Update managed workflows** |
| Set models in **Feature Settings** | The privileges listed in [Manage access to AI features](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#requirements) |

Granting **All** for **Workflows** doesn't include **Update managed workflows**, so assign it explicitly.

The `manage_security` privilege also lets a user manage users and roles for the whole cluster. Instead of granting it only for {{alertzero}}, ask an admin who already has it to set up {{alertzero}}.

For the privileges people need to use {{alertzero}}, such as viewing the home page and approving or declining {{az-proposed-actions}}, refer to [](alertzero-privileges.md).

## Data and detections [alertzero-requirements-data]

{{alertzero}} analyzes the data, alerts, and rules already in your deployment:

- **Security data:** {{az-workers}} analyze the security data you ingest. Refer to [](/solutions/security/get-started/ingest-data-to-elastic-security.md).
- **Detection alerts and rules:** The {{az-alert-triage}} and {{az-attack-discovery}} {{az-workers}} analyze the alerts your detection rules create, and the {{az-detection-watch}} improves the rules themselves. Refer to [](/solutions/security/detect-and-alert/turn-on-detections.md).
- **{{elastic-defend}} data:** The {{az-endpoint-analysis}} {{az-worker}} needs {{elastic-defend}} data from the hosts it analyzes. Refer to [](/solutions/security/configure-elastic-defend/install-elastic-defend.md).

## {{az-worker}} dependencies [alertzero-requirements-dependencies]

Some {{az-workers}} depend on what another {{az-worker}} produces. If you turn off a {{az-worker}} that another one needs, the dependent {{az-worker}} loses some or all of its work.

| {{az-worker}} | Needs | Why |
| --- | --- | --- |
| {{az-rule-coverage}} | {{az-continuous-threat-hunt}} | It works on the detection gaps that {{az-continuous-threat-hunt}} finds. |
| {{az-endpoint-analysis}} | {{az-attack-discovery}} | It analyzes only the attacks that {{az-attack-discovery}} hands off. |
| {{az-attack-discovery}} | {{az-endpoint-analysis}} | It hands off attacks it can't rule out as false positives. If {{az-endpoint-analysis}} is off, those attacks stay unanalyzed, and their {{az-investigations}} stay open. |

{{alertzero}} asks you to confirm before you turn off a {{az-worker}} that another one needs, and shows a warning on both. It never turns {{az-workers}} on or off for you.

When you turn on {{az-continuous-threat-hunt}}, {{alertzero}} also turns on the [{{az-threat-intel-supply}}](glossary.md#alertzero-glossary-threat-intel-supply) workflows that provide its {{az-threat-reports}}. Turning off {{az-continuous-threat-hunt}} turns those workflows off.
