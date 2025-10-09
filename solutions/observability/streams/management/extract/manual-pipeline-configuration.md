---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---
# Manual pipeline configuration [streams-manual-pipeline-configuration]

The **Manual pipeline configuration** lets you create a JSON-encoded array of ingest pipeline processors.

Refer to the [ingest processor reference][elasticsearch://reference/enrich-processor] for more information on manually configuring processors.

To manually create an array of ingest pipeline processors:

1. Select **Create** → **Create processor**.
1. Select **Manual pipeline configuration** from the **Processor** menu.
1. In **Ingest pipeline processors**, add JSON to manually configure ingest pipelines.

:::{note}
Conditions defined in the processor JSON take precedence over conditions defined in **Optional fields**.
:::