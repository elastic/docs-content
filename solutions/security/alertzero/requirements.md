---
navigation_title: Requirements
description: "Check the subscription, space, advanced setting, AI model, privileges, and data that AlertZero needs before you set it up in Elastic Security."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} requirements [alertzero-requirements]

Before you [set up {{alertzero}}](set-up-alertzero.md), check that your deployment meets these requirements. Without an AI model or the setup privileges, you can't turn on {{az-workers}}.

## Subscription [alertzero-requirements-subscription]

- {applies_to}`serverless: preview` The Security Analytics Complete [feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#elastic-sec-project-features)
- {applies_to}`stack: preview 9.6` An active Enterprise [subscription](https://www.elastic.co/subscriptions)

## Security solution view [alertzero-requirements-space]
```{applies_to}
serverless: unavailable
```

{{alertzero}} works only in spaces that use the **Security** solution view. In any other view, including **Classic**, {{alertzero}} shows **{{alertzero}} is not available in this space**. To set a space's solution view, refer to [Create a space](/deploy-manage/manage-spaces.md#spaces-managing).

## Advanced setting [alertzero-requirements-setting]

{{alertzero}} is off by default. Turn it on in each space with the {{alertzero}} advanced setting (`securitySolution:enableAlertZero`). Refer to [Turn on {{alertzero}} for a space](set-up-alertzero.md#alertzero-turn-on).

% For the setting's details, refer to the [advanced settings reference](kibana://reference/advanced-settings.md#securitysolution-enablealertzero).

## AI model [alertzero-requirements-ai-model]

The space needs at least one AI model that {{alertzero}} can use, such as an [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) or an [External Inference](/explore-analyze/elastic-inference/external.md) model. You can't turn on {{az-workers}} until a model is available. To connect a model, refer to [Connect to an LLM](/solutions/security/ai/set-up-ai-features.md#set-up-ai-llm).

Optionally, select which model {{alertzero}} uses for each kind of task. Find **Feature Settings** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). In the **{{alertzero}}** section, set **{{az-efficient-models}}**, **{{az-balanced-models}}**, **{{az-frontier-models}}**, and **{{az-cyber-domain-models}}**. Refer to [Feature settings](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings).

## Privileges [alertzero-requirements-privileges]

To set up {{alertzero}}, you need the **Advanced Settings** and **{{alertzero}}** privileges set to **All**, the `manage_security` cluster privilege, and the **Workflows** sub-feature privileges **Update** and **Update managed workflows**. For every {{alertzero}} task and the privileges it needs, refer to [](alertzero-privileges.md).

## Settings that {{az-workers}} need [alertzero-requirements-worker-settings]

Some {{az-workers}} need settings that are off by default. Turn them on in each space where those {{az-workers}} run:

| {{az-worker}} | Turn on |
| --- | --- |
| {{az-alert-triage}} | The [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) |
| {{az-attack-discovery}} | Attack Discovery workflows (`securitySolution:enableAttackDiscoveryWorkflows`) and [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) (`contextEngine:enabled`) |
| {{az-continuous-threat-hunt}}, {{az-rule-coverage}}, and {{az-endpoint-analysis}} | [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) (`contextEngine:enabled`) |

If a setting that a {{az-worker}} needs is off, the {{az-worker}}'s {{az-watch}} page shows a warning.

## Data and detections [alertzero-requirements-data]

{{alertzero}} analyzes the data, alerts, and rules already in your deployment:

- **Security data:** {{az-workers}} analyze the security data you ingest. Refer to [](/solutions/security/get-started/ingest-data-to-elastic-security.md).
- **Detection alerts and rules:** The {{az-alert-triage}} and {{az-attack-discovery}} {{az-workers}} analyze the alerts your detection rules create, and the {{az-detection-watch}} improves the rules themselves. Refer to [](/solutions/security/detect-and-alert/turn-on-detections.md).
- **{{elastic-defend}} data:** The {{az-endpoint-analysis}} {{az-worker}} needs {{elastic-defend}} data from the hosts it analyzes. Refer to [](/solutions/security/configure-elastic-defend/install-elastic-defend.md).

## {{az-worker}} dependencies [alertzero-requirements-dependencies]

Some {{az-workers}} rely on what another {{az-worker}} produces. Before you turn off a {{az-worker}}, check whether another one needs it.

| {{az-worker}} | Needs | Why |
| --- | --- | --- |
| {{az-rule-coverage}} | {{az-continuous-threat-hunt}} | It works on the detection gaps that {{az-continuous-threat-hunt}} finds. |
| {{az-endpoint-analysis}} | {{az-attack-discovery}} | It analyzes only the attacks that {{az-attack-discovery}} hands off. |
| {{az-attack-discovery}} | {{az-endpoint-analysis}} | It hands off attacks it can't rule out as false positives. If {{az-endpoint-analysis}} is off, those attacks stay unanalyzed, and their {{az-investigations}} stay open. |

When you turn off a {{az-worker}} that another one needs, {{alertzero}} asks you to confirm first and shows a warning on both {{az-workers}}. It never turns {{az-workers}} on or off for you.

When you turn on {{az-continuous-threat-hunt}}, {{alertzero}} also turns on the [{{az-threat-intel-supply}}](glossary.md#alertzero-glossary-threat-intel-supply) workflows that provide its {{az-threat-reports}}. Turning off {{az-continuous-threat-hunt}} turns those workflows off.
