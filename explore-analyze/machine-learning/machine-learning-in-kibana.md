---
applies_to:
  stack: ga
  serverless: ga
navigation_title: ML in Kibana
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-ml.html
---

# Machine learning in Kibana [xpack-ml]

As data sets increase in size and complexity, the human effort required to inspect dashboards or maintain rules for spotting infrastructure problems, cyber attacks, or business issues becomes impractical. Elastic {{ml-features}} such as {{anomaly-detect}} and {{oldetection}} make it easier to notice suspicious activities with minimal human interference.

{{kib}} includes a free **{{data-viz}}** to learn more about your data. In particular, if your data is stored in {{es}} and contains a time field, you can use the **{{data-viz}}** to identify possible fields for {{anomaly-detect}}:

:::{image} ../../images/kibana-ml-data-visualizer-sample.png
:alt: {{data-viz}} for sample flight data
:class: screenshot
:::

You can upload different file formats for analysis with the **{{data-viz}}**.

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

The **{{data-viz}}** identifies the file format and field mappings, and you can import the data into an {{es}} index. To change the default file size limit, see [`fileUpload:maxFileSize`](kibana://reference/advanced-settings.md#kibana-general-settings) in advanced settings.

If {{stack-security-features}} are enabled, users must have the necessary privileges to use {{ml-features}}. Refer to [Set up {{ml-features}}](setting-up-machine-learning.md#setup-privileges).

::::{note}
There are limitations in {{ml-features}} that affect {{kib}}. For more information, refer to [{{ml-cap}}](anomaly-detection/ml-limitations.md).
::::

## Data drift [data-drift-view]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

You can find the data drift view in **{{ml-app}}** > **{{data-viz}}** in {{kib}} or by using the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md). The data drift view shows you the differences in each field for two different time ranges in a given {{data-source}}. The view helps you to visualize the changes in your data over time and enables you to understand its behavior better.

:::{image} ../../images/kibana-ml-data-drift.png
:alt: Data drift view in {{kib}}
:class: screenshot
:::

Select a {{data-source}} that you want to analyze, then select a time range for the reference and the comparison data in the appearing histogram chart. You can adjust the time range for both the reference and the comparison data by moving the respective brushes. When you finished setting the time ranges, click **Run analysis**.

You can decide whether you want to see all the fields in the {{data-source}} or only the ones that contains drifted data. The analysis results table displays the fields, their types, if drift is detected, the p-value that indicates how significant the detected change is, the reference and comparison distribution, and the comparison chart. You can expand the results for a particular field by clicking the arrow icon at the beginning of the field’s row.
