---
description: "Set up AlertZero in an Elastic Security space: check what each Worker needs, turn on AlertZero, select models, and start the Workers."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Set up {{alertzero}} [alertzero-set-up]

This page shows you how to set up {{alertzero}} in an {{elastic-sec}} space. After you confirm that you have what the {{az-workers}} need, turn on {{alertzero}}, choose the models the {{az-workers}} use, and start the {{az-workers}} you want to run.

{{alertzero}} is turned off by default. You must turn it on and set it up in each space where you want to use it.

:::{note}
To use {{alertzero}}, you need a subscription that includes it. For the features in each subscription tier, refer to the subscription pages for [{{ecloud}}]({{subscriptions}}/cloud) and [{{stack}} and self-managed deployments]({{subscriptions}}).
:::

## Before you begin [alertzero-set-up-before]

To run any {{az-worker}}, you need the right privileges, an AI model, and security data for the {{az-workers}} to analyze. Some {{az-workers}} also need extra setup.

### Required for all {{az-workers}} [alertzero-set-up-before-all]

Before you start the {{az-workers}}, make sure you have all the following:

- A role with the following [AlertZero privileges](alertzero-privileges.md#alertzero-admin-access):

  - The **All** privilege for **Advanced Settings**, which you need to [turn on {{alertzero}}](#alertzero-turn-on) in the space.
  - The **All** privilege for **{{alertzero}}**, which you need to start onboarding and turn on the {{az-workers}}.
  - The **Update** and **Update managed workflows** sub-feature privileges for **Workflows**, which let you turn on each {{az-worker}}. Each {{az-worker}} runs as a [managed workflow](/explore-analyze/workflows/managed-workflows.md).
  - The `manage_security` cluster privilege, which {{alertzero}} uses to create a [service account](alertzero-privileges.md#alertzero-worker-privileges) for each {{az-worker}}. It also lets anyone who has it manage users and roles for the whole cluster, so don't add it to a role only for {{alertzero}}. If you don't have it, ask an administrator who does to start the {{az-workers}}.
- An AI model in the space, either an [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) or an LLM connector. If your subscription includes Elastic Managed LLMs, they're available by default. Otherwise, refer to [Connect to an LLM](/solutions/security/ai/set-up-ai-features.md#set-up-ai-llm). To change which models the {{az-workers}} use, refer to [Select models for the {{az-workers}}](#alertzero-choose-models).
- Events and alerts in {{elastic-sec}} for the {{az-workers}} to analyze. Without both, the {{az-workers}} have nothing to triage, correlate, or hunt through. If you don't have them yet, [ingest data](/solutions/security/get-started/ingest-data-to-elastic-security.md) into {{elastic-sec}}, then [turn on detections](/solutions/security/detect-and-alert/turn-on-detections.md) and [install and enable prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) so that your data generates alerts.

### Required for specific {{az-workers}} [alertzero-set-up-before-workers]

Each {{az-worker}} analyzes different data, and some need extra setup, such as [{{context-engine}}](/explore-analyze/ai-features/context-engine.md). Check what each {{az-worker}} you plan to run needs:

| {{az-worker}} | Analyzes | Requirements |
| --- | --- | --- |
| [{{az-alert-triage}}](watches-and-workers.md#alertzero-triage-watch) | Detection alerts waiting for triage | [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) turned on |
| [{{az-attack-discovery}}](watches-and-workers.md#alertzero-triage-watch) | Detection alerts | **Attack Discovery Workflows** [advanced setting](kibana://reference/advanced-settings.md#kibana-siem-settings) turned on, and {{context-engine}} to hand off attacks |
| [{{az-continuous-threat-hunt}}](watches-and-workers.md#alertzero-hunt-watch) | Events in the default [{{elastic-sec}} indices](kibana://reference/advanced-settings.md#kibana-siem-settings), such as `logs-*` | {{context-engine}}, outbound HTTPS access to the [threat feeds](watches-and-workers.md#alertzero-hunt-watch), [models](#alertzero-choose-models) in the default space, and a [default embedding endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) |
| [{{az-rule-tuning}}](watches-and-workers.md#alertzero-detection-watch) | Alerts marked as false positives | None |
| [{{az-rule-coverage}}](watches-and-workers.md#alertzero-detection-watch) | Detection gaps from {{az-continuous-threat-hunt}} | {{az-continuous-threat-hunt}} and {{context-engine}} |
| [{{az-endpoint-analysis}}](watches-and-workers.md#alertzero-forensics-watch) | Attacks handed off by {{az-attack-discovery}} | {{az-attack-discovery}}, {{elastic-defend}}, and {{context-engine}} |

% For docs writers: After elastic/docs-content#9144 merges, link each Worker to its own anchor in watches-and-workers.md: alertzero-alert-triage, alertzero-attack-discovery, alertzero-continuous-threat-hunt, alertzero-rule-tuning, alertzero-rule-coverage, and alertzero-endpoint-analysis. In the Continuous Threat Hunt row, keep Context Engine, and replace the threat feeds, models, and embedding endpoint requirements with a link to watches-and-workers.md#alertzero-threat-reports-requirements, which owns those details.

## Turn on {{alertzero}} for a space [alertzero-turn-on]

1. In the space where you want {{alertzero}}, find **Advanced Settings** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Security Solution** section, turn on the **{{alertzero}}** setting (`securitySolution:enableAlertZero`).
3. Select **Save changes**, then select **Reload page**.

% For docs writers: After elastic/kibana#302289 adds this setting to the advanced settings reference, uncomment the following sentence.
% For the setting's details, refer to the [advanced settings reference](kibana://reference/advanced-settings.md#securitysolution-enablealertzero).

**{{alertzero}}**, **{{az-escalations-cap}}**, and **{{az-watches}}** appear in the {{elastic-sec}} navigation menu.

## Select models for the {{az-workers}} [alertzero-choose-models]

The {{az-workers}} match each model call to a model tier based on what the call needs. This lets you save on calls that run often and keep quality where it matters most. Each tier has its own list of models in the **{{alertzero}}** section of [Feature Settings](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings):

- **{{az-efficient-models}}**: Quick, lightweight calls that run often, such as checking detection coverage.
- **{{az-balanced-models}}**: Calls where accuracy matters, but that run often or use tools over many steps, such as triaging alerts or diagnosing a noisy rule.
- **{{az-frontier-models}}**: Complex work where output quality matters most, such as generating attack discoveries or drafting a detection rule.

    :::{important}
    By default, Claude Opus 5 is first in the **{{az-frontier-models}}** list, so the {{az-workers}} use it whenever it's available. For a better balance of quality and cost, we recommend moving another model, such as GPT-5.6 Sol, to the top of the list.
    :::

Each tier starts with recommended models instead of your default model, and the {{az-workers}} use the first available model in the tier's list. To use a different model for a tier, change it before you [start the {{az-workers}}](#alertzero-turn-on-workers), because their first run starts right away:

1. Go to **Feature Settings** in the main menu, or find it using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **{{alertzero}}** section, find the tier you want to change.
3. Select **Add a model**, then select the model you want.
4. Drag the model to the top of the tier's list, or remove the models above it.
5. Select **Save settings**.

To run every {{az-worker}} on your default model instead, turn off **Feature specific models**.

### Run {{az-workers}} on OpenAI Daybreak models [alertzero-daybreak-models]

The optional **{{az-cyber-domain-models}}** tier is for OpenAI Daybreak models, which are designed for cybersecurity tasks. You don't need to apply to OpenAI's Trusted Access for Cyber program to use them in {{alertzero}}.

Daybreak models are available only through the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), and [standard EIS pricing](/explore-analyze/elastic-inference/eis.md#pricing) applies. The tier stays empty until the models are available on EIS. OpenAI restricts their use, so they work only with {{alertzero}}. They don't appear in any other model list, and you can't chat with them directly.

:::{note}
A Daybreak model in the **{{az-cyber-domain-models}}** tier replaces the other tiers for the {{az-alert-triage}}, {{az-attack-discovery}}, and {{az-continuous-threat-hunt}} {{az-workers}}. The one exception is {{esql}} queries. {{az-continuous-threat-hunt}} can't use a Daybreak model to write them, so it keeps using **{{az-frontier-models}}** for those queries.
:::

% For the AlertZero product team, open question: Product guidance says that choosing cyber domain models means the other AlertZero model settings don't apply. In the Kibana source, a Daybreak model replaces the tiers only for Alert Triage, Attack Discovery, and Continuous Threat Hunt, and Hunt keeps Frontier models for ES|QL queries. Rule Coverage, Rule Tuning, and Endpoint Analysis keep their usual tiers. Does "one or the other" mean something else, or is the preceding note accurate?

## Start the {{az-workers}} [alertzero-turn-on-workers]

1. In the navigation menu, select **{{alertzero}}**. The first time you open it in a space, onboarding starts.
2. Follow the onboarding steps. All {{az-workers}} start out selected, so turn off any that you don't plan to run. At least one {{az-worker}} must stay selected. Onboarding flags any {{az-worker}} that's missing something it needs, such as {{context-engine}}.
3. Select **Enable and run**.

The {{az-workers}} start their first run right away, and {{alertzero}} opens the **{{az-proposed-actions-cap}}** page. When a {{az-worker}} needs your decision, its {{az-proposed-action}} appears there.

To change which {{az-workers}} run after setup, refer to [](configure-worker-settings.md).

% For docs writers: After elastic/docs-content#9144 merges, link configure-worker-settings.md#configure-worker-settings-enabled.

## Next steps [alertzero-set-up-next]

- [](alertzero-privileges.md): Give your team the privileges they need to view and decide {{az-proposed-actions}}.
- [](use-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
- [](configure-worker-settings.md): Change {{az-worker}} settings, such as {{az-autonomy}} and schedule.
