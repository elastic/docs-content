---
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-file-upload.html
  - https://www.elastic.co/guide/en/kibana/current/connect-to-elasticsearch.html#upload-data-kibana
---

# Upload data files [upload-data-kibana]

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/docs-content/serverless/elasticsearch-ingest-data-file-upload.md
% - [x] ./raw-migrated-files/kibana/kibana/connect-to-elasticsearch.md

% Note from David: I've removed the ID $$$upload-data-kibana$$$ from manage-data/ingest.md as those links should instead point to this page. So, please ensure that the following ID is included on this page. I've added it beside the title.

You can upload files, view their fields and metrics, and optionally import them to {{es}} with the Data Visualizer. 

To use the Data Visualizer, click **Upload a file** on the {{es}} **Getting Started** page or navigate to the **Integrations** view and search for **Upload a file**. Clicking **Upload a file** opens the Data Visualizer UI.

:::{image} /images/serverless-file-uploader-UI.png
:alt: File upload UI
:class: screenshot
:::

Drag a file into the upload area or click **Select or drag and drop a file** to choose a file from your computer.

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

The Data Visualizer displays the first 1000 rows of the file. You can inspect the data and make any necessary changes before importing it. Click **Import** continue the process.

This process will create an index and import the data into {{es}}. Once your data is in {{es}}, you can start exploring it, see [Explore and analyze](/explore-analyze/index.md) for more information.

::::{important}
The upload feature is not intended for use as part of a repeated production process, but rather for the initial exploration of your data.

::::

## Required privileges

The {{stack-security-features}} provide roles and privileges that control which users can upload files. To upload a file in {{kib}} and import it into an {{es}} index, you’ll need:

* `manage_pipeline` or `manage_ingest_pipelines` cluster privilege
* `create`, `create_index`, `manage`, and `read` index privileges for the index
* `all` {{kib}} privileges for **Discover** and **Data Views Management**

You can manage your roles, privileges, and spaces in **{{stack-manage-app}}**.