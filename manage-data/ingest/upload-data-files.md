---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-file-upload.html
  - https://www.elastic.co/guide/en/kibana/current/connect-to-elasticsearch.html#upload-data-kibana
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: kibana
---

# Upload data files [upload-data-kibana]

You can upload files, analyze their fields and metrics, and import their data into an {{es}} index using the Data Visualizer.

1. Open the **Integrations** page using the global search field, then search for **Upload a file** using the integrations search field.

2. Click **Upload a file** to open the Data Visualizer UI.

3. Depending on your version and deployment:

    ::::{applies-switch}

    :::{applies-item} stack: ga 9.0.0-9.1.8

    1. Drag a file into the upload area or click **Select or drag and drop a file** to choose a file from your computer.

        You can upload different file formats for analysis with the Data Visualizer.

        The supported file formats are:
          * CSV, TSV, NDJSON, log files (up to 500 MB)
          * PDF, TXT, RTF, ODF, Microsoft Office files (up to 60 MB)

        After you upload a file, you can inspect its data and make any necessary changes before importing it.

    2. Click **Import**.

    3. Enter a name for the index where the data will be stored, then click **Import** again to complete the process.

    :::

    :::{applies-item} stack: ga 9.2

    1. Choose whether to import the data to a new index or to an existing one.
    2. Enter a name for the new index or select an existing index from the dropdown.
    3. Drag one or more files into the upload area or click **Select or drag and drop a file** to choose files from your computer.

       The supported file formats are PDF, TXT, CSV, log files and NDJSON.

       After you upload your files, you can inspect the data and make any necessary changes before importing it.

    4. Click **Import** to complete the process.

    :::

    :::{applies-item} serverless: ga

    1. Choose whether to import the data to a new index or to an existing one.
    2. Enter a name for the new index or select an existing index from the dropdown.
    3. Drag one or more files into the upload area or click **Select or drag and drop a file** to choose files from your computer.

       The supported file formats are PDF, TXT, CSV, log files and NDJSON.

       After you upload your files, you can inspect the data and make any necessary changes before importing it.

    4. Click **Import** to complete the process.

    :::

    ::::

After the uploaded data is imported into the specified {{es}} index, you can start exploring it. For more details, refer to [Explore and analyze](/explore-analyze/index.md).

::::{important}
The upload feature is not intended for use as part of a repeated production process, but rather for the initial exploration of your data.

::::

## Required privileges

The {{stack-security-features}} provide roles and privileges that control which users can upload files. To upload a file in {{kib}} and import it into an {{es}} index, you’ll need:

* `manage_pipeline` or `manage_ingest_pipelines` cluster privilege
* `create`, `create_index`, `manage`, and `read` index privileges for the index
* `all` {{kib}} privileges for **Discover** and **Data Views Management**

You can manage your roles, privileges, and spaces in **{{stack-manage-app}}**.