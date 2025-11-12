---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---
# Manual pipeline configuration [streams-manual-pipeline-configuration]

:::{note}
The manual pipeline configuration processor is only available on [classic streams](../../streams.md#streams-classic-vs-wired).
:::

The **Manual pipeline configuration** lets you create a JSON-encoded array of ingest pipeline processors.This is helpful if you want to add more advanced processing that isn't currently available as part of the UI-based processors.

Refer to the following documentation for more on manually configuring processors:

- [Create readable and maintainable ingest pipelines](../../../../../manage-data/ingest/transform-enrich/readable-maintainable-ingest-pipelines.md)
- [Error handling in ingest pipelines](../../../../../manage-data/ingest/transform-enrich/error-handling.md)
- [Ingest processor reference](elasticsearch://reference/elasticsearch/enrich-processor.md)

To manually create an array of ingest pipeline processors:

1. Select **Create** → **Create processor**.
1. Select **Manual pipeline configuration** from the **Processor** menu.
1. In **Ingest pipeline processors**, add JSON to manually configure ingest pipelines.

:::{note}
Conditions defined in the processor JSON take precedence over conditions defined in **Optional fields**.
:::