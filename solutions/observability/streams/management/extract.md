---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---
# Extract fields [streams-extract-fields]

Use the **Processing** tab to add [processors](#streams-extract-processors) that extract meaningful fields from your log messages. These fields let you filter and analyze your data more effectively.

For example, in [Discover](../../../../explore-analyze/discover.md), extracted fields might let you filter for log messages with an `ERROR` log level that occurred during a specific time period to help diagnose an issue. Without extracting the log level and timestamp fields from your messages, those filters wouldn't return meaningful results.

The processing tab also:

- Simulates your processors and provides an immediate [preview](#streams-preview-changes) that's tested end to end.
- Flags indexing issues, like [mapping conflicts](#streams-processing-mapping-conflicts), so you can address them before applying changes.

After creating your processor, all future data ingested ingested into the stream will be parsed into structured fields accordingly.

:::{note}
Applied changes aren't retroactive and only affect *future ingested data*.
:::

## Supported processors [streams-extract-processors]

Streams supports the following processors:

- [Date](./extract/date.md): Converts date strings into timestamps, with options for timezone, locale, and output formatting.
- [Dissect](./extract/dissect.md): Extracts fields from structured log messages using defined delimiters instead of patterns, making it faster than Grok and ideal for consistently formatted logs.
- [Grok](./extract/grok.md): Extracts fields from unstructured log messages using predefined or custom patterns, supports multiple match attempts in sequence, and can automatically generate patterns with an LLM connector.
- [Set](./extract/set.md): Assigns a specific value to a field, creating the field if it doesn’t exist or overwriting its value if it does.
- [Rename](./extract/rename.md): Changes the name of a field, moving its value to a new field name and removing the original.
- [Append](./extract/append.md): Adds a value to an existing array field, or creates the field as an array if it doesn’t exist.

## Add a processor [streams-add-processors]

Streams uses [{{es}} ingest pipelines](../../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) made up of processors to transform your data, without requiring you to switch interfaces and manually update pipelines.

To add a processor from the **Processing** tab:

1. Select **Create** → **Create processor** to open a list of supported processors.
1. Select a processor from the **Processor** menu.
1. Configure the processor and select **Create** to save the processor.

After adding all desired processors and conditions, make sure to **Save changes**.

Refer to individual [supported processors](#streams-extract-processors) for more on configuring specific processors.

:::{note}
Editing processors with JSON is planned for a future release, and additional processors may be supported over time.
:::

### Add conditions to processors [streams-add-processor-conditions]

You can add conditions to processors so they only run on data that meets those conditions. Each condition is a boolean expression evaluated for every document.

To add a condition:

1. Select **Create** → **Create condition**.
1. Provide a **Field**, a **Value**, and a comparator.
1. Select **Create condition**.
1. Select **Save changes**.

:::{dropdown} Supported comparators
Streams processors support the following comparators:

- equals
- not equals
- less than
- less than or equals
- greater than
- greater than or equals
- contains
- starts with
- ends with
- exists
- not exists
:::

### Preview changes [streams-preview-changes]

After you create processors, the **Data preview** tab simulates processor results with additional filtering options depending on the outcome of the simulation.

When you add or edit processors, the **Data preview** updates automatically.

:::{note}
To avoid unexpected results, it's best to add processors rather than remove or reorder existing ones.
:::

**Data preview** loads 100 documents from your existing data and runs your changes against them.
For any newly created processors and conditions, the preview results are reliable, and you can freely create and reorder during the preview.

Select **Save changes** to apply your changes to the data stream.

If you edit the stream after saving your changes, keep the following in mind:

- Adding processors to the end of the list will work as expected.
- Editing or reordering existing processors can cause inaccurate results. Because the pipeline may have already processed the documents used for sampling, **Data preview** cannot accurately simulate changes to existing data.
- Adding a new processor and moving it before an existing processor may cause inaccurate results. **Data preview** only simulates the new processor, not the existing ones, so the simulation may not accurately reflect changes to existing data.

### Ignore failures [streams-ignore-failures]

Each processor has the option to **Ignore failures**. When enabled, processing of the document continues when the processor fails.

### Ignore missing fields [streams-ignore-missing-fields]

Dissect, grok, and rename processors include the **Ignore missing fields** option. When enabled, processing of the document continues when a source field is missing.

## Detect and resolve failures [streams-detect-failures]

Documents can fail processing for various reasons. Streams helps you identify and resolve these issues before deploying changes.

In the following screenshot, the **Failed** percentage indicates that not all messages matched the provided grok pattern:

![Screenshot showing some failed documents](<../../../images/logs-streams-parsed.png>)

You can filter your documents by selecting **Parsed** or **Failed** at the top of the table.
Selecting **Failed** shows the documents that weren't parsed correctly:

![Screenshot showing the documents UI with Failed selected](<../../../images/logs-streams-failures.png>)

Failures are displayed at the bottom of the process editor:

![Screenshot showing failure notifications](<../../../images/logs-streams-processor-failures.png>)

Some failures may require fixes, while others simply serve as a warning.

### Mapping conflicts [streams-processing-mapping-conflicts]

As part of processing, Streams simulates your changes end to end to check for mapping conflicts. If a conflict is detected, Streams marks the processor as failed and displays a message like the following:

![Screenshot showing mapping conflict notifications](<../../../images/logs-streams-mapping-conflicts.png>)

Use the information in the failure message to find and troubleshoot the mapping issues.

## Processor statistics and detected fields [streams-stats-and-detected-fields]

Once saved, the processor displays its success rate and the fields it added.

![Screenshot showing field stats](<../../../images/logs-streams-field-stats.png>)

## Advanced: How and where do these changes get applied to the underlying data stream? [streams-applied-changes]

% make sure this is all still accurate.

When you save processors, Streams modifies the best-matching ingest pipeline for the data stream. In short, it either chooses the best-matching pipeline ending in `@custom` in your data stream, or it adds one for you.

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

### User interaction with pipelines

Do not manually modify the `<data_stream_name>@stream.processing` pipeline created by Streams.
You can still add your own processors manually to the `@custom` pipeline if needed. Adding processors before the pipeline processor created by Streams may cause unexpected behavior.

## Known limitations [streams-known-limitations]

- Streams does not support all processors. We are working on adding more processors in the future.
- The data preview simulation may not accurately reflect the changes to the existing data when editing existing processors or re-ordering them. We will allow proper simulations using original documents in a future version.