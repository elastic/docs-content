---
navigation_title: Customize data retention policies
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/data-streams-ilm-tutorial.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: fleet
  - id: elastic-agent
---

# Customize data retention policies for integrations [data-streams-ilm-tutorial]

These tutorials explain how to apply a custom {{ilm-init}} policy to an integration’s data stream.


## Before you begin [data-streams-general-info]

For certain features you’ll need to use a slightly different procedure to manage the index lifecycle:

* APM: For versions 8.15 and later, refer to [Index lifecycle management](/solutions/observability/apm/index-lifecycle-management.md).
* Synthetic monitoring: Refer to [Manage data retention](/solutions/observability/synthetics/manage-data-retention.md).
* Universal Profiling: Refer to [Universal Profiling index life cycle management](/solutions/observability/infra-and-hosts/universal-profiling-index-life-cycle-management.md).


## Identify your use case [data-streams-scenarios]

How you apply an ILM policy depends on the data streams you want it to cover. Choose the approach that matches your use case.

* **[Apply an ILM policy to all data streams across all namespaces](/reference/fleet/data-streams-scenario1.md)**: Edit the `logs@custom` or `metrics@custom` component template, so the policy covers every {{fleet}} `logs-*` or `metrics-*` data stream. Repeat separately for logs and for metrics.
* **[Apply an ILM policy to specific data streams across all namespaces](/reference/fleet/data-streams-scenario2.md)**: Edit a data stream's own `@custom` component template, leaving the integration's other data streams untouched.
* **[Apply an ILM policy to one data stream in one namespace](/reference/fleet/data-streams-scenario3.md)**: Clone the integration's index template and scope the copy to a single namespace. This is the heaviest option, because you take on maintaining the cloned template.

  {applies_to}`stack: ga 9.5+` For shared settings across every data stream in a namespace, refer to [Customize data streams with namespace index templates](/reference/fleet/data-streams-namespace-custom.md).

* {applies_to}`stack: ga 9.1` **[Apply an ILM policy to all data streams in a custom integration](/reference/fleet/data-streams-scenario4.md)**: Create an `<integration>@custom` component template for an integration package you built yourself.

::::{note}
:applies_to: stack: ga 9.5+

To apply an ILM policy to every data stream an integration produces in a single namespace, without editing templates yourself, refer to [Apply an {{ilm-init}} policy to an integration namespace](/reference/fleet/data-streams-namespace-ilm.md). This option requires [namespace index templates](/reference/fleet/data-streams-namespace-custom.md).
::::
