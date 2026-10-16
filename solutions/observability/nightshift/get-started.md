---
applies_to:
  serverless:
    observability: preview
description: Start an investigation in Elastic nightshift, ask questions about it, check how it reached its conclusion, and confirm the fix you applied.
products:
  - id: observability
  - id: cloud-serverless
---

# Get started with Elastic nightshift

Use Elastic nightshift to investigate a problem, ask questions about what it found, check how it reached its conclusion, and resolve the problem. You can start from an alert, or describe the problem in your own words. This page suggests ways to try each of these, with the steps for each.

:::{note}
Elastic nightshift is in private preview and isn't enabled by default. To request access, contact your Elastic account team.
:::

## Before you begin [nightshift-get-started-prereqs]

:::{include} _snippets/requirements.md
:::

## Investigate anything [nightshift-get-started-anything]

If you’ve noticed an issue in your system that isn't covered by an alert, describe the problem in your own words. Elastic nightshift runs a structured investigation into whatever you describe.

To start an investigation:

1. From the Elastic nightshift home page, select **Start investigation**.
1. Enter or paste what you want to investigate in the text box. The more context you provide, the better.
1. Select **Investigate**.

The investigation appears on the home page, where you can open it to follow its progress and read the results.

## Investigate an alert [nightshift-get-started-alert]

If an alert needs a closer look, run an investigation into it to find out what happened and how to fix it. Start an investigation from either the [alerts table](#nightshift-get-started-alerts-table) or from an [alert notification](#nightshift-get-started-alert-details).

:::{note}
Investigations from an alert work only with alerts created by [{{kib}} alerting](/explore-analyze/alerting/alerts.md). They don't work with alert episodes from the [{{alerting-v2-system}}](/explore-analyze/alerting/system-overview.md).
:::

### From the Alerts table [nightshift-get-started-alerts-table]

To run an investigation from the **Alerts** table:

1. Find **Alerts** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Find the alert you want to investigate and open the {icon}`boxes_vertical` **More actions** menu, then select {icon}`inspect` **Investigate**.
1. After the investigation starts, select **View investigation**.

When the investigation finishes, it explains what happened and how to fix it.

### From an alert notification [nightshift-get-started-alert-details]

To run an investigation from an alert notification:

1. From an alert notification, open the **Alert details** page in {{kib}}.
1. Open the {icon}`boxes_vertical` **Actions** menu, then select {icon}`inspect` **Investigate**.
1. After the investigation starts, select **View investigation**.

When the investigation finishes, it explains what happened and how to fix it.

## Ask questions about an investigation [nightshift-get-started-questions]

Chat with Elastic nightshift to ask questions about an investigation, or check something else for you.

1. Open the investigation.
1. Select **Open chat**.
1. Ask your question. For example, ask "How did you arrive at this conclusion?"

## Check how Elastic nightshift reached its conclusion [nightshift-get-started-reasoning]

To validate the reasoning behind a conclusion, review the hypotheses Elastic nightshift considered.

1. Open the investigation.
1. Select **View hypothesis tree**.

The hypothesis tree is a diagram that reads from top to bottom and shows:

- **Trigger**: What started the investigation, such as the alert.
- **Hypotheses**: The number of hypotheses analyzed and how many were confirmed or dismissed, followed by a card for each hypothesis. Each card shows the hypothesis, whether it was **Confirmed** or **Dismissed**, its confidence percentage, and an excerpt of the evidence behind it.
- **Conclusion**: The investigation's conclusion, connected to the hypothesis that was confirmed.
- **Proposed actions**: The actions that follow from the conclusion, each with a confidence level.

To read a hypothesis in full, select its card. A panel opens with the complete explanation and the supporting evidence, including charts of the data behind it.

## Resolve a problem and confirm you did it [nightshift-get-started-resolve]

Elastic nightshift proposes actions you can take to mitigate or fix the problem.

1. In the investigation, select a proposed action to view it.
1. Review the proposed action, and make the changes if they make sense.
1. Select **I applied** to confirm that you've applied the action.

## Connect GitHub [nightshift-get-started-github]

GitHub holds the source of truth for the code behind your systems, and often your runbooks, architecture diagrams, and Helm charts too. Connect GitHub to give Elastic nightshift more information to investigate problems with your systems.

1. Find **Connectors** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Create a new connector and select **GitHub**.
1. Enter your credentials. Use a fine-grained personal access token, which lets you limit access to specific repositories.

## Manage what Elastic nightshift knows about your systems [nightshift-get-started-knowledge]

Elastic nightshift learns about your systems every time it runs an investigation. Storing what it learns as knowledge makes future investigations more accurate and uses fewer tokens. You can view this knowledge, correct it, and add your own.

### View what Elastic nightshift knows [nightshift-get-started-knowledge-view]

Open the **Knowledge** page. It has two tabs for what Elastic nightshift knows:

- **Cortex**: A breakdown of what Elastic nightshift knows about your systems, organized by type, such as services, runbooks, postmortems, and queries. Each page shows its type and whether it's established or tentative.
- **Memory**: The individual memories Elastic nightshift has learned.

### Edit, archive, or delete knowledge [nightshift-get-started-knowledge-edit]

If something isn't correct or useful, you can change it.

In **Cortex**:

- To stop Elastic nightshift from using a page, open the page and select **Archive**.
- To change a page yourself, open it and select **Edit**. Elastic nightshift doesn't change a page you edit manually.
- To change a page and let Elastic nightshift keep updating it as it learns, ask the Elastic AI Agent to make the change instead.

In **Memory**:

- To stop Elastic nightshift from using a memory, open it and select **Archive**. Select **Restore** to use it again.
- To remove a memory permanently, select **Delete**.

### Tell Elastic nightshift about your systems [nightshift-get-started-knowledge-add]

Provide Elastic nightshift with information about your systems before it runs an investigation. This helps future investigations know where to look and what to do.

To create a Cortex page yourself:

1. From **Knowledge**, select the **Cortex** tab.
1. Select **New page** {icon}`plus`.
1. In the **New Cortex page** dialog, select a **Type**. Enter a **Slug**, using lowercase words separated by hyphens, such as `checkout-latency-p99`, and a **Title**.
1. Select **Create**, then open the page and select **Edit** to add your content.

Elastic nightshift prioritizes a page you create over other knowledge it has about your systems. It can't change that page over time.

To create knowledge that Elastic nightshift can keep updating as it learns from investigations, ask the Elastic AI Agent to create it:

1. Select **AI Agent**.
1. Ask the agent to create entries about your systems. For example:
   - Ask it to create a service entry for your service and tell it where to look in GitHub. [Connect GitHub](#nightshift-get-started-github) first.
   - Tell it where to find your runbooks.
   - Tell it anything you would want an on-call engineer to know.
1. When the agent asks for permission to write to Cortex, select **Approve**.

You can't manually create memories, only Elastic nightshift can.

## Next steps [nightshift-get-started-next]

- [Elastic nightshift](./nightshift.md): Get an overview of Elastic nightshift and its requirements
- [Investigations](./investigations.md): Learn how investigations work and how to read the results
- [Context](./memory.md): Review and add what Elastic nightshift knows about your systems
