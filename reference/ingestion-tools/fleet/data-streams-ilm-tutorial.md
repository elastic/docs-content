---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/data-streams-ilm-tutorial.html
---

# Tutorials: Customize data retention policies [data-streams-ilm-tutorial]

These tutorials explain how to apply a custom {{ilm-init}} policy to an integration’s data stream.


## Before you begin [data-streams-general-info]

For certain features you’ll need to use a slightly different procedure to manage the index lifecycle:

* APM: For verions 8.15 and later, refer to [Index lifecycle management](/solutions/observability/apps/index-lifecycle-management.md).
* Synthetic monitoring: Refer to [Manage data retention](/solutions/observability/apps/manage-data-retention.md).
* Universal Profiling: Refer to [Universal Profiling index life cycle management](/solutions/observability/infra-and-hosts/universal-profiling-index-life-cycle-management.md).


## Identify your scenario [data-streams-scenarios]

How you apply an ILM policy depends on your use case. Choose a scenario for the detailed steps.

* **[Scenario 1](/reference/ingestion-tools/fleet/data-streams-scenario1.md)**: You want to apply an ILM policy to all logs or metrics data streams across all namespaces.
* **[Scenario 2](/reference/ingestion-tools/fleet/data-streams-scenario2.md)**: You want to apply an ILM policy to selected data streams in an integration.
* **[Scenario 3](/reference/ingestion-tools/fleet/data-streams-scenario3.md)**: You want apply an ILM policy for data streams in a selected namespace in an integration.
