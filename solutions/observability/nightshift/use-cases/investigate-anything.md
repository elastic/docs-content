---
navigation_title: Investigate anything
applies_to:
  serverless:
    observability: preview
description: Describe any problem in your own words, and get an investigation with the likely cause, the evidence, and actions that you can take.
products:
  - id: observability
  - id: cloud-serverless
---

# Investigate anything [nightshift-investigate-anything]

Describe a problem in your own words, and in a few minutes {{nightshift}} returns the likely cause, the evidence, and actions you can take. You don't need an alert: use it for anything you notice or hear about from a customer.

## Before you begin [nightshift-uc-anything-before]

- An admin has [enabled {{nightshift}}](../get-started/investigations.md#nightshift-get-started-enable), and your data is connected. Refer to [Get started](../get-started.md).
- You have the privileges to start investigations. Refer to [Grant access](../get-started/privileges.md#nightshift-privileges-analyst).
- Investigations count toward the daily limits. Refer to [Investigation limits](../investigation/limits.md).

## Example: slow ticket lookups [nightshift-uc-anything-example]

Customers say that loading their tickets takes ages. No alert has fired. You open {{nightshift}} and ask:

> "In the last 24 hours, why is GET /tickets on inventory-api slow? p95 looks like about 5 seconds."

A few minutes later, {{nightshift}} reports that the `tickets` table in the `encore` database has no index on `order_id`, so every lookup reads most of the table. It shows the latency chart, the queries it ran, the explanations it ruled out, and proposes adding the index.

## Write a good question [nightshift-uc-anything-question]

The more specific your question, the faster {{nightshift}} finds the right data. Include:

- **The service or component**: the name of the service, database, or frontend.
- **The symptom**: slow, failing, timing out, an error message, a number that looks wrong.
- **The time window**: "in the last hour", "since 14:00 UTC", "last night between 02:00 and 03:00 UTC".
- **What you already know**: a recent deploy, a change you suspect, or what you've ruled out.

| Instead of | Ask |
| --- | --- |
| "Checkout is broken" | "Why do checkout requests return 500 errors since 14:00 UTC?" |
| "Database problems?" | "Why are queries from the payment service hitting lock timeouts in the last hour?" |
| "Errors went up" | "What caused the error spike on the payment service last night around 02:00 UTC? We deployed version 2.4 at 01:45." |

:::{tip}
Give a time window when the problem already ended. Without one, {{nightshift}} looks at recent data, and it can report that the problem isn't happening anymore.
:::

## Investigate a problem [nightshift-uc-anything-steps]

:::::{stepper}

::::{step} Start the investigation
:anchor: nightshift-uc-anything-start

1. Select **Nightshift** in the navigation menu to open the home page.
1. Select **Investigate**.
1. Describe the problem, then select **Investigate**.

:::{image} ../../../images/nightshift-home.png
:alt: The Elastic nightshift home page with the Investigate button at the top right, above the severity tiles and the list of investigations
:screenshot:
:::

A card appears in the **In progress** section of the home page, named after your question until {{nightshift}} gives it a title.

No **Investigate** button? It appears after your first investigation. Until then, use the **Ask your own question** box in the **Get started** checklist. Refer to [Try your first investigation](../get-started/investigations.md#nightshift-get-started-first-investigation).
::::

::::{step} Wait for the results
:anchor: nightshift-uc-anything-wait

An investigation usually takes up to five minutes, and stops after 60 minutes at the latest. You don't have to keep the page open. Meanwhile, {{nightshift}} tests hypotheses against your logs, metrics, and traces, and your code if you [connected GitHub](../get-started/investigations.md#nightshift-get-started-other-sources).

When it finishes, the card shows **Investigated** and moves to a severity section, such as **High** or **Medium**. {{nightshift}} rates the severity from what it found. If a person changes it, {{nightshift}} keeps that change unless later findings contradict it.
::::

::::{step} Read the results
:anchor: nightshift-uc-anything-results

Select the card to read the results. Refer to [Read an investigation](../investigation/index.md#nightshift-read-investigation).

:::{image} ../../../images/nightshift-investigation-results.png
:alt: An investigation flyout for a question about slow GET /tickets calls on inventory-api. What's happened summarizes the problem, the trigger card shows the question, and Impact shows a chart of failed calls
:screenshot:
:::

At the top, you can set the **Status**, change the **Severity**, and add **Assignees**. A conclusion is a well-tested hypothesis, not a certainty. Refer to [Check the evidence before you act](../investigation/index.md#nightshift-investigations-accuracy).
::::

::::{step} Check the reasoning
:anchor: nightshift-uc-anything-hypotheses

Select **View hypothesis tree** to check each hypothesis that {{nightshift}} tested. Refer to [Check the reasoning in the hypothesis tree](../investigation/index.md#nightshift-investigations-hypotheses).

:::{image} ../../../images/nightshift-hypothesis-tree-detail.png
:alt: The hypothesis tree with a confirmed hypothesis at 95% confidence selected. The detail panel shows what was tested, the result, and a chart of lock timeouts while a batch session held the lock
:screenshot:
:::

Does the confirmed hypothesis match what you observed? Did {{nightshift}} dismiss something you still suspect? Challenge it in chat. Refer to [Ask follow-up questions](#nightshift-uc-anything-chat).
::::

::::{step} Act on the proposed actions
:anchor: nightshift-uc-anything-actions

{{nightshift}} proposes actions, such as a command, a configuration change, a code fix, or a rollback. It never changes your environment.

:::{image} ../../../images/nightshift-investigation-conclusion.png
:alt: The Conclusion section explains that the tickets table has no index on order_id. Below it, three proposed actions each show Apply manually and Needs review
:screenshot:
:::

If an action fits, make the change, then select **Mark as applied**. Otherwise, select **Decline**. Refer to [Decide on proposed actions](../investigation/index.md#nightshift-investigations-actions).
::::

:::::

## Ask follow-up questions [nightshift-uc-anything-chat]

Chat continues the investigation with everything it found so far. Select **Open chat** at the bottom of the flyout, or the chat icon on the investigation card. The chat opens in Agent Builder next to the investigation.

:::{image} ../../../images/nightshift-investigation-chat.png
:alt: The chat panel open next to an investigation. The agent's answer lists per-minute request and failure counts for GET /tickets, with an Ask anything box at the bottom
:screenshot:
:::
For example, ask "How did you reach this conclusion?", or "Add and test a hypothesis that the slowdown started with the last deploy." For more prompts, refer to [Ask follow-up questions in chat](../investigation/index.md#nightshift-investigations-chat).

## What to check [nightshift-uc-anything-check]

- **Read what it couldn't check**, such as a query plan or a dashboard. A gap there can change the answer.
- **Compare with what you know.** If the timeline or numbers don't match what you saw, say so in chat.
- **Close the investigation when you're done.** Set **Status** to **Closed**. A closed investigation doesn't continue; a new problem starts a new one.
- **Tell Elastic how it went.** Rate answers in chat, or open the {icon}`boxes_vertical` menu on the home page and select **Feedback**.

## Next steps [nightshift-uc-anything-next]

- [Investigate your alerts](./investigate-alerts.md): Start an investigation from an alert instead of a question.
- [Investigate in Slack](./investigate-in-slack.md): Ask {{nightshift}} for help from a Slack thread.
- [How investigations work](../investigation/index.md): Learn how {{nightshift}} forms and tests hypotheses, and how far to trust a conclusion.
- [How {{nightshift}} builds context](../context/index.md): Check what {{nightshift}} learned from this investigation.
