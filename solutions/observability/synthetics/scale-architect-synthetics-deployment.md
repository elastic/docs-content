---
navigation_title: Scale and architect a deployment
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-scale-and-architect.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-scale-and-architect.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Scale and architect a Synthetics deployment [synthetics-scale-and-architect]

Use these advanced considerations when using the {{synthetics-app}} for large and complex use cases.

% Stateful only for do not use... section

## Do not use the Synthetics UI with CCS/CCR [synthetics-no-ccs-ccr]
```{applies_to}
stack: ga
```

In complex environments it’s common to have multiple task-specific {{stack}} deployments with one  centralized overview cluster using CCS or CCR to centralize {{kib}} dashboards and apps. **Do not use this pattern with the Synthetics UI**. Instead, configure your synthetic monitors directly on the {{kib}} instance where you want to view and manage them.

You may, however, use Dashboards and the Discover feature with CCS to view `synthetics-*` indices.

The Synthetics UI does *not* work with CCS/CCR because it would limit the rich user experience that the Synthetics UI provides. Unlike the majority of {{kib}} apps, the Synthetics UI relies heavily on state stored in {{kib}} shared objects in order to provide a rich user experience. Because {{kib}} saved objects cannot be shared via CCS/CCR, the Synthetics UI will not show any user data even if CCS/CCR is configured.

## Manage large numbers of Synthetic monitors with tags [synthetics-tagging]

When managing larger numbers of synthetic monitors, use tags to keep them organized. Many of the views in the Synthetics UI are tag-aware and can group data by tag.

## Create custom dashboards [synthetics-custom-dashboards]

If we don't provide a UI for your exact needs, you can use [dashboards](/explore-analyze/dashboards.md) to build custom visualizations. For a complete accounting of fields used by the Synthetics UI, refer to [{{heartbeat}}'s exported fields](beats://reference/heartbeat/exported-fields.md).