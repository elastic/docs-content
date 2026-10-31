---
description: "Turn on AlertZero for a space and start the Workers you want."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Set up {{alertzero}} [alertzero-set-up]

To start using {{alertzero}} in a space, turn on its advanced setting, then select which {{az-workers}} to run. {{alertzero}} is off by default, and you set it up separately in each space.

## Before you begin [alertzero-set-up-before]

Check that the [requirements](requirements.md) are in place. To finish setup, you need the [setup privileges](requirements.md#alertzero-requirements-privileges) and an [AI model](requirements.md#alertzero-requirements-ai-model) that {{alertzero}} can use in the space.

## Turn on {{alertzero}} for a space [alertzero-turn-on]

1. In the space where you want {{alertzero}}, go to **Advanced Settings** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Space Settings** tab, find the **{{alertzero}}** setting in the **Security Solution** section, and turn it on.
3. Select **Save changes**, then select **Reload page**.

**{{alertzero}}** appears in the {{elastic-sec}} navigation menu, along with **Escalations** and **Watches**.

## Turn on {{az-workers}} [alertzero-turn-on-workers]

The first time you open {{alertzero}} in a space, the home page walks you through turning on {{az-workers}}.

1. Open **{{alertzero}}** from the navigation menu.
2. On **Let's add your data?**, select **Continue**. To connect more data sources first, select **Open Getting started**.

   If you can't select **Continue**, you need the **{{alertzero}}** privilege set to **All**.

3. On **Let's turn on the {{az-watches}}?**, review the list of {{az-workers}}. Every {{az-worker}} is on by default. Turn off any you don't want to run yet. At least one must stay on.
4. Select **Enable and run**.

{{alertzero}} turns on the {{az-workers}} you kept, creates a service account for each one, and opens the home page. {{az-workers}} that run on a schedule start their first run right away. The {{az-endpoint-analysis}} {{az-worker}} waits until the {{az-attack-discovery}} {{az-worker}} hands it an attack. Until the first {{az-proposed-actions}} arrive, the home page shows **{{az-workers}} are running in the background**.

## If you can't turn on {{az-workers}} [alertzero-set-up-blocked]

The onboarding page shows a message when something blocks a {{az-worker}} from turning on.

| Message | What to do |
| --- | --- |
| **AI models aren't set up for this space** | Make an AI model available in the space, such as an LLM connector, then return to {{alertzero}}. Refer to [AI model](requirements.md#alertzero-requirements-ai-model). |
| **You need the manage_security cluster privilege to enable {{az-workers}}** | Ask an admin who has the [setup privileges](requirements.md#alertzero-requirements-privileges) to turn on the {{az-workers}}. |
| **Some {{az-workers}} weren't turned on** | {{alertzero}} couldn't create the service accounts for the {{az-workers}} the message lists. Select **Enable and run** again to retry them. |

## Turn off {{alertzero}} [alertzero-turn-off]

Turning off the {{alertzero}} setting hides {{alertzero}} in the space, but its {{az-workers}} stay on and keep running. To stop them, turn off each {{az-worker}} on its {{az-watch}} page before you turn off the setting, because the {{az-watch}} pages aren't available while the setting is off. Refer to [](configure-worker-settings.md).

## Next steps [alertzero-set-up-next]

- [](use-alertzero.md): Decide the {{az-proposed-actions}} that {{az-workers}} bring you.
- [](configure-worker-settings.md): Change a {{az-worker}}'s {{az-autonomy}}, schedule, and other settings.
- [](watches-and-workers.md): Find out what each {{az-worker}} does.
