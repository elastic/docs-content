---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---
# Manual pipeline configuration [streams-manual-pipeline-configuration]

The **Manual pipeline configuration** lets you create a JSON-encoded array of ingest pipeline processors.

To manually create an array of ingest pipeline processors:

1. Select **Create** → **Create processor**.
1. Select **Manual pipeline configuration** from the **Processor** menu.
1. Set the **Source Field** to the field you want to dissect
1. Set the delimiters you want to use in the **Pattern** field. Refer to the [example pattern](#streams-dissect-example) for more information on setting delimiters.