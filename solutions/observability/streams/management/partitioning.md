---
applies_to:
  serverless: preview
  stack: preview 9.2
---

# Partition data into child streams [streams-partitioning]
:::{note}
The **Partitioning** tab and the ability to route data into child streams is only available on [wired streams](../wired-streams.md).
:::

For [wired streams](../wired-streams.md), send all of your logs to the `/logs` endpoint. This endpoint acts as your entry point for all of your log data.

Once you've sent your data to the `/logs` endpoint, open the stream and use the **Partitioning** tab to organize and route the data into meaningful child streams. For example, you can partition your logs into child streams their source or type:

- Route application logs to a `logs.myapp` child stream.
- Route system logs to a `logs.system` child stream.

Create partitions using the following options:

- [**Manual configuration**](#streams-manual-partitioning): Use fields and attributes from your data to define how it's routed to child streams.
- [**AI suggestions**](#streams-AI-partitioning): Let Streams analyze your data and suggest partitions, which you can review and accept or reject.

## Create partitions manually [streams-manual-partitioning]

To manually configure when to send data to child streams:

1. Select **Create partition manually**.
1. From the **Data preview**, filter data based on fields or attributes by hovering over the field and selecting the {icon}`plus_in_circle` icon. This creates a **Condition** for your stream.
1. Under **Stream name**, give your stream a name based on the condition.
1. Select **Save** to create the child stream.

## Create partitions using AI suggestions [streams-AI-partitioning]

:::{note}
This feature requires an [LLM connector](../../../security/ai/set-up-connectors-for-large-language-models-llm.md).
:::

To use AI suggestions to send data to child streams:

1. Select **Suggest partitions with AI**. Streams uses AI to look at your data and give you suggestions for grouping your data.
1. Either **Accept** or **Reject** the AI suggestions. After selecting **Accept**, you'll see the suggested **Stream name** and **Condition**.
1. Select **Create stream**.

## Next steps

After partitioning your wired streams:

- [Extract fields](./extract.md) using the **Processing** tab to filter and analyze your data effectively.
- [Map fields](./schema.md) using the **Schema** tab to make fields easier to query.