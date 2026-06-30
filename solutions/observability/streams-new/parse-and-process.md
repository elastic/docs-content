---
navigation_title: Process documents
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Process and extract fields from incoming Streams documents using configurable processors, conditions, and live simulation previews.
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
# Process your documents with Streams [streams-extract-fields]

Most log data arrives as unstructured text. To filter, search, and analyze it effectively, you need to extract fields from that raw content. For example, extracted fields let you filter for log messages with an `ERROR` log level that occurred during a specific time period to help diagnose an issue.

The Streams **Processing** tab provides a single place to build and manage your document processing pipeline:

- **[Add processors and conditions](#streams-add-processors)**: Use the Streams UI without needing to manually configure pipeline JSON or Grok syntax.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.3+` **[Generate pipeline suggestions using AI](#streams-generate-pipeline-suggestions)**: Let Streams analyze sample documents and suggests pipeline patterns, so you're refining instead of writing from scratch.
- **[Preview changes](#streams-preview-changes)**: Use the data preview to view which fields your pattern extracts per document, so you can verify field extraction before saving.
- **[Detect and resolve processing issues](#streams-detect-failures)**: Identify which processor or condition is causing documents to fail during processing.
- **[Catch mapping conflicts](#streams-processing-mapping-conflicts)**: Identify potential mapping conflicts before they cause cluster-wide failures. Streams simulates the indexing process end-to-end before deploying.

## Add and configure processors [streams-add-processors]

Streams uses [{{es}} ingest pipelines](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) made up of processors and conditions to transform your data, without requiring you to switch interfaces and manually update pipelines.

To add a processor from the **Processing** tab:

:::::::{stepper}
::::::{step} Add processors and conditions
:anchor: streams-generate-pipeline-suggestions

Use any combination of the following options to build your processing pipeline:

- **Suggest a pipeline**: Let Streams analyze your sample data and generate a complete processor pipeline using AI.
- **Manually add processors**: Select and configure individual processors yourself when you know which transformations you need.
- **Add conditions**: Attach Boolean expressions to define when to run processors.

:::::{tab-set}

::::{tab-item} Suggest a pipeline

```{applies_to}
stack: preview 9.3+
serverless: preview
```

:::{note}
This feature requires a [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md).
:::

Setting up processors is generally a multi-step process. For example, you might need a grok processor to extract fields, a date processor to convert timestamps, and a remove processor to get rid of temporary fields. Instead of creating individual processors manually, you can have AI suggest an entire pipeline for you:

1. From the **Processing** tab, select **Suggest a pipeline**.
1. Review the suggested processors, and either **Accept** or **Reject** the suggestions.
1. Select **Regenerate** to have Streams regenerate the suggested pipeline. Change the large language model (LLM) that Streams uses to generate suggestions from the {icon}`controls` menu.

:::{dropdown} How does Suggest a pipeline work?
:::{include} ../../_snippets/streams-suggestions.md
:::
:::
::::

::::{tab-item} Manually add processors

If you know which processors you want to use, you can add them manually from the Streams UI. Refer to the [Streamlang reference](./streamlang.md) for supported processors and configuration details.

1. Select **Create processor**. You can also let Streams suggest processors by selecting [Suggest a pipeline](#streams-generate-pipeline-suggestions).
1. Select a processor from the **Processor** menu.

   :::{note}
   Let Streams suggest patterns for [Grok](./processors/grok.md#streams-grok-patterns) and [dissect](./processors/dissect.md#streams-dissect-patterns) processors by selecting **Generate pattern**. This feature requires a [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md).
   :::

1. Configure the processor and select **Create** to save the processor.
1. Optional: Turn on **Ignore failures** if you want document processing to continue even when this processor fails.
1. Optional: For dissect, Grok, and rename processors, enable **Ignore missing fields** if you want processing to continue when a source field is missing.
::::

::::{tab-item} Add conditions

You can add conditions—Boolean expressions evaluated for each document—and attach processors that run only when those conditions are met.

To add a condition:

1. Select **Create** → **Create condition**.
1. Provide a **Field**, a **Value**, and a comparator.
1. Select **Create condition**.
1. After creating a condition, add a processor or another condition to it by selecting the {icon}`plus_in_circle`.

Refer to [Conditions](./streamlang.md#streams-streamlang-conditions) in the Streamlang reference for supported operators and examples.
::::

:::::
::::::

::::::{step} Preview changes
:anchor: streams-preview-changes

After adding processors and conditions, the **Data preview** tab simulates processor results with additional filtering options depending on the outcome of the simulation.

When you add or edit processors, the **Data preview** tab updates automatically.

The **Data preview** tab loads 100 documents from your existing data and runs your changes against them.
For any newly created processors and conditions, the preview results are reliable, and you can freely create and reorder during the preview.

If you edit the stream after previewing your changes, keep the following in mind:

- Adding processors to the end of the list works as expected.
- Editing or reordering existing processors can cause inaccurate results. Because the pipeline might have already processed the documents used for sampling, **Data preview** cannot accurately simulate changes to existing data.
::::::

::::::{step} Detect and resolve failures and mapping conflicts
:anchor: streams-detect-failures

Streams helps you catch issues before you apply your processors:

- **Failures**: A processor couldn't parse or transform a document, usually due to a mismatched pattern or missing field.
- **Mapping conflicts**: A processor produced a field type that conflicts with the existing index mapping.

### Detect and resolve failures [streams-detect-failures-section]

Documents can fail processing for various reasons. Streams helps you identify and resolve these issues before deploying changes.

In the following screenshot, the **Failed** percentage indicates that some messages didn't match the provided grok pattern:

:::{image} ../../images/logs-streams-parsed.png
:screenshot:
:::

You can filter your documents by selecting **Parsed** or **Failed** on the **Data preview** tab.
Selecting **Failed** shows the documents that weren't parsed correctly:

:::{image} ../../images/logs-streams-failures.png
:screenshot:
:::

Streams displays failures at the bottom of the process editor. Some failures might require fixes, while others serve as a warning:

:::{image} ../../images/logs-streams-processor-failures.png
:screenshot:
:::

### Detect mapping conflicts [streams-processing-mapping-conflicts]

As part of processing, Streams also simulates your changes end-to-end to check for mapping conflicts. If it detects a conflict, Streams marks the processor as failed and displays a message like the following:

:::{image} ../../images/logs-streams-mapping-conflicts.png
:screenshot:
:::

Use the information in the failure message to find and troubleshoot the mapping issues.
::::::

::::::{step} Save changes
After adding all of your processors and conditions and addressing any issues, select **Save changes**. Streams then parses all future data ingested into the stream according to your pipeline.

:::{note}
Applied changes aren't retroactive and only affect future ingested data.
:::

::::::
:::::::

## Switch between interactive and YAML editing modes [streams-editing-modes]

The Streams processing UI provides an [interactive mode](#streams-editing-interactive-mode) and a [YAML mode](#streams-editing-yaml-mode) for editing processors and conditions.

To switch modes, select the appropriate tab from the top of the processing page.

:::{image} ../../images/streams-editing-modes.png
:screenshot:
:::

Streams defaults to interactive mode unless the configuration can't be represented in interactive mode (for example, when nesting levels are too deep).

### When to use Interactive mode [streams-editing-interactive-mode]

**Interactive** mode provides a form-based interface for creating and editing processors. This mode works best for:

- Users who prefer a guided, visual approach
- Configurations that don't require deeply nested conditions

### When to use YAML mode [streams-editing-yaml-mode]
```{applies_to}
stack: ga 9.3+
```

**YAML** mode provides a code editor for writing Streamlang directly. This mode works best for:

- Users who prefer working with code
- Advanced configurations with complex or deeply nested conditions

Refer to the [Streamlang reference](./streamlang.md) for the complete syntax, condition operators, and examples.

## Known limitations [streams-known-limitations]

- Streams does not support all processors. Refer to the [Streamlang reference](./streamlang.md) for supported processors.
- The data preview simulation might not accurately reflect the changes to the existing data when editing existing processors or re-ordering them.
- Streams can't properly handle arrays. While it supports basic actions like appending or renaming, it can't access individual array elements. For classic streams, the workaround is to use the [manual pipeline configuration](./processors/manual-pipeline-configuration.md) that supports {{product.painless}} scripting and all ingest processors.

## Advanced: How Streams applies processing changes to the underlying data stream [streams-applied-changes]

::::{dropdown} How Streams applies processing changes

When you save processors, Streams appends processing to the best-matching ingest pipeline for the data stream. It either chooses the best-matching pipeline ending in `@custom` in your data stream, or it adds one for you.

Streams identifies the appropriate `@custom` pipeline (for example, `logs-myintegration@custom` or `logs@custom`) by checking the `default_pipeline` that is set on the data stream. You can view the default pipeline on the **Advanced** tab under **Ingest pipeline**.

In this default pipeline, Streams locates the last processor that calls a pipeline ending in `@custom`.
- For integrations, this would result in a pipeline name like `logs-myintegration@custom`.
- Without an integration, the only `@custom` pipeline available may be `logs@custom`.

If no default pipeline is detected, Streams adds a default pipeline to the data stream by updating the index templates.

If a default pipeline is detected, but it does not contain a custom pipeline, Streams adds the pipeline processor directly to the pipeline.

Streams then adds a pipeline processor to the end of that `@custom` pipeline. This processor definition directs matching documents to a dedicated pipeline managed by Streams called `<data_stream_name>@stream.processing`:

```json
// Example processor added to the relevant @custom pipeline
{
  "pipeline": {
    "name": "<data_stream_name>@stream.processing", // for example, logs-my-app-default@stream.processing
    "if": "ctx._index == '<data_stream_name>'",
    "ignore_missing_pipeline": true,
    "description": "Call the stream's managed pipeline - do not change this manually but instead use the Streams UI or API"
  }
}
```

Streams then creates and manages the `<data_stream_name>@stream.processing` pipeline, adding the [processors](#streams-add-processors) you configured in the UI.

Do not manually modify the `<data_stream_name>@stream.processing` pipeline created by Streams.
You can still add your own processors manually to the `@custom` pipeline if needed. Adding processors before the pipeline processor created by Streams might cause unexpected behavior.
::::