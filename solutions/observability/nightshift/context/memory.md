---
navigation_title: Memory
applies_to:
  serverless:
    observability: preview
description: Check the lessons that Elastic nightshift saved from past investigations, check how useful each one was, and archive or delete memories that are wrong.
products:
  - id: observability
  - id: cloud-serverless
---

# Memory [nightshift-memory]

Memory holds the lessons that {{nightshift}} saved after past investigations, such as where the traces for a service are stored, or that a database problem affected only one service. When a later investigation looks similar, {{nightshift}} recalls the matching memories and starts from them.

{{nightshift}} writes and maintains Memory itself. You can check each memory and how useful it was, and archive or delete the ones that are wrong.

## Open Memory [nightshift-memory-open]

On the [**Knowledge** page](./index.md#nightshift-context-open), select the **Memory** tab.

After the first investigation, Memory holds one or two lessons, such as how your telemetry is laid out. A memory starts at **0% useful · 0% confidence** because no investigation has recalled it yet.

:::{image} ../../../images/nightshift-knowledge-memory.png
:alt: The Memory tab after the first investigation, with one memory about the Elasticsearch OTel telemetry layout for inventory-api and Postgres, at 0% useful and 0% confidence
:screenshot:
:::

## Read the Memory tab [nightshift-memory-read]

As investigations run, Memory grows, and the numbers show which lessons hold up.

:::{image} ../../../images/nightshift-knowledge-memory-populated.png
:alt: The Memory tab with 15 memories. A treemap shows topics such as inventory-api, web, and ticket-issuer. Below it, the Most proven list shows each memory with its usefulness and confidence
:screenshot:
:::

- **Semantic Memory**: A map of the topics that your memories cover, such as a service name or `latency`. Tile size shows each topic's rank score, not a count of memories. Hover a tile to read its **Score** and how many memories it has. Select a tile to show only the memories about that topic, and **Clear all** to show all of them again.
- **Most proven**: The memories that helped most often.
- **Recently updated**: The memories that investigations wrote or changed most recently.
- **Sidebar**: Search with **Search memories**, filter by **All**, **Active**, or **Archived**, and select **Activity** to list recent changes.

Each memory shows two numbers:

- **% useful**: How often the memory helped when an investigation recalled it. Recent investigations count more than older ones: a recall's weight halves every 7 days.
- **% confidence**: How much evidence backs that usefulness figure. It grows as more investigations recall the memory.

For example, a memory at **94% useful · 85% confidence** helped in almost every investigation that recalled it, and was recalled often enough to trust that number.

To read a memory, select it. The details show its **Usefulness**, **Confidence**, **Updated** date, **Tags**, and the **Source task**, which links to the investigation that wrote it. A memory that {{nightshift}} merged from several others lists them under **Merged from**.

## How memories change [nightshift-memory-lifecycle]

After each investigation, {{nightshift}} reviews the memories it recalled and the ones it wrote:

- It updates how useful each recalled memory was.
- It merges memories that say the same thing.
- It archives memories that it judges misleading.

An archived memory shows why it was archived: **merged into another memory**, **judged misleading**, or **archived by a person**. Archived memories are excluded from recall.

## Archive, restore, or delete a memory [nightshift-memory-archive]

You can't edit memories. When a memory is wrong, archive it. You need the privileges listed in [Grant access](../get-started/privileges.md#nightshift-privileges-analyst).

1. On the **Memory** tab, select the memory.
1. Select **Archive**.

Investigations stop recalling it. To use it again, filter by **Archived**, open the memory, and select **Restore**.

To remove a memory for good, open it and select **Delete**, then **Delete permanently**. You can't undo this. Archive instead if you might need the memory again.

To tell {{nightshift}} what's right instead, add [custom context](./index.md#nightshift-context-custom).

## Learn more [nightshift-memory-next]

- [Wiki](./wiki.md): Read the durable pages that every investigation loads.
- [How {{nightshift}} builds context](./index.md): Compare Memory with the other types of context.
- [Cost and models](../cost-and-models.md#nightshift-data): Find out where memories are stored and who can read them.
