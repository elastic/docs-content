---
navigation_title: Organize your data
applies_to:
  serverless: preview
  stack: preview 9.2+
description: Learn how to organize your data streams using routing and partitioning.
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Organize your data with Streams

When logs from multiple sources flow into a single wired stream, partitioning lets you route subsets of that data into dedicated child streams. Each child stream can then be managed independently, with its own retention policy, processing rules, and field mappings.

For example, you can route firewall logs to a `logs.otel.firewall` child stream with a 7-day retention, and application logs to a `logs.otel.application` child stream with a 30-day retention, without duplicating any shared configuration.

Streams also gives you the following functionality:

- **No external routing infrastructure required**: No {{product.logstash}}, no third-party tools.
- **Child streams inherit everything from the parent**: Field mappings, lifecycle settings, and processors cascade down automatically.
- **Config changes propagate through the hierarchy**: Updates to a parent stream apply to all children without manual reconfiguration.

:::{note}
Partitioning is only available on [wired streams](./get-data-in.md#get-data-in-wired). If you're using classic streams or all your logs need identical treatment, skip this step.
:::

## Partitioning recommendations [organize-partitioning-recommendations]

Before creating partitions, keep the following in mind:

- **Partition by logical groupings**, not by high-cardinality fields. Group logs by team, technology type, or environment (for example, `web-servers`, `application`, `security`) rather than by individual service names or host identifiers, which can generate too many streams to manage effectively.
- **Aim for tens of partitions, not hundreds.** Each partition creates a dedicated data stream in {{es}}. There is a cost to each one, so keep the number manageable.
- **Partition only when logs form meaningfully distinct groups: by structure, behavior, or both.** Each partition should map to a set of logs with a distinct schema (fields, formats, or log shapes that differ from other sources), different operational behavior (retention duration, access patterns, storage destination), or both. Firewall logs and application logs warrant a split because they look different and often need different retention. Logs from two web servers do not: same schema, same lifecycle, partitioning adds overhead without benefit. If your logs are structurally similar and need identical treatment, a single stream is simpler to operate.

## Partition your data [organize-partitioning]

:::::::{stepper}

::::::{step} Open the Partitioning tab
1. Open **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select your wired stream from the list.
1. Go to the **Partitioning** tab.
::::::

::::::{step} Create a partition
Choose how to define partitions: manually, using field-based conditions, or automatically, by letting AI analyze your data and suggest groupings.

:::::{dropdown} Create partitions manually
1. Select **Create partition**.
1. In the **Data preview**, hover over a field and select:
   - The plus icon to route data where the field matches the value.
   - The minus icon to route data where the field does not match the value.
1. Under **Stream name**, give the child stream a name that reflects the condition.
1. Select **Save** to create the child stream.

Under **Condition**, you can also set the field, comparator, and value directly. Turn on the **Syntax editor** to enter conditions in YAML. For more on conditions, refer to [Streamlang conditions](./streamlang.md#streams-streamlang-conditions).
:::::

:::::{dropdown} Suggest partitions with AI

:::{note}
This feature requires a [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md).
:::

::::{applies-switch}

:::{applies-item} { serverless: preview, stack: preview 9.4+ }

1. Select **Get partitions suggestions**. Streams analyzes your data and suggests groupings.
1. Review the suggested partitions, then **Accept** or **Reject** each one.
1. To refine the results, select **Modify suggestions**, provide guidance (for example, "Partition by service name and severity level"), and submit. Streams regenerates suggestions based on your input.
1. Continue refining as needed, or select **Try again** to start over.
1. After accepting, review the generated **Stream name** and **Condition**.
1. Select **Create stream**.

:::

:::{applies-item} { stack: preview 9.2-9.3 }

1. Select **Suggest partitions with AI**. Streams analyzes your data and suggests groupings.
1. **Accept** or **Reject** the suggestions. After accepting, review the **Stream name** and **Condition**.
1. Select **Create stream**.

:::

::::
:::::
::::::

::::::{step} Review the stream hierarchy
After saving, your stream list updates to show the parent-child relationship. For example:

```
logs
├── logs.otel.application  [30d retention]
└── logs.otel.firewall     [7d retention]
```

Child streams automatically inherit the parent's field mappings, lifecycle settings, and processors. You can override any inherited setting at the child level without affecting the parent or other children.
::::::

:::::::

## Next steps

After partitioning, each child stream can be configured independently. You're ready to:
- Add [processing rules](./parse-and-process.md) to extract fields.
- Set [retention policies](./configure-retention.md) per stream.
- Monitor [data quality](./manage-data-quality.md) for individual streams.
- Review [field naming](./wired-streams-field-naming.md) for the `logs.otel` and `logs.ecs` endpoints.
