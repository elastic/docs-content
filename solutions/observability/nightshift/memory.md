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

Nightshift memory is a persistent knowledge base that agents read before investigating incidents. Rather than re-deriving knowledge from raw telemetry on every [investigation](./investigations.md), Nightshift maintains a curated wiki of facts about your systems, with  services, deployment processes, infrastructure, known failure patterns, and more. Both agents and users can create memory articles.

Each page added to memory reduces the need for external queries for the next similar incident.

## What memory stores [nightshift-memory-what]

Memory is organized into wiki pages. Each page covers a topic relevant to your environment. Pages use categories to organize knowledge hierarchically (for example, `services/checkout-service` or `infrastructure/kubernetes`). Agents can search, browse, and read these pages during investigations.

## How memory is built [nightshift-memory-how-built]

Memory pages are created manually by the user, through the [onboarding interview](#nightshift-memory-onboarding), or by the following workflows.

- [Synthesize Memory](#nightshift-memory-synthesis)
- [Consolidate Memory](#nightshift-memory-consolidation)
- [Scrape Conversations](#nightshift-memory-scraper)
- [Detect Gaps](#nightshift-memory-gap-detection)

### Synthesize Memory [nightshift-memory-synthesis]

Run the **Synthesize Memory** workflow to have it build wiki pages by selectively querying available information sources like Knowledge Indicators, Significant Events, existing memory pages, and connected external tools. The agent decides which sources to consult based on what's most relevant, then synthesizes the results into coherent pages organized around services, infrastructure, and operations.

### Consolidate Memory [nightshift-memory-consolidation]

Run the **Consolidate Memory** workflow to have it review the full wiki for duplicates, stale entries, and disorganized content. It then merges duplicates, removes outdated pages, improves categories, and adds cross-references between related topics. Consolidation reorganizes data. It doesn't invent new facts.

### Scrape Conversations [nightshift-memory-scraper]

Run the **Scrape Conversations** workflow to have it read recent AI agent conversations. It extracts durable, reusable knowledge like architectural facts, operational patterns, troubleshooting steps and discovered during conversations. It then writes those back to memory as wiki pages.

### Detect Gaps [nightshift-memory-gap-detection]

Run the **Detect Gaps** workflow to have it audit the entire knowledge base against required knowledge dimensions and identify what's missing.

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

After each run, **Detect Gaps** writes a structured overview page listing coverage per dimension, the top gaps, and suggested next steps.

## Onboarding interview [nightshift-memory-onboarding]

The onboarding interview is a conversational agent that populates memory with knowledge about your specific environment at setup time. The agent asks targeted questions about your system to fill the gaps most important for accurate investigations.

To start the onboarding interview, open **Significant Events** and select **Tell us about your system**. Before asking questions, the interview reads the current gap overview and focuses on the highest-priority gaps, so running the Detect Gaps workflow first gives you the most targeted session. The agent skips information that is already covered in memory.

## How agents use memory [nightshift-memory-usage]

When an [investigation](./investigations.md) starts, the investigation agent reads memory pages relevant to the affected service and event type before issuing any telemetry queries. This means:

- The agent starts with knowledge about the service's architecture, known failure modes, and past incident patterns.
- Targeted ES|QL queries replace broad exploratory queries.
- Investigations for familiar issue types complete faster and produce higher-confidence hypotheses.

Memory is also available to you directly during chat. You can ask the AI agent what it knows about a service, request the current gap overview, or ask it to update a memory page based on something you've just learned.

## Learn more [nightshift-memory-nav]

- [Nightshift overview](./nightshift.md)
- [Investigations](./investigations.md)