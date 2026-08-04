---
applies_to:
  stack: experimental 9.5
  serverless: experimental
description: Nightshift memory is a persistent knowledge base that agents read before investigating incidents and write to as they learn.
products:
  - id: observability
  - id: cloud-serverless
---

# Memory [nightshift-memory]

Nightshift **Memory** is a persistent knowledge base that agents read before investigating incidents. Rather than rebuilding knowledge from raw telemetry on every [investigation](./investigations.md), Nightshift maintains a curated wiki of facts about your systems with information about services, deployment processes, infrastructure, known failure patterns, and more. Both agents and users can add memory articles, and each added page reduces the need for external queries for the next similar incident.

To review or edit existing memory pages or create new ones, go to **Streams** → **Significant Events** → **Memory**.

## What memory stores [nightshift-memory-what]

Memory is organized into wiki pages. Each page covers a topic relevant to your environment. Pages use categories to organize knowledge hierarchically (for example, `services/checkout-service` or `infrastructure/kubernetes`). Agents can search, browse, and read these pages during investigations.

## How memory is built [nightshift-memory-how-built]

You can manually create memory pages from the **Memory** tab under **Significant Events** or through the [onboarding interview](#nightshift-memory-onboarding). You can also run the following workflows from the **Workflow actions** {icon}`boxes_vertical` menu:

- [Synthesize Memory](#nightshift-memory-synthesis)
- [Consolidate Memory](#nightshift-memory-consolidation)
- [Scrape Conversations](#nightshift-memory-scraper)
- [Detect Gaps](#nightshift-memory-gap-detection)

### Synthesize Memory [nightshift-memory-synthesis]

The **Synthesize Memory** workflow builds wiki pages by selectively querying available information sources like [Knowledge Indicators](../streams/significant-events/knowledge-indicators.md), Significant Events, existing memory pages, and connected external tools. The agent decides which sources to consult based on what's most relevant, then synthesizes the results into coherent pages organized around services, infrastructure, and operations.

### Consolidate Memory [nightshift-memory-consolidation]

The **Consolidate Memory** workflow reviews the full wiki for duplicates, stale entries, and disorganized content. It then merges duplicates, removes outdated pages, improves categories, and adds cross-references between related topics. Consolidation reorganizes data. It doesn't invent new facts.

### Scrape Conversations [nightshift-memory-scraper]

The **Scrape Conversations** workflow reads recent AI Agent conversations. It extracts durable, reusable knowledge like architectural facts, operational patterns, and troubleshooting steps discovered during conversations. It then writes those back to memory as wiki pages.

### Detect Gaps [nightshift-memory-gap-detection]

The **Detect Gaps** workflow audits the entire knowledge base against required knowledge dimensions and identifies what's missing.

It checks the following dimensions:

- Services and applications
- Deployment processes (CI/CD, rollout strategies, feature flags)
- Infrastructure (cloud, Kubernetes, VMs, regions)
- Observability coverage (what data flows into Elastic, what's missing)
- Administrative controls (change freezes, approval processes)
- Health-checking and on-call (dashboards, runbooks, escalation paths)
- Known failure modes (past incidents, postmortems, recurring issues)
- External tools and integrations (deployment APIs, CMDB, incident management)
- Code repositories (structure, branching, ownership)
- Data and request flows (end-to-end paths, queues, databases)
- Access points and connectors (dashboards, wikis, runbooks)

After each run, **Detect Gaps** creates a structured overview page that lists coverage per dimension, the top gaps, and suggested next steps.

## Onboarding interview [nightshift-memory-onboarding]

The onboarding interview is a conversational agent that creates memory pages with knowledge about your specific environment at setup time. The agent asks targeted questions about your system to fill in gaps required for investigations.

To start the onboarding interview, open **Significant Events** and select **Tell us about your system**. Before asking questions, the interview reads the current gap overview and focuses on the highest-priority gaps, so it's best to run the Detect Gaps workflow before starting the interview. The agent skips information that is already covered in memory.

## How agents use memory [nightshift-memory-usage]

When an [investigation](./investigations.md) starts, the investigation agent reads memory pages relevant to the affected service and event type before issuing any telemetry queries. This means:

- The agent starts with knowledge about the service's architecture, known failure modes, and past incident patterns.
- Targeted ES|QL queries replace broad exploratory queries.
- Investigations for familiar issue types complete faster and produce higher-confidence hypotheses.

Memory is also available to you directly during chat. You can ask the AI Agent what it knows about a service, request the current gap overview, or ask it to update a memory page based on something you've learned.

## Give feedback [nightshift-memory-feedback]

Use the **Submit feedback** {icon}`comment` button at the top of the page to share your experience. Your feedback goes directly to the team.

## Learn more [nightshift-memory-nav]

- [Nightshift overview](./nightshift.md): Get an overview of Nightshift, requirements, and how to get started
- [Investigations](./investigations.md): Learn how Nightshift automatically investigates Significant Events and produces root cause hypotheses
- [How Significant Events works](../streams/significant-events/how-it-works.md): Pipeline internals for KI extraction, rule generation, detection, and discovery
- [Knowledge Indicators](../streams/significant-events/knowledge-indicators.md): Get an in-depth overview of how KIs work
- [Operator guide](../streams/significant-events/operator-guide.md): Learn more about system impact, cost drivers, and operational procedures