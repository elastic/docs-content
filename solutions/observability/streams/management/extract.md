---
applies_to:
  serverless: preview
  stack: preview 9.1
---
# Extract fields [streams-extract-fields]

Unstructured log messages must be parsed into meaningful fields before you can filter and analyze them effectively. Commonly extracted fields include `@timestamp` and the `log.level`, but you can also extract information like IP addresses, usernames, and ports.

Use the **Processing** tab on the **Manage stream** page to process your data. The UI simulates your changes and provides an immediate preview that's tested end-to-end.

The UI also shows indexing problems, such as mapping conflicts, so you can address them before applying changes.

:::{note}
Applied changes aren't retroactive and only affect *future ingested data*.
:::

## Add a processor [streams-add-processors]

Streams uses {{es}} ingest pipelines to process your data. Ingest pipelines are made up of processors that transform your data.

To add a processor:

1. Select **Add processor** to open a list of supported processors.
1. Select a processor from the list:
    - [Date](./extract/date.md)
    - [Dissect](./extract/dissect.md)
    - [Grok](./extract/grok.md)
    - GeoIP
    - Rename
    - Set
    - URL Decode
1. Select **Add Processor** to save the processor.

:::{note}
Editing processors with JSON is planned for a future release, and additional processors may be supported over time.
:::

### Add conditions to processors [streams-add-processor-conditions]

You can provide a condition for each processor under **Optional fields**. Conditions are boolean expressions that are evaluated for each document. Provide a field, a value, and a comparator.
Processors support these comparators:
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

### Preview changes [streams-preview-changes]

Under **Processors for field extraction**, when you set pipeline processors to modify your documents, **Data preview** shows you a preview of the results with additional filtering options depending on the outcome of the simulation.

When you add or edit processors, the **Data preview** updates automatically.

:::{note}
To avoid unexpected results, we recommend adding processors rather than removing or reordering existing processors.
:::

**Data preview** loads 100 documents from your existing data and runs your changes using them.
For any newly added processors, this simulation is reliable. You can save individual processors during the preview, and even reorder them.
Selecting **Save changes** applies your changes to the data stream.

If you edit the stream again, note the following:
- Adding more processors to the end of the list will work as expected.
- Changing existing processors or re-ordering them may cause unexpected results. Because the pipeline may have already processed the documents used for sampling, the UI cannot accurately simulate changes to existing data.
- Adding a new processor and moving it before an existing processor may cause unexpected results. The UI only simulates the new processor, not the existing ones, so the simulation may not accurately reflect changes to existing data.

![Screenshot of the Grok processor UI](<../../../../images/logs-streams-grok.png>)

### Ignore failures [streams-ignore-failures]

Turn on **Ignore failure** to ignore the processor if it fails. This is useful if you want to continue processing the document even if the processor fails.

### Ignore missing fields [streams-ignore-missing-fields]

Turn on **Ignore missing fields** to ignore the processor if the field is not present. This is useful if you want to continue processing the document even if the field is not present.

## Detect and handle failures [streams-detect-failures]

Documents fail processing for different reasons. Streams helps you to easily find and handle failures before deploying changes.

In the following screenshot, the **Failed** percentage shows that not all messages matched the provided Grok pattern:

![Screenshot showing some failed documents](<../../../../images/logs-streams-parsed.png>)

You can filter your documents by selecting **Parsed** or **Failed** at the top of the table. Select **Failed** to see the documents that weren't parsed correctly:

![Screenshot showing the documents UI with Failed selected](<../../../../images/logs-streams-failures.png>)

Failures are displayed at the bottom of the process editor:

![Screenshot showing failure notifications](<../../../../images/logs-streams-processor-failures.png>)

These failures may require action, but in some cases, they serve more as warnings.

### Mapping conflicts

As part of processing, Streams also checks for mapping conflicts by simulating the change end to end. If a mapping conflict is detected, Streams marks the processor as failed and displays a failure message like the following:

![Screenshot showing mapping conflict notifications](<../../../../images/logs-streams-mapping-conflicts.png>)

You can then use the information in the failure message to find and troubleshoot mapping issues going forward.

## Processor statistics and detected fields [streams-stats-and-detected-fields]

Once saved, the processor provides a quick look at the processor's success rate and the fields that it added.

![Screenshot showing field stats](<../../../../images/logs-streams-field-stats.png>)

## Advanced: How and where do these changes get applied to the underlying datastream? [streams-applied-changes]

When you save processors, Streams modifies the "best matching" ingest pipeline for the data stream. In short, Streams either chooses the best matching pipeline ending in `@custom` that is already part of your data stream, or it adds one for you.

Streams identifies the appropriate @custom pipeline (for example, `logs-myintegration@custom` or `logs@custom`).
It checks the default_pipeline that is set on the datastream.

You can view the default pipeline at **Manage stream** → **Advanced** under **Ingest pipeline**.
In this default pipeline, we locate the last processor that calls a pipeline ending in `@custom`. For integrations, this would result in a pipeline name like `logs-myintegration@custom`. Without an integration, the only `@custom` pipeline available may be `logs@custom`.

- If no default pipeline is detected, Streams adds a default pipeline to the data stream by updating the index templates.
- If a default pipeline is detected, but it does not contain a custom pipeline, Streams adds the pipeline processor directly to the pipeline.

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
- Streams does not support all processor options. We are working on adding more options in the future.
- The data preview simulation may not accurately reflect the changes to the existing data when editing existing processors or re-ordering them.
- Dots in field names are not supported. You can use the dot expand processor in the `@custom` pipeline as a workaround. You need to manually add the dot expand processor.
- Providing any arbitrary JSON in the Streams UI is not supported. We are working on adding this in the future.
