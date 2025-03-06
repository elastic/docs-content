# Upload a file [elasticsearch-ingest-data-file-upload]

You can upload files to {{es}} using the File Uploader. Use the visualizer to inspect the data before importing it.

You can upload different file formats for analysis:

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


## How to upload a file [elasticsearch-ingest-data-file-upload-how-to-upload-a-file]

You’ll find a link to the Data Visualizer on the {{es}} **Getting Started** page.

:::{image} ../../../images/serverless-file-data-visualizer-homepage-link.png
:alt: data visualizer link
:class: screenshot
:::

Clicking **Upload a file** opens the Data Visualizer UI.

:::{image} ../../../images/serverless-file-uploader-UI.png
:alt: File upload UI
:class: screenshot
:::

Drag a file into the upload area or click **Select or drag and drop a file** to choose a file from your computer.

The file is uploaded and analyzed. The Data Visualizer displays the first 1000 rows of the file. You can inspect the data and make any necessary changes before importing it. Click **Import** continue the process.

On the next screen, give your index a name and click **Import**.

This process will create an index and import the data into {{es}}. Once your data is in {{es}}, you can start exploring it, see [Explore your data](../../../explore-analyze/index.md) for more information.

::::{important}
The upload feature is not intended for use as part of a repeated production process, but rather for the initial exploration of your data.

::::
