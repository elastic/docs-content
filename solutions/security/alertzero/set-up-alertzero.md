---
description: "Check what AlertZero needs in Elastic Security, turn it on in a space, select which Workers to run, and fix messages that block Workers from turning on."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Set up {{alertzero}} [alertzero-set-up]

{{alertzero}} is off by default, and you set it up separately in each space. Check what it needs, turn on its advanced setting, then select which {{az-workers}} to run. {{alertzero}} requires the Security Analytics Complete [feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#elastic-sec-project-features) in {{serverless-short}} or an Enterprise [subscription](https://www.elastic.co/subscriptions) on {{stack}}.

## Before you begin [alertzero-set-up-before]

Complete these in each space where you want to use {{alertzero}}. Without the privileges and an AI model, you can't turn on {{az-workers}}.

- **Privileges:** Setting up {{alertzero}} needs privileges that most roles don't include, so you might need an administrator to do it. Refer to [](alertzero-privileges.md).
- **AI model:** The space needs at least one AI model that {{alertzero}} can use, such as an [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) or an [External Inference](/explore-analyze/elastic-inference/external.md) model. To connect one, refer to [Connect to an LLM](/solutions/security/ai/set-up-ai-features.md#set-up-ai-llm). Choosing a model for each kind of task is optional, and you can do it later in the **{{alertzero}}** section of **Feature Settings**, under **{{az-efficient-models}}**, **{{az-balanced-models}}**, **{{az-frontier-models}}**, and **{{az-cyber-domain-models}}**. Refer to [Feature settings](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings).
- **Security data:** {{az-workers}} analyze the security data you ingest. If the space has no data yet, add it first, or the {{az-workers}} have nothing to analyze. Refer to [](/solutions/security/get-started/ingest-data-to-elastic-security.md).
- {applies_to}`stack: preview 9.6` **Security solution view:** {{alertzero}} works only in spaces that use the **Security** solution view. In any other view, including **Classic**, the message "{{alertzero}} is not available in this space" appears instead. Refer to [Create a space](/deploy-manage/manage-spaces.md#spaces-managing).

For the {{az-workers}} you plan to turn on, also check [what specific {{az-workers}} need](#alertzero-requirements-specific-workers). You can also do this later, when a {{az-watch}} page warns you.

## Turn on {{alertzero}} for a space [alertzero-turn-on]

1. In the space where you want {{alertzero}}, find **Advanced Settings** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Security Solution** section, turn on the **{{alertzero}}** setting (`securitySolution:enableAlertZero`).
3. Select **Save changes**, then select **Reload page**.

% For the setting's details, refer to the [advanced settings reference](kibana://reference/advanced-settings.md#securitysolution-enablealertzero).

**{{alertzero}}**, **{{az-escalations-cap}}**, and **{{az-watches}}** appear in the {{elastic-sec}} navigation menu.

## Turn on {{az-workers}} [alertzero-turn-on-workers]

The first time you open {{alertzero}} in a space, it walks you through turning on {{az-workers}}.

1. In the navigation menu, select **{{alertzero}}**.
2. On the **Let's add your data?** step, select **Continue**. To connect more data sources first, select **Open Getting started**.

   If you can't select **Continue**, you don't have the privileges to set up {{alertzero}}. Refer to [](alertzero-privileges.md).

3. On the **Let's turn on the {{az-watches}}?** step, turn off any [{{az-workers}}](configure-worker-settings.md) you don't want to run yet. Keep at least one on.

   Every {{az-worker}} is on by default. Some {{az-workers}} need others, so before you turn one off, check [which {{az-workers}} need other {{az-workers}}](#alertzero-requirements-dependencies).

4. Select **Enable and run**.

{{alertzero}} turns on the {{az-workers}} you kept, creates a service account for each one, and opens the **{{az-proposed-actions-cap}}** page.

Scheduled {{az-workers}} start their first run immediately, and the page shows "{{az-workers}} are running in the background" until the first {{az-proposed-actions}} arrive. The {{az-endpoint-analysis}} {{az-worker}} waits until the {{az-attack-discovery}} {{az-worker}} hands it an attack.

## What specific {{az-workers}} need [alertzero-requirements-specific-workers]

Some {{az-workers}} need more than every space does. Complete only the parts for the {{az-workers}} you turn on, and skip the rest. If one of them is missing something, its {{az-watch}} page shows a warning.

### Settings that are off by default [alertzero-requirements-worker-settings]

Turn on these settings in each space where the {{az-workers}} run:

| {{az-worker}} | Turn on |
| --- | --- |
| {{az-alert-triage}} | The [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) |
| {{az-attack-discovery}} | Attack Discovery workflows (`securitySolution:enableAttackDiscoveryWorkflows`) and [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) (`contextEngine:enabled`) |
| {{az-continuous-threat-hunt}}, {{az-rule-coverage}}, and {{az-endpoint-analysis}} | [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) (`contextEngine:enabled`) |

The {{az-workers}} that need {{context-engine}} use it to pass detection gaps and forensics handoffs to each other. Refer to [](configure-worker-settings.md).

### Data that specific {{az-workers}} need [alertzero-requirements-data]

- **Detection alerts and rules:** The {{az-alert-triage}} and {{az-attack-discovery}} {{az-workers}} analyze the alerts your detection rules create, and the {{az-detection-watch}} improves the rules themselves. Refer to [](/solutions/security/detect-and-alert/turn-on-detections.md).
- **{{elastic-defend}} data:** The {{az-endpoint-analysis}} {{az-worker}} needs {{elastic-defend}} data from the hosts it analyzes. Refer to [](/solutions/security/configure-elastic-defend/install-elastic-defend.md).

### {{az-workers}} that need other {{az-workers}} [alertzero-requirements-dependencies]

Some {{az-workers}} work on what another {{az-worker}} produces. For each {{az-worker}} you turn on in the first column, turn on the {{az-worker}} it needs too.

| {{az-worker}} | Needs | Why |
| --- | --- | --- |
| {{az-rule-coverage}} | {{az-continuous-threat-hunt}} | It works on the detection gaps that {{az-continuous-threat-hunt}} finds. |
| {{az-endpoint-analysis}} | {{az-attack-discovery}} | It analyzes only the attacks that {{az-attack-discovery}} hands off. |
| {{az-attack-discovery}} | {{az-endpoint-analysis}} | It hands off attacks it can't rule out as false positives. If {{az-endpoint-analysis}} is off, those attacks stay unanalyzed, and their {{az-investigations}} stay open. |

To turn {{az-workers}} on or off after setup, refer to [](configure-worker-settings.md).

% After elastic/docs-content#9118 merges, link the Configure Watches and Workers references in this section to configure-worker-settings.md#alertzero-context-engine and configure-worker-settings.md#alertzero-worker-on-off.

## If you can't turn on {{az-workers}} [alertzero-set-up-blocked]

If something blocks {{az-workers}} from turning on, the onboarding page shows one of these messages:

| Message | What to do |
| --- | --- |
| "AI models aren't set up for this space" | Make an AI model available in the space, such as an Elastic Managed LLM, then return to {{alertzero}}. To assign models, select **Open Feature settings**. Refer to [](#alertzero-set-up-before). |
| "You need the manage_security cluster privilege to enable {{az-workers}}" | Ask an administrator who has the [privileges to set up {{alertzero}}](alertzero-privileges.md) to turn on the {{az-workers}}. |
| "Some {{az-workers}} weren't turned on" | {{alertzero}} couldn't create service accounts for the {{az-workers}} that the message lists. To retry, select **Enable and run** again. |

## Next steps [alertzero-set-up-next]

- [](alertzero-privileges.md): Give each person the privileges they need to use {{alertzero}}.
- [](manage-alertzero.md): Change how {{az-workers}} run, or turn {{alertzero}} off in a space.
