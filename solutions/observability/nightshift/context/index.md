---
navigation_title: How context is built
applies_to:
  serverless:
    observability: preview
description: Find out what Elastic nightshift has learned about your system, where that knowledge comes from, and how to check it, correct it, and add your own context.
products:
  - id: observability
  - id: cloud-serverless
---

# How {{nightshift}} builds context [nightshift-context]

Each investigation starts from what {{nightshift}} has learned previously. While a model brings general troubleshooting skills, it doesn't have knowledge about your services, where their telemetry lives, or how previous issues were resolved. {{nightshift}} context fills that gap, so investigations spend their time on the problem instead of trying to understand your system.

This page explains where that knowledge comes from, and how to check and correct it.

## Where context comes from [nightshift-context-sources]

Knowledge builds up in layers, from your raw telemetry to what {{nightshift}} learned from its own work.

:::{image} ../../../images/nightshift-context-layers.svg
:alt: Four layers of context, from bottom to top: your telemetry, Knowledge Indicators (KIs), your knowledge, and learnings (Wiki and Memory). An investigation reads your telemetry, your knowledge, and the learnings, and writes what it learns back to the Wiki and Memory. Detection uses the KIs to raise significant events, which can start an investigation.
:width: 100%
:::

Knowledge reaches {{nightshift}} in the following ways:

1. **From your data, ahead of time.** When detection is on, it reads the data in your sources and extracts Knowledge Indicators (KIs), which include facts about your services, dependencies, and technologies. Detection uses them to create rules and find significant events. Investigations don't read KIs directly. KIs reach them through significant events.
1. **From people.** Custom context and automation instructions tell {{nightshift}} information it can't learn from your data, such as team conventions, where to look first, and the location of your runbooks and code. Investigations then read those runbooks and code when they run.
1. **From its own investigations.** After each investigation, {{nightshift}} saves what it learned. Durable facts about your services and integrations go to the Wiki. Lessons, such as which checks found the cause, go to Memory. For alerts it has investigated before, it keeps the troubleshooting path that worked as a decision tree, which you can view in developer mode.

Every investigation reads the Wiki, recalls the memories that match the problem, and follows your instructions. Then it saves what it learned, so the next investigation starts further ahead.

For example, after its first investigation of a slow service, {{nightshift}} can save a memory about where that service's telemetry lives, and Wiki pages for the service and its database. The next investigation of that service reads them first and doesn't have to search for the right indices again.

## Compare the types of context [nightshift-context-compare]

| | What it is | Who writes it | When it's used | Can you change it? |
| --- | --- | --- | --- | --- |
| [Knowledge Indicators](./knowledge-indicators.md) | Facts and queries that detection extracts from your data, such as services, dependencies, and known failure patterns | {{nightshift}}, from your detection sources | When detection creates rules and finds significant events | Exclude, restore, delete, or keep them from expiring |
| [Wiki](./wiki.md) | Short pages about your services, integrations, runbooks, and queries | {{nightshift}}, after each investigation | Read at the start of every investigation | Archive or restore pages. You can't edit them. |
| [Memory](./memory.md) | Lessons from past investigations | {{nightshift}}, after each investigation | Searched by meaning, and recalled when an investigation looks similar | Archive, restore, or delete memories. You can't edit them. |
| [Custom context](#nightshift-context-custom) | Notes about your environment and conventions | You | Added to every investigation and chat in the space | Yes, add, edit, or delete notes |
| [Decision trees](./decision-trees.md) | Troubleshooting paths for alerts that {{nightshift}} has investigated before | {{nightshift}}, after investigations | Followed when the same alert fires again | No. View them in developer mode. |

## Open the Knowledge page [nightshift-context-open]

The **Knowledge** page shows everything that {{nightshift}} has learned.

1. Open {{nightshift}}: select **Nightshift** in the navigation menu.
1. On the home page, open the {icon}`boxes_vertical` menu and select **Knowledge**.

:::{image} ../../../images/nightshift-home-menu.png
:alt: The Elastic nightshift home page with the more menu open, showing the Knowledge, Settings, and Feedback options
:screenshot:
:::

The page has a tab for each type of context: **Knowledge Indicators**, **Wiki**, and **Memory**. With [developer mode](../settings.md#nightshift-settings-developer-mode) on, it also has a **Decision Trees** tab.

To view the Knowledge page, or to archive, restore, or delete entries, you need the privileges listed in [Grant access](../get-started/privileges.md#nightshift-privileges-analyst).

## Correct what {{nightshift}} learned [nightshift-context-correct]

{{nightshift}} manages the Wiki and Memory itself, so you can't edit them. When an entry is wrong or out of date, archive it. Investigations stop using it, and you can restore it later.

- To archive a Wiki page, refer to [Archive or restore a Wiki page](./wiki.md#nightshift-wiki-archive).
- To archive or delete a memory, refer to [Archive, restore, or delete a memory](./memory.md#nightshift-memory-archive).
- To stop detection from using a Knowledge Indicator, exclude it. Refer to [Knowledge Indicators](./knowledge-indicators.md#sig-events-ki-lifecycle).

Then tell {{nightshift}} what's right, with custom context or in your automation instructions.

To remove everything learned after a point in time, use **Purge knowledge** in [developer mode](../settings.md#nightshift-settings-developer-mode).

## Give {{nightshift}} context [nightshift-context-give]

Some things {{nightshift}} can't learn from your data: who owns a service, which checks your team always runs first, or how you name things. Tell it in one of two ways.

| To give context to | Use | Where |
| --- | --- | --- |
| Every investigation and chat in the space | Custom context | **Settings** → **Investigations** |
| The investigations that one automation starts | Automation instructions | The automation's **Additional Instructions** or **Instructions** field |

### Add custom context [nightshift-context-custom]

Custom context is a set of short notes that {{nightshift}} adds to every investigation and chat in the space. In Tech Preview, you can't tell {{nightshift}} to remember something, or write to the Wiki or Memory directly. Custom context is the way to give it knowledge that every investigation uses.

To add, edit, or remove snippets, and for more examples, including how to describe an API behind an HTTP connector, refer to [Add custom context](../investigation/extend.md#nightshift-extend-custom-context).

### Add context to an automation [nightshift-context-automation]

Automation instructions apply only to the investigations that one automation starts, for example "For latency alerts, compare the p95 latency before and after the last deploy." Point them to where your knowledge lives, such as a runbook in a GitHub repository: the investigation reads it when it runs, and what it learns can end up in the Wiki and Memory.

Refer to [Instructions](../investigation/automations.md#nightshift-automations-instructions).

## Learn more [nightshift-context-next]

- [Wiki](./wiki.md): Read the pages that {{nightshift}} loads before each investigation.
- [Memory](./memory.md): Check which lessons {{nightshift}} recalls, and how useful they were.
- [Knowledge Indicators](./knowledge-indicators.md): Understand what detection learns from your data.
- [Cost and models](../cost-and-models.md#nightshift-data): Find out where this knowledge is stored and who can read it.
