---
navigation_title: Automatic Import
description: Use Automatic Import with an LLM to build a custom Elastic integration from a data sample when no prebuilt integration exists, for Security, Observability, and other solutions.
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/automatic-import.html
  - https://www.elastic.co/guide/en/serverless/current/security-automatic-import.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: security
  - id: observability
---

# Automatic Import [automatic-import]

:::{include} /explore-analyze/_snippets/automatic-import-intro.md
:::

## Requirements [automatic-import-requirements]

* A working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
* {{stack}} users: An [Enterprise](https://www.elastic.co/pricing) subscription.
* {{serverless-short}} **{{sec-serverless}}** projects: the [Security Analytics Complete](/deploy-manage/deploy/elastic-cloud/project-settings.md#elastic-sec-project-features) feature tier.
* {{serverless-short}} **{{obs-serverless}}** projects: the [Observability Complete](/deploy-manage/deploy/elastic-cloud/project-settings.md#obs-serverless-project-features) feature tier.
* A sample of the data you want to import.


## Prepare your sample data [automatic-import-sample-data]

To use Automatic Import, you must provide a sample of the data you want to import. An LLM processes that sample and creates an integration suitable for the data represented by the sample. **Automatic Import supports the following sample formats: JSON, NDJSON, CSV, and syslog (structured and unstructured).**

{applies_to}`stack: removed 9.4` For API-based collection, Automatic Import can generate a program in **Common Expression Language (CEL)**. For background, refer to the [CEL specification](https://github.com/google/cel-spec){:target="_blank"} and the [CEL input in {{filebeat}}](beats://reference/filebeat/filebeat-input-cel.md).

* You can upload a sample of any size. The LLM detects its format and selects up to 1000 documents for detailed analysis.

  :::{note}
  :applies_to: stack: ga 9.0-9.3
  The LLM selects up to 100 documents for detailed analysis, not 1000.
  :::

* The more variety in your sample, the more accurate the pipeline is. For best results, include a wide range of unique log entries in your sample instead of repeating similar logs.
* When you upload a CSV, a header with column names is automatically recognized. If the header is not present, the LLM attempts to create descriptive field names based on field formats and values.
* For JSON and NDJSON samples, each object in your sample should represent an event. Avoid deeply nested object structures.
* {applies_to}`stack: removed 9.4` When you select **`API (CEL input)`** as one of the sources, you’re prompted to provide the associated OpenAPI specification (OAS) file to generate a CEL program that consumes this API.

::::{warning}
:applies_to: stack: removed 9.4
CEL generation in Automatic Import is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


## Recommended models [automatic-import-recommended-models]

You can use Automatic Import with any LLM. Model performance varies. Model performance for Automatic Import is similar to model performance for Attack Discovery: models that perform well for Attack Discovery perform well for Automatic Import. Refer to the [large language model performance matrix for {{elastic-sec}}](/solutions/security/ai/large-language-model-performance-matrix.md). For {{observability}} workloads, refer to the [LLM performance matrix for {{observability}}](/solutions/observability/ai/llm-performance-matrix.md).

::::{important}
Using Automatic Import allows users to create new third-party data integrations through the use of third-party generative AI models (“GAI models”). Any third-party GAI models that you choose to use are owned and operated by their respective providers. Elastic does not own or control these third-party GAI models, nor does it influence their design, training, or data-handling practices. Using third-party GAI models with Elastic solutions, and using your data with third-party GAI models is at your discretion. Elastic bears no responsibility or liability for the content, operation, or use of these third-party GAI models, nor for any potential loss or damage arising from their use. Users are advised to exercise caution when using GAI models with personal, sensitive, or confidential information, as data submitted can be used to train the models or for other purposes. Elastic recommends familiarizing yourself with the development practices and terms of use of any third-party GAI models before use. You are responsible for ensuring that your use of Automatic Import complies with the terms and conditions of any third-party platform you connect with.
::::



## Create a new custom integration [_create_a_new_custom_integration]

The integration creation flow changed in {{stack}} 9.4 to support multiple data streams per integration and a new approve-then-install workflow. {{serverless-short}} already uses the updated flow.

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.4+", "serverless": "ga" }

1. In {{kib}}, open **Integrations**. You can use the main menu, the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), or your solution's entry point (for example, **Add integrations** in {{elastic-sec}}, or **Add data** in {{observability}}).
2. Under **Can't find an integration?** click **Create integration**.

   :::{image} /solutions/images/security-auto-import-create-new-integration-button.png
   :alt: The Integrations page with the Create integration button highlighted
   :::

3. Select an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md) in the top right.
4. Under **Integration Details**, provide a **Title** (required), **Description** (required), and **Logo** (optional).

   :::{image} /solutions/images/security-auto-import-new-integration-form.png
   :alt: The New Integration page showing Integration Details fields and an Add Data Stream button
   :::

5. Under **Define data streams and upload logs**, click **Add Data Stream**. You can add multiple data streams to a single integration.
6. In the **Data Stream** panel, provide a **Data stream title** and **Data stream description**. These fields appear on the integration's configuration page to help identify the data stream it writes to.

   :::{image} /solutions/images/security-auto-import-data-stream-flyout.png
   :alt: The Data Stream panel with fields for title, description, data collection method, and sample logs
   :::

7. Select a [**Data collection method**](beats://reference/filebeat/configuration-filebeat-options.md) to determine how the integration ingests the data. Supported methods: 

   - File Stream
   - AWS S3
   - AWS Cloudwatch
   - Azure Blog Storage
   - Azure Event Hub
   - GCP Pub/Sub
   - Google Cloud Storage
   - HTTP Endpoint
   - Kafka
   - TCP 
   - UDP

8. Under **Logs**, either upload a sample of your data or select an existing index. Only indexes that include the `event.original` field are supported. Make sure your sample includes all the types of events that you want the integration to handle.
9. Click **Analyze logs** and wait for processing to complete. This can take several minutes. The data stream(s) continue to process as shown by the status on the **Manage my integrations** menu, so you can navigate away and come back later.

   :::{note}
   The **Manage my integrations** menu lists only integrations created with Automatic Import on versions 9.4+. 
   
   Manually created custom integration `.zip`s  get installed from the **Installed integrations** tab and aren't tracked on the **Manage my integrations** menu. For more information about user-created custom integrations, refer to [Upload a new integration](https://www.elastic.co/docs/extend/integrations/upload-new-integration).
   :::

   :::{image} /solutions/images/security-auto-import-data-streams-status.png
   :alt: The New Integration page showing multiple data streams with Analyzing and Success statuses
   :::

10. When all data streams reach a **Success** status, the integration is ready to approve.

    :::{image} /solutions/images/security-auto-import-manage-integrations-row.png
    :alt: The Manage my integrations view showing a custom integration with a Ready to approve status
    :::

11. From the integration's **Actions** menu, click **Review & approve**. Select a category to help identify the integration on the Integrations page, then review the field mappings and the ingest pipeline.

    :::{image} /solutions/images/auto-import-approve-stream-modal.png
    :alt: The Review and approve data streams modal with a category selector and an Approve button
    :::

    Integration versions automatically increase when more data streams are added after the integration is approved.

    (Optional) To fine-tune the ingest pipeline, open it from the **Review & approve** panel and make your changes. Refer to the [{{elastic-sec}} ECS reference](/reference/security/fields-and-object-schemas/siem-field-reference.md) for field-mapping guidance. Click **Save** when you're done.

12. When you approve an integration, by default it's also installed, which makes it available for assignment to a policy. To approve an integration without installing it, turn off the automatic installation option on its approval confirmation popup. Then, to install it later, click **Install** on the **Actions** menu. 


13. Once you've installed an integration, you can find it using its category.

    :::{image} /solutions/images/security-auto-import-find-integration.png
    :alt: The Integrations catalog showing a newly installed custom integration under its chosen category
    :::

14. Click **Add** to start collecting data and assign the integration to an [agent policy](/reference/fleet/agent-policy.md).

    :::{image} /solutions/images/security-auto-import-add-integration.png
    :alt: The integration details page with an Add button to deploy the integration to an agent policy
    :::

15. (Optional) After you've added an integration, you can edit the ingest pipeline from the **Ingest Pipelines** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::

::::{applies-item} stack: ga 9.0-9.3

1. In {{kib}}, open **Integrations**. You can use the main menu, the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), or your solution's entry point (for example, **Add integrations** in {{elastic-sec}}, or **Add data** in {{observability}}).
2. Under **Can't find an integration?** click **Create new integration**.
3. Click **Create integration**.
4. Select an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
5. Define how your new integration appears on the Integrations page by providing a **Title**, **Description**, and **Logo**. Click **Next**.
6. Define your integration's package name, which prefixes the imported event fields.
7. Define your **Data stream title**, **Data stream description**, and **Data stream name**. These fields appear on the integration's configuration page to help identify the data stream it writes to.
8. Select your [**Data collection method**](beats://reference/filebeat/configuration-filebeat-options.md). This determines how your new integration ingests the data (for example, from an S3 bucket, an HTTP endpoint, or a file stream).

   :::{note}
   If you select **API (CEL input)** ([Common Expression Language](https://github.com/google/cel-spec) via the [CEL input in {{filebeat}}](beats://reference/filebeat/filebeat-input-cel.md)), you have the additional option to upload the API's OAS file here. After you do, the LLM uses it to determine which API endpoints (GET only), query parameters, and data structures to use in the new custom integration. You then select which API endpoints to consume and your authentication method before uploading your sample data.
   :::

9. Upload a sample of your data. Make sure to include all the types of events that you want the new integration to handle.
10. Click **Analyze logs**, then wait for processing to complete. This may take several minutes.
11. After processing is complete, the pipeline's field mappings appear, including ECS and custom fields.

    :::{image} /solutions/images/security-auto-import-review-integration-page.png
    :alt: The Automatic Import Review page showing proposed field mappings
    :::

12. (Optional) After reviewing the proposed pipeline, you can fine-tune it by clicking **Edit pipeline**. Refer to the [{{elastic-sec}} ECS reference](/reference/security/fields-and-object-schemas/siem-field-reference.md) to learn more about formatting field mappings. When you're satisfied with your changes, click **Save**.

    :::{note}
    If your new integration collects data from an API, you can update the [CEL input](beats://reference/filebeat/filebeat-input-cel.md) configuration (program and API authentication information) from the new integration's integration policy.
    :::

    :::{image} /solutions/images/security-auto-import-edit-pipeline.gif
    :alt: An animation showing a user clicking the edit pipeline button and viewing the ingest pipeline flyout
    :::

13. Click **Add to Elastic**. After the **Success** message appears, your new integration is available on the Integrations page.

    :::{image} /solutions/images/security-auto-import-success-message.png
    :alt: The automatic import success message
    :::

14. Click **Add to an agent** to deploy your new integration and start collecting data, or click **View integration** to view detailed information about your new integration.
15. (Optional) After you've added an integration, you can edit the ingest pipeline from the **Ingest Pipelines** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::

:::::

::::{tip}
If you use {{elastic-sec}}, you can use the [Data Quality dashboard](/solutions/security/dashboards/data-quality-dashboard.md) to check the health of your data ingest pipelines and field mappings.
::::
