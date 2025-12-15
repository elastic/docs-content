---
applies_to:
  serverless: preview
  stack: preview 9.2
---

# Partition data into child streams [streams-partitioning]
:::{note}
The **Partitioning** tab and the ability to route data into child streams is only available on [wired streams](../wired-streams.md).
:::

For [wired streams](../wired-streams.md), the `/logs` endpoint acts as the entry point for all your log data.

Once you've sent your data to the `/logs` endpoint, open the stream and use the **Partitioning** tab to organize and route the data into meaningful child streams. For example, you can partition your logs into child streams their source or type:

- Route application logs to a `logs.myapp` child stream.
- Route system logs to a `logs.system` child stream.

For more on when to partition your data and how granular your partitioning should be, refer to [Partitioning recommendations](#streams-partitioning-recommendations).

Create partitions using the following options:

- [**Manual configuration**](#streams-manual-partitioning): Use fields and attributes from your data to define how it's routed to child streams.
- [**AI suggestions**](#streams-AI-partitioning): Let Streams analyze your data and suggest partitions, which you can review and accept or reject.

## Partitioning recommendations [streams-partitioning-recommendations]

Partitioning helps you manage your data when you have multiple systems sending logs to a single parent stream.

Focus on logical groupings for data such as by team or overarching technology. For example, partition web server logs in one stream and custom application logs in another.

Don't partition by fields with high cardinality. Even partitioning by common fields like `service.name` can create too many partitions to manage effectively.

As a general rule, aim for tens of partitions, not hundreds. Each partition comes with a cost, as it creates a data stream in {{es}} under the hood. You can have many of them, but not an unlimited amount.

### When you *need* to partition [streams-must-partition]

You only *need* a partition when you want a subset of your data to follow a different lifecycle than the rest.

For example, suppose you have a noisy firewall and a quiet custom application sending logs to the same stream. You don't need to retain the firewall logs for as long and they take up disk space. In this case, you can partition the stream and assign a different [{{ilm-init}} policy or retention setting](./retention.md) to each child stream:

```bash
logs
- logs.firewall [7d]
- logs.custom-app [30d]
```

## Create partitions manually [streams-manual-partitioning]

To manually configure when to send data to child streams:

1. Select **Create partition manually**.
1. From the **Data preview**, filter data based on fields or attributes by hovering over the field and selecting the {icon}`plus_in_circle` icon. This creates a **Condition** for your stream.
1. Under **Stream name**, give your stream a name based on the condition.
1. Select **Save** to create the child stream.

## Create partitions using AI suggestions [streams-AI-partitioning]

:::{note}
This feature requires a [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md).
:::

To use AI suggestions to send data to child streams:

1. Select **Suggest partitions with AI**. Streams uses AI to look at your data and give you suggestions for grouping your data.
1. Either **Accept** or **Reject** the AI suggestions. After selecting **Accept**, you'll see the suggested **Stream name** and **Condition**.
1. Select **Create stream**.

## Next steps

After partitioning your wired streams:

- [Extract fields](./extract.md) using the **Processing** tab to filter and analyze your data effectively.
- [Map fields](./schema.md) using the **Schema** tab to make fields easier to query.