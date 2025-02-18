---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/automatic-import.html
  - https://www.elastic.co/guide/en/serverless/current/security-automatic-import.html
---

# Automatic import

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/automatic-import.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-automatic-import.md

::::{warning}
This feature is in technical preview. It may change in the future, and you should exercise caution when using it in production environments. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of GA features.
::::


Automatic Import helps you quickly parse, ingest, and create [ECS mappings](https://www.elastic.co/elasticsearch/common-schema) for data from sources that don’t yet have prebuilt Elastic integrations. This can accelerate your migration to {{elastic-sec}}, and help you quickly add new data sources to an existing SIEM solution in {{elastic-sec}}. Automatic Import uses a large language model (LLM) with specialized instructions to quickly analyze your source data and create a custom integration.

While Elastic has 400+ [prebuilt data integrations](https://docs.elastic.co/en/integrations), Automatic Import helps you extend data coverage to other security-relevant technologies and applications. Elastic integrations (including those created by Automatic Import) normalize data to [the Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current/ecs-reference.html), which creates uniformity across dashboards, search, alerts, machine learning, and more.

::::{tip}
Click [here](https://elastic.navattic.com/automatic-import) to access an interactive demo that shows the feature in action, before setting it up yourself.
::::


::::{admonition} Requirements
* A working [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md). Recommended models: `Claude 3.5 Sonnet`; `GPT-4o`; `Gemini-1.5-pro-002`.
* An [Enterprise](https://www.elastic.co/pricing) subscription.
* A sample of the data you want to import, in a structured or unstructured format (including JSON, NDJSON, and Syslog).
* To import data from a REST API, have its OpenAPI specification (OAS) file ready.

::::


::::{important}
Using Automatic Import allows users to create new third-party data integrations through the use of third-party generative AI models (“GAI models”). Any third-party GAI models that you choose to use are owned and operated by their respective providers. Elastic does not own or control these third-party GAI models, nor does it influence their design, training, or data-handling practices. Using third-party GAI models with Elastic solutions, and using your data with third-party GAI models is at your discretion. Elastic bears no responsibility or liability for the content, operation, or use of these third-party GAI models, nor for any potential loss or damage arising from their use. Users are advised to exercise caution when using GAI models with personal, sensitive, or confidential information, as data submitted may be used to train the models or for other purposes. Elastic recommends familiarizing yourself with the development practices and terms of use of any third-party GAI models before use. You are responsible for ensuring that your use of Automatic Import complies with the terms and conditions of any third-party platform you connect with.
::::



## Create a new custom integration [_create_a_new_custom_integration]

1. In {{elastic-sec}}, click **Add integrations**.
2. Under **Can’t find an integration?** click **Create new integration**.

    :::{image} ../../../images/security-auto-import-create-new-integration-button.png
    :alt: The Integrations page with the Create new integration button highlighted
    :::

3. Click **Create integration**.
4. Select an [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md).
5. Define how your new integration will appear on the Integrations page by providing a **Title**, **Description***, and ***Logo**.  Click **Next**.
6. Define your integration’s package name, which will prefix the imported event fields.
7. Define your **Data stream title**, **Data stream description**, and **Data stream name**. These fields appear on the integration’s configuration page to help identify the data stream it writes to.
8. Select your [**Data collection method**](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-filebeat-options.html). This determines how your new integration will ingest the data (for example, from an S3 bucket, an HTTP endpoint, or a file stream).

    ::::{admonition} Importing CEL data
    :class: note

    If you select **API (CEL input)**, you’ll have the additional option to upload the API’s OAS file here. After you do, the LLM will use it to determine which API endpoints (GET only), query parameters, and data structures to use in the new custom integration. You will then select which API endpoints to consume and your authentication method before uploading your sample data.

    ::::

9. Upload a sample of your data. Make sure to include all the types of events that you want the new integration to handle.

    ::::{admonition} Best practices for sample data
    * For JSON and NDJSON samples, each object in your sample should represent an event, and you should avoid deeply nested object structures.
    * The more variety in your sample, the more accurate the pipeline will be. Include a wide range of unique log entries instead of just repeating the same type of entry. Automatic Import will select up to 100 different events from your sample to use as the basis for the new integration.
    * Ideally, each field name should describe what the field does.

    ::::

10. Click **Analyze logs**, then wait for processing to complete. This may take several minutes.
11. After processing is complete, the pipeline’s field mappings appear, including ECS and custom fields.

    :::{image} ../../../images/security-auto-import-review-integration-page.png
    :alt: The Automatic Import Review page showing proposed field mappings
    :::

12. (Optional) After reviewing the proposed pipeline, you can fine-tune it by clicking **Edit pipeline**. Refer to the [{{elastic-sec}} ECS reference](https://www.elastic.co/guide/en/security/current/siem-field-reference.html) to learn more about formatting field mappings. When you’re satisfied with your changes, click **Save**.

    ::::{admonition} How to edit a CEL program
    :class: note

    If your new integration collects data from an API, you can update the CEL input configuration (program and API authentication information) from the new integration’s integration policy.

    ::::


    :::{image} ../../../images/security-auto-import-edit-pipeline.gif
    :alt: A gif showing the user clicking the edit pipeline button and viewing the ingest pipeline flyout
    :::

13. Click **Add to Elastic**. After the **Success** message appears, your new integration will be available on the Integrations page.

    :::{image} ../../../images/security-auto-import-success-message.png
    :alt: The automatic import success message
    :::

14. Click **Add to an agent** to deploy your new integration and start collecting data, or click **View integration** to view detailed information about your new integration.
15. (Optional) Once you’ve added an integration, you can edit the ingest pipeline by going to **Project Settings → Stack Management → Ingest Pipelines**.

::::{tip}
You can use the [Data Quality dashboard](/solutions/security/dashboards/data-quality-dashboard.md) to check the health of your data ingest pipelines and field mappings.
::::
