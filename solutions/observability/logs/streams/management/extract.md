---
applies_to:
    serverless: tp
---
# Extract field
Log messages are often unstructured. To get the most value, it’s important to parse them and extract some of the information into dedicated fields. The most common data to extract is usually the timestamp and the log level, but other pieces of information like IP addresses, usernames, or ports can also be useful.
The extract field UI let’s you easily iterate and process your data. Any change is immediately available as a preview and is tested end to end.
Because the changes to your data's structure is simulated, you'll see them instantly. You'll also see potential indexing problems such as mapping conflicts ahead of time, so you can address them before applying the change.
Applied changes aren't retroactive and only affect **future data ingested**.

## Add a processor
Streams uses {{es}} ingest pipelines to process your data. The processors are the building blocks of the pipeline and are used to transform your data.
To add a processor:

1. Select **Add processor**. This opens a list of supported processors.
1. Select one of the following processors from the list:
  - [Date](./extract/date.md)
  - [Dissect](./extract/dissect.md)
  - [Grok](./extract/grok.md)
  - [Key-Value (KV)](./extract/key-value.md)
  - GeoIP
  - Rename
  - Set
  - URL Decode
1. Save the processor by selecting **Add Processor** towards the top.

JSON editing of the processors is planned for a future release. More processors may be added over time.

### Add conditions to processors
You can provide a condition for each processor under **Optional fields**. The condition is a boolean expression that is evaluated for each document. Provide a field, a value, and a comparator.
Processors support the following comparators:
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

### Ignore failures
Turn on the `Ignore failure` option to ignore the processor if it fails. This is useful if you want to continue processing the document even if the processor fails.

### Ignore missing fields
Turn on the `Ignore missing fields` option to ignore the processor if the field is not present. This is useful if you want to continue processing the document even if the field is not present.

### Preview Changes
The left side of the UI gives you access to a subset of pipeline processors to modify your documents, while the right side shows you a preview of the results, with additional filtering options depending on the outcome of the simulation.

Anytime you make a change on the left side of the UI, the table on the right updates automatically.

We recommend primarily adding processing steps, not removing them or changing the order of existing processors, as this may lead to unexpected results.

To preview changes, streams loads 100 documents from your existing data and runs your changes using them.
For any newly added processors, this simulation is reliable. You can save individual processors during the preview, and even reorder them.
Once you click 'Save changes' at the bottom right of the UI, the changes are applied to the data stream.

If you then edit the stream again, keep the following in mind:
- Adding more processors to the end of the list will work as expected.
- Making changes to existing processors or re-ordering them may cause unexpected results, as we are not able to accurately simulate the changes to the existing data. This is because the documents used for sampling may have already been processed by the pipeline. This is a known limitation.
- Adding a new processor and moving it before an existing processor may have unexpected consequences. The simulation will only simulate the new processor, and not the existing ones. This means that the simulation may not accurately reflect the changes to the existing data.

![alt text](<grok.png>)

## Detect and handle failures
Documents fail processing for many different reasons. Streams helps you to easily find and handle failures before deploying changes.

The following example shows not all messages matched the provided grok pattern:

![alt text](<parsed.png>)

You can filter your documents by selecting **Parsed** or **Failed** at the top of the table. Select **Failed** to see the documents that failed:

![alt text](<failures.png>)

Any failures are displayed at the bottom of the process editor:

![alt text](<processor-failures.png>)

These failures may be something you should address, but in some cases they also act as more of a warning.

**Map Conflicts**
As part of processing, streams also checks for mapping conflicts. This is done by end-to-end simulation of the change. If a mapping conflict is detected, the processor is marked as failed and you'll see a failure message will the UI:

![alt text](<mapping-conflicts.png>)

## Processor Statistics and Detected Fields
Once saved, the processor also gives you statistics at a quick glance to indicate how successful the processing was for this step and which fields were added.

![alt text](<field-stats.png>)

## Advanced: How and where do these changes get applied to the underlying datastream?
When you save processors, streams modifies the ‘best matching’ ingest pipeline for the data stream. In short, streams chooses the best matching pipeline ending in “@custom” that is already part of your data stream or adds one for you.

Streams identifies the appropriate @custom pipeline (for example, logs-myintegration@custom or logs@custom).
It checks the default_pipeline that is set on the datastream.

You can also view the default pipeline in the **Advanced** tab under `Ingest pipeline`.
In this default pipeline, we locate the last processor that calls a pipeline ending in “@custom”. For integrations, this would result in a pipeline name like `logs-myintegration@custom`. When not using the integration, the only @custom pipeline available may be `logs@custom`.
- If no default pipeline is detected, a default pipeline will be added to the data stream by updating the index templates.
- If a default pipeline is detected, but it does not contain a custom pipeline, the pipeline processor is added to the pipeline directly.

Streams then adds a pipeline processor to the end of that @custom pipeline. This processor definition directs matching documents to a dedicated pipeline managed by streams called `<data_stream_name>@stream.processing`:

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

**User Interaction with Pipelines**:
Do not manually modify the `<data_stream_name>@stream.processing` pipeline created by streams.
You can still add your own processors manually to the @custom pipeline if needed. Any processors you add before the pipeline processor streams created may effect the behavior in unexpected ways.

## Known limitations
- The UI does not support all processors. We are working on adding more processors in the future.
- The UI does not support all processor options. We are working on adding more options in the future.
- The simulation may not accurately reflect the changes to the existing data when editing existing processors or re-ordering them.
- Dots in field names are not supported. A workaround you can take is to use a dot expand processor in the @custom pipeline. This is a processor you will have to add manually at this point.
- Providing any arbitrary JSON in the UI is not supported. We are working on adding this in the future.