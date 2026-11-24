---
navigation_title: How detection learns
applies_to:
  serverless:
    observability: preview
description: Learn how Elastic nightshift extracts Knowledge Indicators about your services, infrastructure, and dependencies from your logs, how long it takes, and how to keep that knowledge current.
products:
  - id: observability
  - id: cloud-serverless
---

# How detection learns your system [nightshift-detection-learning]

Detection watches for problems specific to *your* system, not generic problems. To do that, {{nightshift}} first reads your logs and records what it finds. It takes note of which services you run, what infrastructure they use, and what they depend on. You don't have to give it a service catalog, a schema, or any configuration.

{{nightshift}} stores each finding as a Knowledge Indicator (KI). It uses KIs to write detection rules for your services, and discovery uses them to check signals.

## What a Knowledge Indicator is [nightshift-detection-learning-kis]

There are two kinds: feature KIs describe your system, and query KIs are {{esql}} queries for conditions worth watching. Refer to [KI types](../context/knowledge-indicators.md#sig-events-ki-types).

For an example of the KIs that one log line produces, refer to [From a log line to Knowledge Indicators](../context/knowledge-indicators.md#nightshift-ki-example).

## When learning runs [nightshift-detection-learning-when]

Learning, also called KI onboarding, has two steps for each source: it identifies feature KIs, and then generates query KIs from them. It runs:

- **When you add a source.** Learning starts as soon as you create an enabled source.
- **Continuously in the background.** With continuous KI onboarding, {{nightshift}} learns each enabled source again at an interval, so its KIs follow your system as it changes. Continuous KI onboarding turns on when the space gets its first source.
- **When you ask.** Refer to [Manage sources](./sources.md#nightshift-detection-sources-manage).

To change the interval or turn it off, refer to [Continuous KI onboarding](../settings.md#nightshift-settings-ki-onboarding). It's the largest driver of detection cost.

## How long learning takes [nightshift-detection-learning-warmup]

Right after you turn detection on, the **Detection engine** shows **Monitoring** and every count is zero. That's expected.

1. **First KIs and rules, within a few minutes.** {{nightshift}} samples your logs and extracts KIs, then writes rules from them. The **knowledge indicators**, **entities**, and **rules** counts go up.
1. **Rule warm-up, then the first signals.** Rules need some history before a change can stand out. Rules for critical problems need about 40 minutes of data. All other rules need about 2 hours. Detection also checks the rules in turn, which can add up to 30 minutes. Expect the first signals 40 minutes to about 2.5 hours after you turn detection on.
1. **First significant events.** Once the rules have warmed up, detection runs every 10 minutes by default and checks about a third of the rules in each run, so a new problem is detected in about 10 to 30 minutes. Discovery then reviews it in its next run, also every 10 minutes by default, and raises the significant event in that run. Events appear only when something actually changes in your system. On a healthy system, there can be none for a while.

You might not see any events on a healthy system even after a few hours. To rule out a problem, check that:

- The **Detection engine** shows **Monitoring**, not **Paused**.
- **Enable scheduled discovery** is still on in **Settings** → **Detections**.
- Your sources show a green **Status** on the **Sources** page.

## Check what {{nightshift}} learned [nightshift-detection-learning-see]

- **On the Detections page.** The **Entities** list on the left shows the services, databases, storage, and other components that {{nightshift}} learned. Select one to filter the events and rules to it.
- **On the Knowledge page.** The **Knowledge Indicators** tab lists every KI, and you can exclude a wrong one. Refer to [Review KIs](../context/knowledge-indicators.md#nightshift-ki-review).
- **On the Topology tab, in developer mode.** The tab shows the entities and dependencies that {{nightshift}} learned as a graph. Refer to [Explore the topology](#nightshift-detection-learning-topology).

### Explore the topology [nightshift-detection-learning-topology]

The **Topology** tab on the **Detections** page is only available in [developer mode](../settings.md#nightshift-settings-developer-mode). It draws the entities that {{nightshift}} learned from your sources and the dependencies between them.

- In **Sources**, choose the sources to draw from. By default, it uses all readable sources.
- In **Topology view**, select **Neighborhood** to see the entities that you selected in the **Entities** list and the ones connected to them. Use **Hops** to set how far from them to go. Select **Full topology** to see everything.
- Select a node or an edge to read its metadata, such as its subtype, technology, protocol, and where {{nightshift}} learned it.

A dependency that points to something {{nightshift}} hasn't learned yet shows as an **Unresolved reference**.

## Next steps [nightshift-detection-learning-next]

- [Rules and signals](./rules-and-signals.md): Check which rules {{nightshift}} wrote from your KIs and what they found.
- [Knowledge Indicators](../context/knowledge-indicators.md): Browse, correct, and promote KIs.
