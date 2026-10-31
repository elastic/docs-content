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

- Complete [what every space needs](requirements.md#alertzero-requirements-every-space). Without an AI model and the privileges to set up {{alertzero}}, you can't turn on {{az-workers}}.
- For the {{az-workers}} you plan to turn on, complete [what specific {{az-workers}} need](requirements.md#alertzero-requirements-specific-workers). You can also do this later, when a {{az-watch}} page warns you.

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

3. On the **Let's turn on the {{az-watches}}?** step, turn off any [{{az-workers}}](watches-and-workers.md) you don't want to run yet. Keep at least one on.

   Every {{az-worker}} is on by default. Some {{az-workers}} need others, so before you turn one off, check [which {{az-workers}} need other {{az-workers}}](requirements.md#alertzero-requirements-dependencies).

4. Select **Enable and run**.

{{alertzero}} turns on the {{az-workers}} you kept, creates a service account for each one, and opens the **{{az-proposed-actions-cap}}** page.

Scheduled {{az-workers}} start their first run immediately, and the page shows "{{az-workers}} are running in the background" until the first {{az-proposed-actions}} arrive. The {{az-endpoint-analysis}} {{az-worker}} waits until the {{az-attack-discovery}} {{az-worker}} hands it an attack.

## If you can't turn on {{az-workers}} [alertzero-set-up-blocked]

If something blocks {{az-workers}} from turning on, the onboarding page shows one of these messages:

| Message | What to do |
| --- | --- |
| "AI models aren't set up for this space" | Make an AI model available in the space, such as an Elastic Managed LLM, then return to {{alertzero}}. To assign models, select **Open Feature settings**. Refer to [AI model](requirements.md#alertzero-requirements-ai-model). |
| "You need the manage_security cluster privilege to enable {{az-workers}}" | Ask an administrator who has the [privileges to set up {{alertzero}}](alertzero-privileges.md) to turn on the {{az-workers}}. |
| "Some {{az-workers}} weren't turned on" | {{alertzero}} couldn't create service accounts for the {{az-workers}} that the message lists. To retry, select **Enable and run** again. |

## Next steps [alertzero-set-up-next]

- [](review-first-proposed-action.md): Follow one {{az-proposed-action}} from the **{{az-proposed-actions-cap}}** page to a decision.
- [](alertzero-privileges.md): Give each person the privileges they need to use {{alertzero}}.
- [](manage-alertzero.md): Change how {{az-workers}} run, or turn {{alertzero}} off in a space.
