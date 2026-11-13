---
navigation_title: Review decision trees
applies_to:
  serverless:
    observability: preview
description: View the decision trees that Elastic nightshift keeps for alerts it has investigated. Decision trees are experimental and available in developer mode.
products:
  - id: observability
  - id: cloud-serverless
---

# Review decision trees [nightshift-decision-trees]

A decision tree is the troubleshooting path that {{nightshift}} keeps for an alert it has investigated. It tells you which evidence to gather first, which checks decide between explanations, and where each branch led. When the same alert fires again, the investigation can follow the tree.

A tree can also steer an investigation down a path that doesn't fit this time. As with any investigation, check the hypothesis tree and the evidence before you act.

Decision trees are experimental. You can view them only in developer mode, and they can change or go away in later releases.

## Decision trees and the hypothesis tree [nightshift-decision-trees-vs-hypothesis]

They sound alike but aren't the same thing.

| | Hypothesis tree | Decision tree |
| --- | --- | --- |
| Covers | One investigation | One alert, across many investigations |
| Shows | The explanations that the investigation tested, with a confidence for each | The path of checks and decisions that worked before for this alert |
| Where | In the investigation, under **View hypothesis tree** | **Knowledge** > **Decision Trees**, in developer mode |

To read a hypothesis tree, refer to [How investigations work](../investigation/index.md).

## How a tree grows [nightshift-decision-trees-grow]

{{nightshift}} builds a tree for an alert after an investigation of that alert. Each later investigation can add nodes and branches, which creates a version of the tree.

- A tree starts as **Tentative**.
- It becomes **Established** when a person confirms the cause in a follow-up, and the investigation's own evidence supports that cause. A statement alone doesn't confirm it.

Investigations use decision trees whether developer mode is on or off. Developer mode only shows the **Decision Trees** tab.

## View decision trees [nightshift-decision-trees-view]

1. Turn on [developer mode](../settings.md#nightshift-settings-developer-mode).
1. Open the {icon}`boxes_vertical` menu and select **Knowledge**.
1. Select the **Decision Trees** tab.

:::{image} ../../../images/nightshift-knowledge-decision-trees.png
:alt: The Decision Trees tab in developer mode, with a list of trees for different alerts and one tree open in the Diagram view
:screenshot:
:::

The **Overview** shows how many trees there are, how many are established, and how many versions they have. Select a tree to open it:

- **Decision tree**: The tree as a **Diagram**, or as its **Source**. Node types are **Symptom**, **Evidence Gatherer**, **Decision**, and **End**.
- **Version history**: Each version of the tree, with the nodes and edges that an investigation added, changed, or removed.
- **Learnings**: Lessons that people confirmed in follow-ups for this alert.
- **Nodes** and **Edges**: The tree as tables.

You can't edit or archive a decision tree. To remove decision tree versions, [purge knowledge](../settings.md#nightshift-settings-developer-mode).

## Learn more [nightshift-decision-trees-next]

- [How {{nightshift}} builds context](./index.md): Compare decision trees with the Wiki and Memory.
- [Settings and limits](../settings.md#nightshift-settings-developer-mode): Find out what else developer mode shows.
