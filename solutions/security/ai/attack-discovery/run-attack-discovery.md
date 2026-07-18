---
navigation_title: Run Attack Discovery
description: "The different ways to trigger Attack Discovery analysis, from a manual run to a fully automated, always-on pipeline."
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run Attack Discovery [run-attack-discovery]

Attack Discovery can be triggered in more than one way. Every method runs the same underlying analysis pipeline, so the discoveries you get are consistent no matter which one you use.

* [Manual runs](/solutions/security/ai/attack-discovery/manual-runs.md): run it on demand from the Attack Discovery UI.
* [Scheduled runs](/solutions/security/ai/attack-discovery/schedule-discoveries.md): let the Alerting framework fire it automatically on a recurring schedule.
<!-- * [Embedded or automated runs](/solutions/security/ai/attack-discovery/embedded-runs.md): call it as a step inside an Elastic Workflow. -->
<!-- * [Conversation-driven runs](/solutions/security/ai/attack-discovery/conversational-runs.md): summon it from an Agent Builder chat using natural language. -->

<!-- Per docs-content-internal#1448, once the 9.5 feature set is confirmed, expand this overview with a comparison (for example, a "Method | Use when | Where it runs" table) to help readers choose between the four paths, and note that they all land on the same audited pipeline (retrieve alerts, LLM identifies chain candidates from anonymized data, validation, persist) inside the same anonymization boundary. Content deferred to a separate PR, not included here. -->
