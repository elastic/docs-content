---
description: "Find what the AlertZero Endpoint Analysis Worker does, what it needs, its settings, and where its work appears in Elastic Security."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-endpoint-analysis}} {{az-worker}}

The {{az-endpoint-analysis}} {{az-worker}} belongs to the [{{az-forensics-watch}}](forensics-watch.md).

<!--
Placeholder. Model this page on rule-tuning-worker.md. Write an intro with:
1. What the Worker does, and which Watch it's part of.
2. A sentence that says what the page covers: how the Worker works, where to find its proposed actions, its settings, and its limits (if any).
Then a "How it works" section: "On each run, the Endpoint Analysis Worker:" followed by numbered steps,
then a sentence on what it works from (attacks that the Attack Discovery Worker hands off),
then what starts it (it has no Trigger setting; about once a minute, it picks up any new handoffs from the Attack Discovery Worker, whether you approved them or the Attack Discovery Worker handed them off at Supervised),
the autonomy levels it offers (Manual and Supervised), and where its proposed actions appear.
Then add a Settings section, and a Limits section if it has any limits.
This Worker has no schedule, so its Settings section has no Trigger entry.
-->
