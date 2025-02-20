---
navigation_title: "Data Quality"
---

# Data Quality dashboard [security-data-quality-dash]


The Data Quality dashboard shows you whether your data is correctly mapped to the [Elastic Common Schema](asciidocalypse://docs/ecs/docs/reference/ecs/index.md) (ECS). Successful [mapping](../../../manage-data/data-store/mapping.md) enables you to search, visualize, and interact with your data throughout {{elastic-sec}}.

:::{image} ../../../images/serverless--dashboards-data-qual-dash.png
:alt: The Data Quality dashboard
:class: screenshot
:::

Use the Data Quality dashboard to:

* Check one or multiple indices for unsuccessful mappings, to help you identify problems (the indices used by {{elastic-sec}} appear by default).
* View the number of documents stored in each of your indices.
* View detailed information about the fields in checked indices.
* Track unsuccessful mappings by creating a case or Markdown report based on data quality results.

::::{admonition} Requirements
:class: note

To use the Data Quality dashboard, you need the appropriate user role with the following privileges for each index you want to check:

* `monitor` or `manage`
* `view_index_metadata` or `manage` (required for the [Get mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-mapping))
* `read` (required for the [Search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search))

::::



## Check indices [data-quality-dash-check-indices]

When you open the dashboard, data does not appear until you select indices to check.

* **Check multiple indices**: To check all indices in the current data view, click **Check all** at the top of the dashboard. A progress indicator will appear.

::::{important}
To customize which indices are checked when you click **Check all**, [change the current data view](../../../solutions/security/get-started/data-views-elastic-security.md).

::::


* **Check a single index**: To check a single index, click the **Check now** button under **Actions**. Checking a single index is faster than checking all indices.


## Visualize checked indices [security-data-quality-dash-visualize-checked-indices]

The treemap that appears at the top of the dashboard shows the relative document count of your indices. The color of each index’s node refers to its status:

* **Blue:** Not yet checked.
* **Green:** Checked, no incompatible fields found.
* **Red:** Checked, one or more incompatible fields found.

Click a node in the treemap to expand the corresponding index.


## Learn more about checked index fields [security-data-quality-dash-learn-more-about-checked-index-fields]

After an index is checked, a `Pass` or `Fail` status appears. `Fail` indicates mapping problems in an index. To view index check details, including which fields weren’t successfully mapped, click the **Check now** button under **Actions**.

:::{image} ../../../images/serverless--dashboards-data-qual-dash-detail.png
:alt: An expanded index with some failed results in the Data Quality dashboard
:class: screenshot
:::

The index check flyout provides more information about the status of fields in that index. Each of its tabs describe fields grouped by mapping status.

::::{note}
Fields in the Same family category have the correct search behavior, but might have different storage or performance characteristics (for example, you can index strings to both text and keyword fields). To learn more, refer to [Field data types](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/field-data-types.md).

::::



## View historical data quality results [security-data-quality-dash-view-historical-data-quality-results]

You can review an index’s data quality history by clicking **View history** under **Actions***, or by clicking the ***History*** tab in the details flyout. You can filter the results by time and ***Pass** / **Fail** status. Click a historical check to expand it and view more details.

:::{image} ../../../images/serverless-history-tab.png
:alt: An index's data quality history tab
:class: screenshot
:::

::::{note}
Recent historical data includes the **Incompatible fields** and **Same family** views. Legacy historical data only includes the **Incompatible fields** view.

::::



## Export data quality results [security-data-quality-dash-export-data-quality-results]

You can share data quality results to help track your team’s remediation efforts. First, follow the instructions under [Check indices](../../../solutions/security/dashboards/data-quality-dashboard.md#data-quality-dash-check-indices) to generate results, then either:

**Export results for all indices in the current data view**:

1. At the top of the dashboard, under the **Check all** button, are two buttons that allow you to share results. Exported results include all the data which appears in the dashboard.
2. Click **Add to new case** to open a new [case](../../../solutions/security/investigate/cases.md).
3. Click **Copy to clipboard** to copy a Markdown report to your clipboard.

**Export results for one index**:

1. View details for a checked index by clicking the **Check now** button under **Actions**.
2. From the **Incompatible fields** tab, select **Add to new case** to open a new [case](../../../solutions/security/investigate/cases.md), or click **Copy to clipboard** to copy a Markdown report to your clipboard.

::::{note}
For more information about how to fix mapping problems, refer to [Mapping](../../../manage-data/data-store/mapping.md).

::::
