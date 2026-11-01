---
description: "Turn on AlertZero in an Elastic Security space, then use onboarding to start its Workers."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Set up {{alertzero}} [alertzero-set-up]

{{alertzero}} is off by default, and you set it up separately in each space. First turn on its advanced setting, then let onboarding guide you through starting the {{az-workers}}.

## Turn on {{alertzero}} for a space [alertzero-turn-on]

1. In the space where you want {{alertzero}}, find **Advanced Settings** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Security Solution** section, turn on the **{{alertzero}}** setting (`securitySolution:enableAlertZero`).
3. Select **Save changes**, then select **Reload page**.

% For the setting's details, refer to the [advanced settings reference](kibana://reference/advanced-settings.md#securitysolution-enablealertzero).

**{{alertzero}}**, **{{az-escalations-cap}}**, and **{{az-watches}}** appear in the {{elastic-sec}} navigation menu.

## Decide which {{az-workers}} to run [alertzero-decide-workers]

In onboarding, every {{az-worker}} starts out selected, and at least one has to stay selected. Some {{az-workers}} build on each other's results, so check what depends on a {{az-worker}} before you turn it off. For example, the {{az-endpoint-analysis}} {{az-worker}} investigates only the attacks that the {{az-attack-discovery}} {{az-worker}} hands off, so if you turn off {{az-attack-discovery}}, {{az-endpoint-analysis}} has nothing to analyze.

To decide which {{az-workers}} fit your environment and check what each one needs, refer to [](configure-worker-settings.md). You can enable {{az-workers}} or turn them off later on their {{az-watch}} pages.

## Start the {{az-workers}} [alertzero-turn-on-workers]

{{az-workers}} need security data to analyze and at least one AI model to run. Onboarding links to where to add data, and you can't start the {{az-workers}} until the space has a model. To prepare ahead, refer to [](/solutions/security/get-started/ingest-data-to-elastic-security.md) and [Connect to an LLM](/solutions/security/ai/set-up-ai-features.md#set-up-ai-llm).

Some {{az-workers}} also need [{{context-engine}}](/explore-analyze/ai-features/context-engine.md), which they use to pass work to each other. Without it, the {{az-rule-coverage}} and {{az-endpoint-analysis}} {{az-workers}} can't do their work, and the {{az-attack-discovery}} and {{az-continuous-threat-hunt}} {{az-workers}} run but don't pass work on. Onboarding flags each {{az-worker}} that's missing it.

The first time you open {{alertzero}} in a space, onboarding walks you through starting the {{az-workers}}. To open it, select **{{alertzero}}** in the navigation menu. Follow the steps, turn off any {{az-workers}} you decided not to run, then select **Enable and run**.

:::{note}
**Enable and run** turns on the {{az-workers}} you selected, so it needs **All** for **{{alertzero}}**, the `manage_security` cluster privilege, and the **Workflows** sub-feature privileges **Update** and **Update managed workflows**. For details, refer to [](alertzero-privileges.md).
:::

% After elastic/docs-content#9115 merges, link the privileges reference in the note to alertzero-privileges.md#alertzero-privileges-configure.

After you select **Enable and run**, {{alertzero}} opens its home page, the **{{az-proposed-actions-cap}}** page. Scheduled {{az-workers}} start their first run immediately, and their {{az-proposed-actions}} appear there when they need your decision.

## Next steps [alertzero-set-up-next]

- [](alertzero-privileges.md): Give your team the privileges they need to view and decide {{az-proposed-actions}}.
- [](use-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
- [](configure-worker-settings.md): Change how often {{az-workers}} run and how much {{az-autonomy}} each one has.
