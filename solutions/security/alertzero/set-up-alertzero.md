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

In onboarding, every {{az-worker}} starts out selected, and at least one has to stay selected. Some {{az-workers}} build on each other's results, and some need extra features or integrations. Before you decide, check what each {{az-worker}} needs and what depends on it. Refer to [](watches-and-workers.md).

You can turn {{az-workers}} on or off later on their {{az-watch}} pages. Refer to [](configure-worker-settings.md).

% After elastic/docs-content#9144 merges, link configure-worker-settings.md#configure-worker-settings-enabled.

## Start the {{az-workers}} [alertzero-turn-on-workers]

{{az-workers}} need security data to analyze and at least one AI model to run. Onboarding links to where to add data, and you can't start the {{az-workers}} until the space has a model. To prepare ahead, refer to [](/solutions/security/get-started/ingest-data-to-elastic-security.md) and [Connect to an LLM](/solutions/security/ai/set-up-ai-features.md#set-up-ai-llm).

Some {{az-workers}} also need [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) to pass work to each other. Onboarding flags each {{az-worker}} that's missing it. To check which {{az-workers}} need it, refer to [](watches-and-workers.md).

:::{note}
**Enable and run** turns on the {{az-workers}} you selected, so it needs **All** for **{{alertzero}}**, the `manage_security` cluster privilege, and the **Workflows** sub-feature privileges **Update** and **Update managed workflows**. Because `manage_security` also lets anyone who has it manage users and roles for the whole cluster, ask an administrator who already has it to start the {{az-workers}} instead of granting it only for {{alertzero}}. For details, refer to [](alertzero-privileges.md).
:::

% After elastic/docs-content#9115 merges, link the privileges reference in the note to alertzero-privileges.md#alertzero-privileges-configure.

The first time you open {{alertzero}} in a space, onboarding walks you through starting the {{az-workers}}. To open it, select **{{alertzero}}** in the navigation menu. Follow the steps, turn off any {{az-workers}} you decided not to run, then select **Enable and run**.

After you select **Enable and run**, {{alertzero}} opens its home page, the **{{az-proposed-actions-cap}}** page. Scheduled {{az-workers}} start their first run immediately, and their {{az-proposed-actions}} appear there when they need your decision.

## Next steps [alertzero-set-up-next]

- [](alertzero-privileges.md): Give your team the privileges they need to view and decide {{az-proposed-actions}}.
- [](use-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
- [](configure-worker-settings.md): Change {{az-worker}} settings, such as {{az-autonomy}} and schedule.
