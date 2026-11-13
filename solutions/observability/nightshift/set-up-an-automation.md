---
applies_to:
  serverless:
    observability: preview
description: Create an Elastic nightshift automation that runs an investigation when an alert fires or on a schedule, and posts the results to Slack.
products:
  - id: observability
  - id: cloud-serverless
---

# Set up an automation [nightshift-set-up-automation]

Create an automation to run investigations without starting each one yourself. An automation can start an investigation when an alert fires or on a schedule, and post the results to Slack.

## Before you begin [nightshift-set-up-automation-prereqs]

- An admin has [enabled Elastic nightshift](./get-started.md#nightshift-get-started-enable) for the space.
- You have the **All** privilege for Elastic nightshift and the `manage_security` privilege. Without them, the edit actions are disabled.
- To post results to Slack, an admin has [connected the Slack channel](./get-started/connect-your-data-and-tools.md#nightshift-connect-slack), or you have a saved Slack connector.

## Create an automation [nightshift-set-up-automation-create]

1. From the Elastic nightshift home page, select **Automations**, then select **Create automation**.

1. Enter a **Name**. Optionally, add a **Description** and **Tags**.
1. Under **Trigger**, select **Add trigger** and choose one:

   - **Alert triggered**: Starts when an alert changes to **Active**. By default, it matches alerts from any rule. To narrow it, use **Any rule** to search for rules or filter them by tag, and select the rules to match. Each matching alert starts its own investigation, so a rule that fires often can use up your daily limit. Narrow the alerts that the automation matches, and set a limit.
   - **New message in channel**: Starts from a Slack message. Select the channels from the **Select channels** list. By default, the trigger matches any message from anyone through any app. To narrow it, use **Any message** to match only messages that contain certain text, **Anyone** to search for the people whose messages start it, and **Any app** to match only messages that one app or bot posts, using its exact app name, app ID, or bot ID.
   - **Every...**: Starts on a schedule. Choose how often it runs, then enter **Instructions** that describe what to investigate each time. A scheduled automation requires instructions, and they can be up to 5,000 characters.

     - **Hour**: Runs every hour. To run it every hour only during certain hours, select **between hours**, then set the start and end times, such as 09:00 AM and 05:00 PM.
     - **Day**: Runs once a day. Set the time, such as 09:00 AM.
     - **Week**: Runs on the days that you select, from **Mon** to **Sun**, at the time that you set. The weekdays are selected by default.

     Each schedule has a time zone, which defaults to UTC.

1. For an alert or Slack trigger, optionally add context or priorities in the **Additional Instructions** field to guide the investigation. You can enter up to 5,000 characters.
1. Set the trigger's **Daily trigger limit**. The limit defaults to 20 per day, and Elastic nightshift recommends 15 to 20. To remove the limit, turn on **No daily limit**. When the limit is reached, additional triggers are skipped until the count resets at 12:00 AM UTC. The deployment-wide limits are in [Settings and lifecycle](./manage/settings-and-lifecycle.md#nightshift-settings-lifecycle-investigations).
1. Under **Actions**, select **Add action**, then **Post in Slack**, and search for a channel. If no channels are connected, select **Connect channels in Settings**. For a Slack trigger, Elastic nightshift replies in the thread of the message that started the automation.
1. Select **Save** to add the automation to the **Automations** page turned off, or **Save and enable** to turn it on right away. To turn on a saved automation later, use its **Enabled** toggle.

To check what an automation did, refer to [Manage automations and check their runs](./core-components/automations.md#nightshift-automations-manage).

## Give Elastic nightshift context in the instructions [nightshift-set-up-automation-context]

Automate an investigation by setting up an automation on your Slack notifications or on your alerts. Use the **Additional Instructions** field, or the **Instructions** field for a schedule, to tell Elastic nightshift what it needs to investigate, such as:

- Links to the GitHub repositories that hold your architecture
- Where to find your runbooks, skills, and guidance
- Who owns each service

Instructions are the preferred way to give Elastic nightshift context in Tech Preview. After the automation runs once, Elastic nightshift explores what you pointed it to and adds it to the Wiki and Memory, so it can reuse and learn from it in later investigations. To review what it added, refer to [Manage knowledge and memory](./manage/manage-knowledge-and-memory.md).

## Next steps [nightshift-set-up-automation-next]

- [Automations](./core-components/automations.md): Learn how automations work
- [Manage knowledge and memory](./manage/manage-knowledge-and-memory.md): Review what Elastic nightshift has learned
- [Settings and lifecycle](./manage/settings-and-lifecycle.md): Set the daily limits on investigations and detection runs
- [Investigations](./investigate-and-respond.md#nightshift-investigations-slack): Use Slack to chat with Elastic nightshift and receive results
