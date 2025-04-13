---
applies_to:
    serverless: preview
---
# Extract fields [streams-extract-fields]

Unstructured log messages need to be parsed into meaningful fields so you can filter and analyze them quickly. Common fields to extract include timestamp and the log level, but you can also extract information like IP addresses, usernames, or ports.

Use the **Extract field** page under the **Management** tab to process your data. Changes are immediately available as a preview and tested end-to-end.
The UI simulates your changes, so you can see them immediately.

The UI also shows indexing problems, such as mapping conflicts, so you can address them before applying changes.

:::{note}
Applied changes aren't retroactive and only affect *future data ingested*.
:::

## Add a processor [streams-add-processors]

Streams uses {{es}} ingest pipelines to process your data. Ingest pipelines are made up of processors that transform your data.

To add a processor:

1. Select **Add processor** to open a list of supported processors.
1. Select a processor from the list:
    - [Date](./extract/date.md)
    - [Dissect](./extract/dissect.md)
    - [Grok](./extract/grok.md)
    - [Key-Value (KV)](./extract/key-value.md)
    - GeoIP
    - Rename
    - Set
    - URL Decode
1. Select **Add Processor** to save the processor.

:::{note}
Editing processors with JSON is planned for a future release. More processors may be added over time.
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

### Ignore failures [streams-ignore-failures]

Turn on **Ignore failure** to ignore the processor if it fails. This is useful if you want to continue processing the document even if the processor fails.

### Ignore missing fields [streams-ignore-missing-fields]

Turn on **Ignore missing fields** to ignore the processor if the field is not present. This is useful if you want to continue processing the document even if the field is not present.

### Preview changes [streams-preview-changes]

Under **Processors for field extraction**, set pipeline processors to modify your documents. **Data preview** shows you a preview of the results, with additional filtering options depending on the outcome of the simulation.

When you add or edit processors, the **Data preview** updates automatically.

:::{note}
To avoid unexpected results, focus on adding processors rather than removing or reordering existing processors.
:::

**Data preview** loads 100 documents from your existing data and runs your changes using them.
For any newly added processors, this simulation is reliable. You can save individual processors during the preview, and even reorder them.
Selecting 'Save changes' applies your changes to the data stream.

If you edit the stream again, note the following:
- Adding more processors to the end of the list will work as expected.
- Changing existing processors or re-ordering them may cause unexpected results. Because the the pipeline may have already processed the documents used for sampling, the UI cannot accurately simulate changes to existing data.
- Adding a new processor and moving it before an existing processor may cause unexpected results. The UI only simulates the new processor, not the existing ones, so the simulation may not accurately reflect changes to existing data.

![alt text](<grok.png>)

## Detect and handle failures [streams-detect-failures]

Documents fail processing for different reasons. Streams helps you to easily find and handle failures before deploying changes.

The following example shows not all messages matched the provided grok pattern:

![alt text](<parsed.png>)

You can filter your documents by selecting **Parsed** or **Failed** at the top of the table. Select **Failed** to see the documents that failed:

![alt text](<failures.png>)

Failures are displayed at the bottom of the process editor:

![alt text](<processor-failures.png>)

These failures may be something you should address, but in some cases they also act as more of a warning.

### Mapping Conflicts

As part of processing, streams also checks for mapping conflicts by simulating the change end to end. If a mapping conflict is detected, streams marks the processor as failed and displays a failure message:

![alt text](<mapping-conflicts.png>)

## Processor statistics and detected fields [streams-stats-and-detected-fields]

Once saved, the processor also gives you a quick look at how successful the processing was for this step and which fields were added.

![alt text](<field-stats.png>)

## Advanced: How and where do these changes get applied to the underlying datastream? [streams-applied-changes]

When you save processors, streams modifies the "best matching" ingest pipeline for the data stream. In short, streams either chooses the best matching pipeline ending in `@custom` that is already part of your data stream, or it adds one for you.

Streams identifies the appropriate @custom pipeline (for example, `logs-myintegration@custom` or `logs@custom`).
It checks the default_pipeline that is set on the datastream.

You can view the default pipeline at **Management** → **Advanced** under **Ingest pipeline**.
In this default pipeline, we locate the last processor that calls a pipeline ending in `@custom`. For integrations, this would result in a pipeline name like `logs-myintegration@custom`. Without an integration, the only `@custom` pipeline available may be `logs@custom`.

- If no default pipeline is detected, streams adds a default pipeline to the data stream by updating the index templates.
- If a default pipeline is detected, but it does not contain a custom pipeline, streams adds the pipeline processor directly to the pipeline.

Streams then adds a pipeline processor to the end of that `@custom` pipeline. This processor definition directs matching documents to a dedicated pipeline managed by streams called `<data_stream_name>@stream.processing`:

// Example processor added to the relevant @custom pipeline
{
  "pipeline": {
    "name": "<data_stream_name>@stream.processing", // e.g., logs-my-app-default@stream.processing
    "if": "ctx._index == '<data_stream_name>'",
    "ignore_missing_pipeline": true,
    "description": "Call the stream's managed pipeline - do not change this manually but instead use the streams UI or API"
  }
}

Streams then creates and manages the `<data_stream_name>@stream.processing` pipeline, placing the processors you configured in the UI (Grok, Set, etc.) inside it.

### User interaction with pipelines

Do not manually modify the `<data_stream_name>@stream.processing` pipeline created by streams.
You can still add your own processors manually to the `@custom` pipeline if needed. Adding processors before the pipeline processor streams created may cause unexpected behavior.

## Known limitations [streams-known-limitations]

- The UI does not support all processors. We are working on adding more processors in the future.
- The UI does not support all processor options. We are working on adding more options in the future.
- The simulation may not accurately reflect the changes to the existing data when editing existing processors or re-ordering them.
- Dots in field names are not supported. A workaround you can take is to use a dot expand processor in the @custom pipeline. This is a processor you will have to add manually at this point.
- Providing any arbitrary JSON in the UI is not supported. We are working on adding this in the future.