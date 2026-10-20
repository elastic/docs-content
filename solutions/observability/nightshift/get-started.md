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
Investigations from an alert work only with alerts created by [{{kib}} alerting](/explore-analyze/alerting/alerts.md). They don't work with alert episodes from the [{{alerting-v2-system}}](/explore-analyze/alerting/esql/system-overview.md).
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

## Next steps [nightshift-get-started-next]

- [Elastic nightshift](./nightshift.md): Get an overview of Elastic nightshift and its requirements
- [Investigations](./investigations.md): Learn how investigations work and how to read the results
- [Context](./memory.md): Review and add what Elastic nightshift knows about your systems
