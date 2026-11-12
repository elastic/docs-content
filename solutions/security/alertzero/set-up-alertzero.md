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

To use {{alertzero}} in an {{elastic-sec}} space, turn it on, select the models the {{az-workers}} use, and start the {{az-workers}}. {{alertzero}} is off by default, so repeat this setup in each space.

:::{note}
To use {{alertzero}}, you need a subscription that includes it. For the features in each subscription tier, refer to the subscription pages for [{{ecloud}}]({{subscriptions}}/cloud) and [{{stack}} and self-managed deployments]({{subscriptions}}).
:::

## Before you begin [alertzero-set-up-before]

### Required for all {{az-workers}} [alertzero-set-up-before-all]

Before you start the {{az-workers}}, make sure you have all the following:

- A role with the [privileges to set up {{alertzero}}](alertzero-privileges.md#alertzero-admin-access).
- An AI model in the space, either an [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) or an [external {{infer}} endpoint](/explore-analyze/elastic-inference/external.md) for a third-party model provider. If your subscription includes Elastic Managed LLMs, they're available by default. To change which models the {{az-workers}} use, refer to [Select models for the {{az-workers}}](#alertzero-choose-models).
- Events and alerts in {{elastic-sec}} for the {{az-workers}} to analyze. If you don't have them yet, [ingest data](/solutions/security/get-started/ingest-data-to-elastic-security.md) into {{elastic-sec}}, then [turn on detections](/solutions/security/detect-and-alert/turn-on-detections.md) and [install and enable prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) so that your data generates alerts.

### Required for specific {{az-workers}} [alertzero-set-up-before-workers]

Check what each {{az-worker}} you plan to run needs:

| {{az-worker}} | Analyzes | Requirements |
| --- | --- | --- |
| [{{az-alert-triage}}](watches-and-workers.md#alertzero-alert-triage) | Detection alerts waiting for triage | [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) turned on |
| [{{az-attack-discovery}}](watches-and-workers.md#alertzero-attack-discovery) | Detection alerts | **Attack Discovery Workflows** [advanced setting](kibana://reference/advanced-settings.md#kibana-siem-settings) turned on, and [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) to hand off attacks |
| [{{az-continuous-threat-hunt}}](watches-and-workers.md#alertzero-continuous-threat-hunt) | Events in the default [{{elastic-sec}} indices](kibana://reference/advanced-settings.md#kibana-siem-settings), such as `logs-*` | {{context-engine}}, and [what {{alertzero}} needs to build {{az-threat-reports}}](threat-reports.md#alertzero-threat-reports-requirements) |
| [{{az-rule-tuning}}](watches-and-workers.md#alertzero-rule-tuning) | Alerts marked as false positives | None |
| [{{az-rule-coverage}}](watches-and-workers.md#alertzero-rule-coverage) | Detection gaps from {{az-continuous-threat-hunt}} | {{az-continuous-threat-hunt}} and {{context-engine}} |
| [{{az-endpoint-analysis}}](watches-and-workers.md#alertzero-endpoint-analysis) | Attacks handed off by {{az-attack-discovery}} | {{az-attack-discovery}}, {{elastic-defend}}, and {{context-engine}} |

## Turn on {{alertzero}} for a space [alertzero-turn-on]

In the space where you want {{alertzero}}, open **Advanced Settings**, turn on the **{{alertzero}}** setting (`securitySolution:enableAlertZero`), save your changes, and reload {{kib}}. {{alertzero}} then appears in the {{elastic-sec}} navigation menu. For the setting's details, refer to the [advanced settings reference](kibana://reference/advanced-settings.md#securitysolution-enablealertzero).

## Select models for the {{az-workers}} [alertzero-choose-models]

The {{az-workers}} match each model call to a model tier based on what the call needs. Each tier has its own list of models in the **{{alertzero}}** section of [Feature Settings](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings):

- **{{az-efficient-models}}**: Quick, lightweight calls that run often, such as checking detection coverage.
- **{{az-balanced-models}}**: Calls where accuracy matters, but that run often or use tools over many steps, such as triaging alerts or diagnosing a noisy rule.
- **{{az-frontier-models}}**: Complex work where output quality matters most, such as generating attack discoveries or drafting a detection rule.

% For docs writers: When Elastic publishes model evaluations for AlertZero, link them here so readers can compare models for each tier. Don't list the default models for each tier, because they change with the product defaults.

Each tier starts with its own preset models instead of your default model, and the {{az-workers}} use the first available model in the tier's list. To use a different model for a tier, add it to the tier's list in the **{{alertzero}}** section of **Feature Settings**, and move it to the top or remove the models listed before it. Do this before you [start the {{az-workers}}](#alertzero-turn-on-workers), because their first run starts right away.

To run every {{az-worker}} on your default model instead, turn off **Feature specific models**.

### Run {{az-workers}} on {{openai-daybreak}} models [alertzero-daybreak-models]

The optional **{{az-cyber-domain-models}}** tier is for {{openai-daybreak}} models, which are designed for cybersecurity tasks. You don't need to apply to OpenAI's Trusted Access for Cyber program to use them in {{alertzero}}.

{{daybreak}} models are available only through the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), and [standard EIS pricing](/explore-analyze/elastic-inference/eis.md#pricing) applies. The tier stays empty until the models are available on EIS. OpenAI restricts their use to {{alertzero}}, so they don't appear in other model lists, and you can't chat with them directly.

% For docs writers: When Daybreak models become available on EIS, remove "The tier stays empty until the models are available on EIS."

:::{note}
A {{daybreak}} model in the **{{az-cyber-domain-models}}** tier replaces the other tiers for the {{az-alert-triage}}, {{az-attack-discovery}}, and {{az-continuous-threat-hunt}} {{az-workers}}. The one exception is {{esql}} queries. {{az-continuous-threat-hunt}} can't use a {{daybreak}} model to write them, so it keeps using **{{az-frontier-models}}** for those queries.
:::

% For the AlertZero product team, open question: Product guidance says that choosing cyber domain models means the other AlertZero model settings don't apply. In the Kibana source, a Daybreak model replaces the tiers only for Alert Triage, Attack Discovery, and Continuous Threat Hunt, and Hunt keeps Frontier models for ES|QL queries. Rule Coverage, Rule Tuning, and Endpoint Analysis keep their usual tiers. Does "one or the other" mean something else, or is the preceding note accurate?

## Start the {{az-workers}} [alertzero-turn-on-workers]

Open **{{alertzero}}** in the navigation menu to start onboarding. Every {{az-worker}} starts out on, so turn off any that you don't plan to run. At least one {{az-worker}} must stay on. If a {{az-worker}} needs a setting that's off, such as {{context-engine}}, onboarding lets you turn it on, and it links to setup for dependencies such as {{elastic-defend}}.

When you finish onboarding, the {{az-workers}} start their first run right away, and {{alertzero}} opens the **{{az-proposed-actions-cap}}** page. When a {{az-worker}} needs your decision, its {{az-proposed-action}} appears there.

To change which {{az-workers}} run after setup, refer to [Turn a {{az-worker}} on or off](configure-worker-settings.md#configure-worker-settings-enabled). To change the default {{az-worker}} settings, refer to [](configure-worker-settings.md).

## Next steps [alertzero-set-up-next]

- [Give your team access to {{alertzero}}](alertzero-privileges.md) so they can review and decide {{az-proposed-actions}}.
- [Find the {{az-proposed-actions}} that need your decision](work-in-alertzero.md).
- [Change {{az-worker}} settings](configure-worker-settings.md), such as {{az-autonomy}} and schedule.
