---
applies_to:
  serverless:
    observability: preview
description: Get started with Elastic nightshift. Check the requirements, enable it, add data, run your first investigation, and create your first automation.
products:
  - id: observability
  - id: cloud-serverless
---

# Get started with Elastic nightshift [nightshift-get-started]

To use Elastic nightshift in a space, enable it, connect the data and tools that investigations use, and run your first investigation. Elastic nightshift is off by default, so an admin needs to enable it.

Check the requirements first, then follow the steps. They match the **Get started** checklist on the Elastic nightshift home page.

## Requirements [nightshift-get-started-requirements]

Make sure you meet the following requirements:

- **An {{obs-serverless}} project on the Complete tier**: In Tech Preview, Elastic nightshift is available only on {{serverless-full}}. It isn't available on self-managed or {{ech}} deployments.
- **Access to Elastic nightshift**: Your project must have Elastic nightshift [enabled](#nightshift-get-started-enable).
- **Data to monitor**: Elastic nightshift works with the data you already have in your local project or in remote serverless projects connected through {{cps}}.
- **A connector for your data**: Investigations query your data through a connector, so you add an External Elasticsearch connector when you set up. Refer to [Connect your data and tools](./get-started/connect-your-data-and-tools.md).
- **The right privileges**: An administrator with the `manage_security` privilege and the **Manage engines** privilege must enable Elastic nightshift. Other access depends on user roles. Refer to [Grant access to Elastic nightshift](./get-started/privileges.md).

Elastic nightshift uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).

## Set up Elastic nightshift [nightshift-get-started-steps]

:::::{stepper}

::::{step} Enable Elastic nightshift
:anchor: nightshift-get-started-enable

An admin enables Elastic nightshift once for each space. You need a role with the `manage_security` cluster privilege and the **Manage engines** Elastic nightshift privilege. If you don't have these privileges, ask and admin to enable Elastic nightshift.

1. Open the Elastic nightshift home page. If Elastic nightshift isn't enabled for the space yet, the page shows **One-time admin setup required for this space**.
1. Select **Enable Elastic Nightshift**.
::::

::::{step} Add data
:anchor: nightshift-get-started-add-data

Investigations are only as good as the data Elastic nightshift has access to. To give Elastic nightshift access to more data:

- **Connect your tools.** Add connectors so the investigation agent can query your data and read the code behind your systems. Tech Preview supports External Elasticsearch, GitHub, and Slack. Refer to [Connect your data and tools](./get-started/connect-your-data-and-tools.md).
- **Optionally, choose the data that detection watches.** Refer to [Set up detection sources](./audit-and-manage-detections.md#nightshift-detections-sources).
::::

::::{step} Try your first investigation
:anchor: nightshift-get-started-first-investigation

Describe a problem and let Elastic nightshift look into it. Use a problem from your own systems, or a question such as "Why is checkout latency up?"

1. From the home page, select **Investigate**, describe the problem, and select **Investigate**. The investigation appears in the **In progress** section. Refer to [Start an investigation](./investigate-and-respond.md#nightshift-investigations-start).
1. Select the investigation to open it, and read **What's happened**, **Impact**, and **Conclusion**. Refer to [Read investigation results](./investigate-and-respond.md#nightshift-investigations-results).
1. In **Conclusion**, select **View hypothesis tree** to see how Elastic nightshift reached its conclusion. Each hypothesis is marked **Confirmed** or **Dismissed**, with a confidence percentage.
1. In **Proposed actions**, select an action and read why it's suggested. If you make the change in your environment, select **Mark as applied**. Elastic nightshift doesn't make the change for you. Refer to [Review proposed actions](./investigate-and-respond.md#nightshift-investigations-actions).
1. Select **Open chat** and ask a question, for example "How did you arrive at this conclusion?" The conversation opens in Agent Builder and continues the investigation. Refer to [Ask follow-up questions in chat](./investigate-and-respond.md#nightshift-investigations-chat).
::::

::::{step} Create your first automation
:anchor: nightshift-get-started-first-automation

An automation starts investigations for you when an alert fires or on a schedule, and can post the results to Slack. Refer to [Set up an automation](./set-up-an-automation.md).
::::

:::::

## What enabling Elastic nightshift sets up [nightshift-get-started-enable-sets-up]

Elastic nightshift runs investigations as the `nightshift_agent` service account, not as the person who started them.

A deployment has two Elastic nightshift service accounts:

- `nightshift_agent` runs investigations, their sandbox tools, and the agent's hooks.
- `nightshift_automations` runs automation workflows.

Each account has a role that Elastic nightshift doesn't create or change, and the roles cover every space. Setting up a space grants the agent the privileges that it needs, installs the investigation agent in the space, and installs the workflows that run as these accounts. Which account acts in a space is decided by the workflows that are installed there.

The agent performs investigations and actions on behalf of the users in the space. You can revoke the privileges at any time in **Settings**.

Investigations use the connectors in the space and the credentials stored in those connectors. Refer to [Connect your data and tools](./get-started/connect-your-data-and-tools.md).

## Next steps [nightshift-get-started-nav]

- [Connect your data and tools](./get-started/connect-your-data-and-tools.md): Add the connectors that investigations use, including Slack
- [Set up detection sources](./audit-and-manage-detections.md#nightshift-detections-sources): Choose the data that detection watches
- [Investigations](./investigations.md): Find what needs attention, start investigations from alerts, and act on the results
- [Set up an automation](./set-up-an-automation.md): Run investigations when an alert fires or on a schedule
- [Core components](./core-components/index.md): Learn how the engines, automations, proposed actions, and connectors work
- [Manage Elastic nightshift](./manage/index.md): Configure settings, manage knowledge, and set run limits
