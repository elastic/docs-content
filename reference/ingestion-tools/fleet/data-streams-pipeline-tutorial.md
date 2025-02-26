---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/data-streams-pipeline-tutorial.html
---

# Tutorial: Transform data with custom ingest pipelines [data-streams-pipeline-tutorial]

This tutorial explains how to add a custom ingest pipeline to an Elastic Integration. Custom pipelines can be used to add custom data processing, like adding fields, obfuscate sensitive information, and more.

**Scenario:** You have {{agent}}s collecting system metrics with the System integration.

**Goal:** Add a custom ingest pipeline that adds a new field to each {{es}} document before it is indexed.


## Step 1: Create a custom ingest pipeline [data-streams-pipeline-one]

Create a custom ingest pipeline that will be called by the default integration pipeline. In this tutorial, we’ll create a pipeline that adds a new field to our documents.

1. In {{kib}}, navigate to **Stack Management** → **Ingest Pipelines*** → ***Create pipeline** → **New pipeline**.
2. Name your pipeline. We’ll call this one, `add_field`.
3. Select **Add a processor**. Fill out the following information:

    * Processor: "Set"
    * Field: `test`
    * Value: `true`

        The [Set processor](elasticsearch://docs/reference/ingestion-tools/enrich-processor/set-processor.md) sets a document field and associates it with the specified value.

4. Click **Add**.
5. Click **Create pipeline**.


## Step 2: Apply your ingest pipeline [data-streams-pipeline-two]

Add a custom pipeline to an integration by calling it from the default ingest pipeline. The custom pipeline will run after the default pipeline but before the final pipeline.


### Edit integration [_edit_integration]

Add a custom pipeline to an integration from the **Edit integration** workflow. The integration must already be configured and installed before a custom pipeline can be added. To enter this workflow, do the following:

1. Navigate to **{{fleet}}**
2. Select the relevant {{agent}} policy
3. Search for the integration you want to edit
4. Select **Actions** → **Edit integration**


### Select a data stream [_select_a_data_stream]

Most integrations write to multiple data streams. You’ll need to add the custom pipeline to each data stream individually.

1. Find the first data stream you wish to edit and select **Change defaults**. For this tutorial, find the data stream configuration titled, **Collect metrics from System instances**.
2. Scroll to **System CPU metrics** and under **Advanced options** select **Add custom pipeline**.

    This will take you to the **Create pipeline** workflow in **Stack management**.



### Add the pipeline [_add_the_pipeline]

Add the pipeline you created in step one.

1. Select **Add a processor**. Fill out the following information:

    * Processor: "Pipeline"
    * Pipeline name: "add_field"
    * Value: `true`

2. Click **Create pipeline** to return to the **Edit integration** page.


### Roll over the data stream (optional) [_roll_over_the_data_stream_optional]

For pipeline changes to take effect immediately, you must roll over the data stream. If you do not, the changes will not take effect until the next scheduled roll over. Select **Apply now and rollover**.

After the data stream rolls over, note the name of the custom ingest pipeline. In this tutorial, it’s `metrics-system.cpu@custom`. The name follows the pattern `<type>-<dataset>@custom`:

* type: `metrics`
* dataset: `system.cpu`
* Custom ingest pipeline designation: `@custom`


### Repeat [_repeat]

Add the custom ingest pipeline to any other data streams you wish to update.


## Step 3: Test the ingest pipeline (optional) [data-streams-pipeline-three]

Allow time for new data to be ingested before testing your pipeline. In a new window, open {{kib}} and navigate to **{{kib}} Dev tools**.

Use an [exists query](elasticsearch://docs/reference/query-languages/query-dsl-exists-query.md) to ensure that the new field, "test" is being applied to documents.

```console
GET metrics-system.cpu-default/_search <1>
{
  "query": {
    "exists": {
      "field": "test" <2>
    }
  }
}
```

1. The data stream to search. In this tutorial, we’ve edited the `metrics-system.cpu` type and dataset. `default` is the default namespace. Combining all three of these gives us a data stream name of `metrics-system.cpu-default`.
2. The name of the field set in step one.


If your custom pipeline is working correctly, this query will return at least one document.


## Step 4: Add custom mappings [data-streams-pipeline-four]

Now that a new field is being set in your {{es}} documents, you’ll want to assign a new mapping for that field. Use the `@custom` component template to apply custom mappings to an integration data stream.

In the **Edit integration** workflow, do the following:

1. Under **Advanced options** select the pencil icon to edit the `@custom` component template.
2. Define the new field for your indexed documents. Select **Add field** and add the following information:

    * Field name: `test`
    * Field type: `Boolean`

3. Click **Add field**.
4. Click **Review** to fast-forward to the review step and click **Save component template** to return to the **Edit integration** workflow.
5. For changes to take effect immediately, select **Apply now and rollover**.


## Step 5: Test the custom mappings (optional) [data-streams-pipeline-five]

Allow time for new data to be ingested before testing your mappings. In a new window, open {{kib}} and navigate to **{{kib}} Dev tools**.

Use the [Get field mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-mapping) to ensure that the custom mapping has been applied.

```console
GET metrics-system.cpu-default/_mapping/field/test <1>
```

1. The data stream to search. In this tutorial, we’ve edited the `metrics-system.cpu` type and dataset. `default` is the default namespace. Combining all three of these gives us a data stream name of `metrics-system.cpu-default`.


The result should include `type: "boolean"` for the specified field.

```json
".ds-metrics-system.cpu-default-2022.08.10-000002": {
  "mappings": {
    "test": {
      "full_name": "test",
      "mapping": {
        "test": {
          "type": "boolean"
        }
      }
    }
  }
}
```


## Step 6: Add an ingest pipeline for a data type [data-streams-pipeline-six]

The previous steps demonstrated how to create a custom ingest pipeline that adds a new field to each {{es}} document generated for the Systems integration CPU metrics (`system.cpu`) dataset.

You can create an ingest pipeline to process data at various levels of customization. An ingest pipeline processor can be applied:

* Globally to all events
* To all events of a certain type (for example `logs` or `metrics`)
* To all events of a certain type in an integration
* To all events in a specific dataset

Let’s create a new custom ingest pipeline `logs@custom` that processes all log events.

1. Open {{kib}} and navigate to **{{kib}} Dev tools**.
2. Run a [pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) request to add a new field `my-logs-field`:

    ```console
    PUT _ingest/pipeline/logs@custom
    {
      "processors": [
        {
          "set": {
            "description": "Custom field for all log events",
            "field": "my-logs-field",
            "value": "true"
          }
        }
      ]
    }
    ```

3. Allow some time for new data to be ingested, and then use a new [exists query](elasticsearch://docs/reference/query-languages/query-dsl-exists-query.md) to confirm that the new field "my-logs-field" is being applied to log event documents.

    For this example, we’ll check the System integration `system.syslog` dataset:

    ```console
    GET /logs-system.syslog-default/_search?pretty
    {
      "query": {
        "exists": {
          "field": "my-logs-field"
        }
      }
    }
    ```


With the new pipeline applied, this query should return at least one document.

You can modify your pipeline API request as needed to apply custom processing at various levels. Refer to [Ingest pipelines](/reference/ingestion-tools/fleet/data-streams.md#data-streams-pipelines) to learn more.
