---
navigation_title: ML in Kibana
description: Explore your data with the Data Visualizer, and detect distribution changes over time with Data drift, directly in Kibana.
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-ml.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Machine learning in Kibana [xpack-ml]

As data sets increase in size and complexity, the human effort required to inspect dashboards or maintain rules for spotting infrastructure problems, cyber attacks, or business issues becomes impractical. Elastic {{ml-features}} such as {{anomaly-detect}} and {{oldetection}} make it easier to notice suspicious activities with minimal human interference.

{{kib}} includes a free **{{data-viz}}** that helps you understand your data's structure, distribution, and quality before you act on it. If your data is stored in {{es}} and contains a time field, the **{{data-viz}}** also helps you identify possible fields for {{anomaly-detect}}.

::::{tip}
:applies_to: {"stack": "ga 9.4", "serverless": "ga"}
Click **Zoom in** or **Zoom out** next to the date picker to quickly narrow or widen the time range when exploring your data.
::::


:::{image} /explore-analyze/images/kibana-ml-data-visualizer-sample.png
:alt: {{data-viz}} for sample web logs data
:screenshot:
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
* Plain text (TXT)
* Rich text (RTF)
* Open Document Format (ODF)

The **{{data-viz}}** identifies the file format and field mappings, and you can import the data into an {{es}} index. To change the default file size limit, refer to [`fileUpload:maxFileSize`](kibana://reference/advanced-settings.md#kibana-general-settings) in **Advanced Settings**.

If {{stack-security-features}} are enabled, users must have the necessary privileges to use {{ml-features}}. Refer to [Set up {{ml-features}}](setting-up-machine-learning.md#setup-privileges).

::::{note}
There are limitations in {{ml-features}} that affect {{kib}}. For more information, refer to [{{ml-cap}}](anomaly-detection/ml-limitations.md).
::::

## Data drift [data-drift-view]
```{applies_to}
stack: ga 9.4+, preview 9.0-9.3
serverless: ga
```

You can find the **Data drift** view in **{{ml-app}}** → **{{data-viz}}** in {{kib}} or by using the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md). The **Data drift** view shows you the differences in each field for two different time ranges in a given {{data-source}}. The view helps you to visualize the changes in your data over time and enables you to understand its behavior better.

:::{image} /explore-analyze/images/kibana-ml-data-drift.png
:alt: Data drift view in {{kib}}
:screenshot:
:::

You select a {{data-source}} to analyze, along with separate time ranges for the reference and comparison data in the histogram chart, adjusting each range by moving its brush. **Run analysis** then compares the reference and comparison periods.

You can decide whether you want to view all the fields in the {{data-source}} or only the ones that contain drifted data. The analysis results table displays the fields, their types, if drift is detected, the p-value that indicates how significant the detected change is, the reference and comparison distribution, and the comparison chart. To expand the results for a particular field, select its row's arrow icon.
