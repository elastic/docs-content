---
description: "Turn on AlertZero in an Elastic Security space with its advanced setting, select which Workers to run, and fix messages that block Workers from turning on."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Set up {{alertzero}} [alertzero-set-up]

{{alertzero}} is off by default, and you set it up separately in each space. Turn on its advanced setting, then select which {{az-workers}} to run.

## Before you begin [alertzero-set-up-before]

Check that the [requirements](requirements.md) are in place. In particular:

- {applies_to}`stack: preview 9.6` The space must use the **Security** solution view.
- You need the [setup privileges](requirements.md#alertzero-requirements-privileges), including the `manage_security` cluster privilege to turn on {{az-workers}}.
- The space needs an [AI model](requirements.md#alertzero-requirements-ai-model) that {{alertzero}} can use.

## Turn on {{alertzero}} for a space [alertzero-turn-on]

1. In the space where you want {{alertzero}}, find **Advanced Settings** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Security Solution** section, turn on the **{{alertzero}}** setting.
3. Select **Save changes**, then select **Reload page**.

**{{alertzero}}**, **{{az-escalations-cap}}**, and **{{az-watches}}** appear in the {{elastic-sec}} navigation menu.

## Turn on {{az-workers}} [alertzero-turn-on-workers]

The first time you open {{alertzero}} in a space, it walks you through turning on {{az-workers}}.

1. In the navigation menu, select **{{alertzero}}**.
2. On the **Let's add your data?** step, select **Continue**. To connect more data sources first, select **Open Getting started**.

   If you can't select **Continue**, you need the **{{alertzero}}** privilege set to **All**.

3. On the **Let's turn on the {{az-watches}}?** step, review the list of [{{az-workers}}](watches-and-workers.md). Every {{az-worker}} is on by default. Turn off any you don't want to run yet, but keep at least one on. Some {{az-workers}} depend on others, so check the [{{az-worker}} dependencies](requirements.md#alertzero-requirements-dependencies) before you turn one off.
4. Select **Enable and run**.

{{alertzero}} turns on the {{az-workers}} you kept, creates a service account for each one, and opens the **{{az-proposed-actions-cap}}** page. Scheduled {{az-workers}} start their first run immediately. The {{az-endpoint-analysis}} {{az-worker}} waits until the {{az-attack-discovery}} {{az-worker}} hands it an attack. Until the first {{az-proposed-actions}} arrive, the page shows **{{az-workers}} are running in the background**.

## If you can't turn on {{az-workers}} [alertzero-set-up-blocked]

If something blocks {{az-workers}} from turning on, the onboarding page shows one of these messages:

| Message | What to do |
| --- | --- |
| **AI models aren't set up for this space** | Make an AI model available in the space, such as an Elastic Managed LLM, then return to {{alertzero}}. To assign models, select **Open Feature settings**. Refer to [AI model](requirements.md#alertzero-requirements-ai-model). |
| **You need the manage_security cluster privilege to enable {{az-workers}}** | Ask an admin who has the [setup privileges](requirements.md#alertzero-requirements-privileges) to turn on the {{az-workers}}. |
| **Some {{az-workers}} weren't turned on** | {{alertzero}} couldn't create service accounts for the {{az-workers}} that the message lists. To retry, select **Enable and run** again. |

## Turn off {{alertzero}} [alertzero-turn-off]

Turning off the advanced setting hides {{alertzero}} in the space, but its {{az-workers}} keep running. You can't reach the {{az-watch}} pages while the setting is off, so turn off the {{az-workers}} first:

1. Turn off each {{az-worker}} on its {{az-watch}} page. Refer to [](configure-worker-settings.md).
2. Turn off the **{{alertzero}}** advanced setting.

## Next steps [alertzero-set-up-next]

- [](alertzero-privileges.md): Give each person the privileges they need to use {{alertzero}}.
- [](use-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
- [](configure-worker-settings.md): Change each {{az-worker}}'s {{az-autonomy}}, schedule, and other settings.
