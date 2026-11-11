---
navigation_title: Create an integration
description: Prepare a data sample, build a custom integration with Automatic Import, then approve, install, and add it to an agent policy to start collecting data.
type: how-to
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: security
  - id: observability
---

# Create a custom integration with Automatic Import [automatic-import-create]

Build a custom integration from a sample of your data, then install it and add it to an agent policy so that {{agent}} starts collecting the data. To check whether Automatic Import fits your source, refer to [When to use Automatic Import](/explore-analyze/ai-features/automatic-import.md#automatic-import-when-to-use).

{applies_to}`stack: ga 9.0-9.3` In {{stack}} 9.0–9.3, follow [Create an integration in {{stack}} 9.0–9.3](#automatic-import-create-9-0-9-3) instead of [Build and deploy the integration](#automatic-import-build).

## Before you begin [automatic-import-create-prerequisites]

- Make sure that you meet the [Automatic Import requirements](/explore-analyze/ai-features/automatic-import.md#automatic-import-requirements).

$$$automatic-import-sample-data$$$ 
- Prepare a sample of your data in one of the following formats:

   * **JSON and NDJSON**: Represent each event as its own object, and keep nesting shallow.
   * **CSV**: Include a header row with column names. Automatic Import recognizes the header. Without a header, the LLM attempts to create descriptive field names from the column formats and values.
   * **Syslog**: Use a structured or unstructured sample.

   For an accurate pipeline, include a wide range of unique log entries for each event type that you want the integration to handle. Automatic Import reads the file from the beginning, so start it with the event types that matter most to you.

   Your LLM provider receives the sample, so remove or mask personal, sensitive, or confidential values before you upload it.

   {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Instead of uploading a file, you can select an existing index as the sample. The index must include the `event.original` field.

   :::{dropdown} Sample size limits
   :name: automatic-import-sample-limits

   Automatic Import limits how much of the sample it sends to the LLM. Each log line or document counts as one sample.

   {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` You can upload a file of any size. Automatic Import reads the file from the beginning and sends samples to the LLM until it reaches one of the following limits. If it omits samples, the **Sample log limits applied** warning tells you how many samples it sent to the LLM and how many it left out.

   | Limit | Value | What happens |
   | --- | --- | --- |
   | Maximum samples | 1,000 | Stops after adding 1,000 samples to the request. |
   | Maximum sample length | 100,000 characters | Skips the entire sample and continues with later samples. |
   | Maximum request size | 10 MB | Stops before the request to the LLM exceeds 10 MB. |

   {applies_to}`stack: ga 9.0-9.3` Automatic Import sends the first 100 samples to the LLM.
   :::

## Build and deploy the integration [automatic-import-build]
```{applies_to}
serverless: ga
stack: ga 9.4+
```

:::::{stepper}

::::{step} Create the integration and analyze your logs
:anchor: _create_a_new_custom_integration

1. In {{kib}}, find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). You can also start from your solution, for example from **Add integrations** in {{elastic-sec}} or **Add data** in {{observability}}.
2. In the **Can't find an integration?** panel, select **Create integration**.
3. Select the [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md) that Automatic Import uses to analyze your data.
4. In the **Integration Details** section, enter a **Title** and a **Description**. (Optional) Upload a **Logo**.
5. In the **Define data streams and upload logs** section, select **Add Data Stream**. In the **Data Stream** panel, enter a **Data stream title** and a **Data stream description**. Users see them on the integration's configuration page, where they help identify the data stream.
6. Select a [**Data collection method**](beats://reference/filebeat/configuration-filebeat-options.md) to tell {{agent}} how to read the data: File Stream, AWS S3, AWS Cloudwatch, Azure Blob Storage, Azure Event Hub, GCP Pub/Sub, Google Cloud Storage, HTTP Endpoint, Kafka, TCP, or UDP. These methods don't call HTTP APIs. For an HTTP API source, refer to [When to use Automatic Import](/explore-analyze/ai-features/automatic-import.md#automatic-import-when-to-use).
7. In **Logs**, upload your sample or select an existing index.
8. Select **Analyze logs**. The analysis can take several minutes. You can leave the page while it runs and check the status later in **Manage my integrations**.

   To add another data stream, for example for a different type of log from the same source, repeat steps 5–8.

   :::{image} /solutions/images/security-auto-import-data-streams-status.png
   :alt: The New Integration page showing multiple data streams with Analyzing and Success statuses
   :::

When the analysis finishes, each data stream shows **Success** or **Failed**. You can re-analyze or delete a data stream that failed.
::::

::::{step} Review, approve, and install the integration
:anchor: automatic-import-approve

Approving the integration creates a version that you can install and add to an agent policy.

1. In {{kib}}, find **Integrations**, then select **Manage my integrations**.
2. In the integration's row, select **Review & approve**. This option is available only when every data stream shows **Success**.
3. In the **Review and approve data streams** dialog, select at least one **Category**. The category determines where the integration appears on the **Integrations** page.

   :::{image} /solutions/images/auto-import-approve-stream-modal.png
   :alt: The Review and approve data streams modal with a category selector and an Approve button
   :::

4. Review the field mappings and the ingest pipeline. To see a data stream's results, select the data stream in the dialog.

   (Optional) To fine-tune the ingest pipeline, edit it from the data stream's results, then select **Save**. For field-mapping guidance, refer to the [Elastic Common Schema (ECS) field reference](ecs://reference/ecs-field-reference.md). For the ECS fields that {{elastic-sec}} uses, refer to [](/reference/security/fields-and-object-schemas/siem-field-reference.md).

5. To approve the integration without installing it, clear **Automatically install integration after approval**. Then select **Approve**.
6. If you approved the integration without installing it, open the integration's **Actions** menu and select **Install** when you're ready.

The integration's **Approval Status** shows **Approved**. After you install the integration, it appears on the **Integrations** page under the category you selected.
::::

::::{step} Collect data with the integration
:anchor: automatic-import-collect-data

1. On the **Integrations** page, select the integration.
2. If the integration's **Overview** page opens, select **Add <integration>**.
3. Configure the integration and assign it to an [agent policy](/reference/fleet/agent-policy.md).

To confirm that data arrives, search for recent documents from the integration in [Discover](/explore-analyze/discover.md). If you use {{elastic-sec}}, you can also check the health of the integration's ingest pipelines and field mappings in the [Data Quality dashboard](/solutions/security/dashboards/data-quality-dashboard.md).
::::

:::::

## Create an integration in {{stack}} 9.0–9.3 [automatic-import-create-9-0-9-3]
```{applies_to}
stack: ga 9.0-9.3
```

In these versions, you create, install, and deploy an integration in a single flow.

::::{dropdown} Steps for {{stack}} 9.0–9.3
:name: automatic-import-create-9-0-9-3-steps

1. In {{kib}}, find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). You can also use your solution's entry point, such as **Add integrations** in {{elastic-sec}} or **Add data** in {{observability}}.
2. In the **Can't find an integration?** panel, select **Create new integration**.
3. Select **Create integration**.
4. Select an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
5. Define how your new integration appears on the Integrations page by providing a **Title**, **Description**, and **Logo**. Select **Next**.
6. Define your integration's package name, which prefixes the imported event fields.
7. Define your **Data stream title**, **Data stream description**, and **Data stream name**. These fields appear on the integration's configuration page to help identify the data stream it writes to.
8. Select your [**Data collection method**](beats://reference/filebeat/configuration-filebeat-options.md). This determines how your new integration ingests the data (for example, from an S3 bucket, an HTTP endpoint, or a file stream).

   :::{warning}
   CEL generation in Automatic Import is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
   :::

   If you select **API (CEL input)**, upload an OpenAPI specification (OAS) file in JSON or YAML format. This file is separate from the data sample, and the sample formats in [Prepare your sample data](#automatic-import-sample-data) don't apply to it. Automatic Import generates a Common Expression Language (CEL) program from that file. The LLM uses the specification to determine which API endpoints (GET only), query parameters, and data structures to use. Select the endpoints to consume and your authentication method, then upload a sample of the API responses in the next step. For background, refer to the [CEL specification](https://github.com/google/cel-spec) and the [CEL input in {{filebeat}}](beats://reference/filebeat/filebeat-input-cel.md).

9. Upload a sample of your data. Make sure to include all the types of events that you want the new integration to handle.
10. Select **Analyze logs**, then wait for processing to complete. This can take several minutes.
11. After processing is complete, the pipeline's field mappings appear, including ECS and custom fields.

    :::{image} /solutions/images/security-auto-import-review-integration-page.png
    :alt: The Automatic Import Review page showing proposed field mappings
    :::

12. (Optional) After reviewing the proposed pipeline, you can fine-tune it by selecting **Edit pipeline**. Refer to the [{{elastic-sec}} ECS reference](/reference/security/fields-and-object-schemas/siem-field-reference.md) to learn more about formatting field mappings. When you're satisfied with your changes, select **Save**.

    :::{note}
    If your new integration collects data from an API, you can update the [CEL input](beats://reference/filebeat/filebeat-input-cel.md) configuration (program and API authentication information) from the new integration's integration policy.
    :::

    :::{image} /solutions/images/security-auto-import-edit-pipeline.gif
    :alt: An animation showing a user clicking the edit pipeline button and viewing the ingest pipeline flyout
    :::

13. Select **Add to Elastic**. After the **Success** message appears, your new integration is available on the Integrations page.

    :::{image} /solutions/images/security-auto-import-success-message.png
    :alt: The automatic import success message
    :::

14. Select **Add to an agent** to deploy your new integration and start collecting data, or select **View integration** to view detailed information about your new integration.
15. (Optional) After you've added an integration, you can edit the ingest pipeline from the **Ingest Pipelines** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
::::

## Next steps [automatic-import-create-next-steps]

* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` [Manage integrations created with Automatic Import](/explore-analyze/ai-features/automatic-import/manage-integrations.md): Edit the integration or use it on another cluster or project.
* [Create a dashboard](/explore-analyze/dashboards/create-dashboard.md) to visualize the data.
