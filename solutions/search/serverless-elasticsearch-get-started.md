---
navigation_title: "Get started on Serverless"
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-connecting-to-es-serverless-endpoint.html
applies:
  serverless:
---

# Get started with {{es}} Serverless [elasticsearch-get-started]

::::{tip}
Not sure whether {{es}} on {{serverless-full}} is the right deployment choice for you?

Check out the following resources to help you decide:
- [What’s different?](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Understand the differences between {{serverless-full}} and other deployment types.
- [Billing](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md): Learn about the billing model for {{es}} on {{serverless-full}}.
::::

## What is {{es-serverless}}? [what-is-elasticsearch-serverless]


{{es-serverless}} is one of the three available project types on [{{serverless-full}}](/deploy-manage/deploy.md).

This project type enables you to use the core functionality of {{es}}: searching, indexing, storing, and analyzing data of all shapes and sizes.

When using {{es}} on {{serverless-full}} you don’t need to worry about managing the infrastructure that keeps {{es}} distributed and available: nodes, shards, and replicas. These resources are completely automated on the serverless platform, which is designed to scale up and down with your workload.

This automation allows you to focus on building your search applications and solutions.

On this page, you will learn how to:

* [Create an {{es-serverless}} project](#elasticsearch-get-started-create-project).
* Get started with {{es}}:

    * [Option 1: Guided index flow](#elasticsearch-follow-guided-index-flow): Follow the step-by-step tutorial provided in the UI to create an index and ingest data.
    * [Option 2: In-product Getting Started guide](#elasticsearch-follow-in-product-getting-started): Use the Getting Started page’s instructions to ingest data and perform your first search.
    * [Option 3: Explore on your own](#elasticsearch-explore-on-your-own): If you’re already familiar with {{es}}, retrieve your connection details, select an ingest method that suits your needs, and start searching.


## Create an {{es-serverless}} project [elasticsearch-get-started-create-project]

Use your {{ecloud}} account to create a fully-managed {{es}} project:

1. Navigate to [cloud.elastic.co](https://cloud.elastic.co?page=docs&placement=docs-body) and create a new account or log in to your existing account.
2. Within **Serverless Projects**, choose **Create project**.
3. Choose the {{es}} project type.
4. Select a **configuration** for your project, based on your use case.

    * **General purpose**: For general search use cases across various data types.
    * **Optimized for Vectors**: For search use cases using vectors and near real-time retrieval.

5. Provide a name for the project and optionally edit the project settings, such as the cloud platform [region](../../deploy-manage/deploy/elastic-cloud/regions.md). Select **Create project** to continue.
6. Once the project is ready, select **Continue**.

::::{tip}
Learn how billing works for your project in [Elasticsearch billing dimensions](../../deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md).

::::


Now your project is ready to start creating indices, adding data, and performing searches. You can choose one of the following options to proceed.


## Option 1: Follow the guided index flow [elasticsearch-follow-guided-index-flow]

Once your project is set up, you’ll be directed to a page where you can create your first index. An index is where documents are stored and organized, making it possible to search and retrieve data.

1. Enter a name for your index.
2. Click **Create my index**. You can also create the index by clicking on **Code** to view and run code through the command line.

    :::{image} ../../images/serverless-get-started-create-an-index.png
    :alt: Create an index.
    :::

3. You’ll be directed to the **Index Management** page. Here, copy and save the following:

    * Elasticsearch URL
    * API key


::::{note}
You won’t be able to view this API key again. If needed you'll need to generate a new one.
::::


The UI provides ready-to-use code examples for ingesting data via the REST API. Choose your preferred tool for making these requests:

* [Console](https://www.elastic.co/guide/en/serverless/current/devtools-run-api-requests-in-the-console.html) in your project’s UI
* Python
* JavaScript
* cURL


## Option 2: Follow the Getting Started guide [elasticsearch-follow-in-product-getting-started]

To get started using the in-product tutorial, navigate to the **Getting Started** page and follow the on-screen steps.

:::{image} ../../images/serverless-getting-started-page.png
:alt: Getting Started page.
:::


## Option 3: Explore on your own [elasticsearch-explore-on-your-own]

If you’re already familiar with Elasticsearch, you can jump right into setting up a connection and ingesting data as per your needs.

1. Retrieve your [connection details](get-started.md).
2. Ingest your data. Elasticsearch provides several methods for ingesting data:

    * [{{es}} API](ingest-for-search.md)
    * [Connector clients](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-integrations-connector-client.html)
    * [File Uploader](../../manage-data/ingest/upload-data-files.md)
    * [{{beats}}](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-beats.html)
    * [{{ls}}](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-logstash.html)
    * [Elastic Open Web Crawler](https://github.com/elastic/crawler)



## Next steps [elasticsearch-next-steps]

* Once you’ve added data to your {{es-serverless}} project, you can use [Playground](rag/playground.md) to test and tweak {{es}} queries and chat with your data, using GenAI.
* You can also try our hands-on [quick start tutorials](https://www.elastic.co/guide/en/elasticsearch/reference/current/quickstart.html#quickstart-list) in the core {{es}} documentation.
