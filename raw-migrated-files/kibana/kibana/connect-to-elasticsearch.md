# Add data [connect-to-elasticsearch]

The best way to add data to the Elastic Stack is to use one of our many integrations, which are pre-packaged assets that are available for a wide array of popular services and platforms. With integrations, you can add monitoring for logs and metrics, protect systems from security threats, and more.

All integrations are available in a single view on the **Integrations** page.

:::{image} ../../../images/kibana-add-integration.png
:alt: Integrations page from which you can choose integrations to start collecting and analyzing data
:class: screenshot
:::

::::{note}
When an integration is available for both [Elastic Agent and Beats](../../../manage-data/ingest/tools.md), the **Integrations** view defaults to the Elastic Agent integration, if it is generally available (GA). To show a Beats integration, use the filter below the side navigation.
::::



## Add data with Elastic solutions [_add_data_with_elastic_solutions]

A good place to start is with one of our Elastic solutions, which offer experiences for common use cases.

* **Elastic connectors and crawler.**

    * Create searchable mirrors of your data in Sharepoint Online, S3, Google Drive, and many other web services using our open code [Elastic connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors.html).
    * Discover, extract, and index your web content into {{es}} using the [Elastic web crawler](https://www.elastic.co/guide/en/enterprise-search/current/crawler.html).

* **Elastic Observability.** Get logs, metrics, traces, and uptime data into the Elastic Stack. Integrations are available for popular services and platforms, such as Nginx, AWS, and MongoDB, and generic input types like log files. Refer to [Elastic Observability](../../../solutions/observability/get-started/what-is-elastic-observability.md) for more information.
* **Endpoint Security.** Protect your hosts and send logs, metrics, and endpoint security data to Elastic Security. Refer to [Ingest data to Elastic Security](../../../solutions/security/get-started/ingest-data-to-elastic-security.md) for more information.


## Add data with programming languages [_add_data_with_programming_languages]

Add any data to the Elastic Stack using a programming language, such as JavaScript, Java, Python, and Ruby. Details for each programming language library that Elastic provides are in the [{{es}} Client documentation](https://www.elastic.co/guide/en/elasticsearch/client/index.html).

If you are running {{kib}} on our hosted {{es}} Service, click **Connection details** on the **Integrations** view to verify your {{es}} endpoint and Cloud ID, and create API keys for integration. Alternatively, the **Connection details** are also accessible through the top bar help menu.


## Add sample data [_add_sample_data]

Sample data sets come with sample visualizations, dashboards, and more to help you explore {{kib}} before you add your own data. In the **Integrations** view, search for **Sample Data**, and then add the type of data you want.

:::{image} ../../../images/kibana-add-sample-data.png
:alt: eCommerce
:class: screenshot
:::


## Upload a data file [upload-data-kibana]

You can upload files, view their fields and metrics, and optionally import them to {{es}} with the Data Visualizer. In the **Integrations** view, search for **Upload a file**, and then drop your file on the target.

You can upload different file formats for analysis with the Data Visualizer:

File formats supported up to 500 MB:

* CSV
* TSV
* NDJSON
* Log files

File formats supported up to 60 MB:

* PDF
* Microsoft Office files (Word, Excel, PowerPoint)
* Plain Text (TXT)
* Rich Text (RTF)
* Open Document Format (ODF)

::::{note}
The upload feature is not intended for use as part of a repeated production process, but rather for the initial exploration of your data.
::::


:::{image} ../../../images/kibana-add-data-fv.png
:alt: Uploading a file in {{kib}}
:class: screenshot
:::

The {{stack-security-features}} provide roles and privileges that control which users can upload files. To upload a file in {{kib}} and import it into an {{es}} index, you’ll need:

* `manage_pipeline` or `manage_ingest_pipelines` cluster privilege
* `create`, `create_index`, `manage`, and `read` index privileges for the index
* `all` {{kib}} privileges for **Discover** and **Data Views Management**

You can manage your roles, privileges, and spaces in **{{stack-manage-app}}**.


## What’s next? [_whats_next_3]

To take your investigation to a deeper level, use [**Discover**](../../../explore-analyze/discover.md) and quickly gain insight to your data: search and filter your data, get information about the structure of the fields, and analyze your findings in a visualization.
