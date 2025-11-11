---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/data-quality-dash.html
  - https://www.elastic.co/guide/en/serverless/current/security-data-quality-dash.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Data Quality dashboard

The Data Quality dashboard shows you whether your data is correctly mapped to the [Elastic Common Schema](ecs://reference/index.md) (ECS). Successful [mapping](/manage-data/data-store/mapping.md) enables you to search, visualize, and interact with your data throughout {{elastic-sec}} and {{kib}}.

:::{image} /solutions/images/security-data-qual-dash.png
:alt: The Data Quality dashboard
:screenshot:
:::

Use the Data Quality dashboard to:

* Check one or multiple indices for unsuccessful mappings, to help you identify problems (the indices used by {{elastic-sec}} appear by default).
* View the amount of data and number of documents stored in each of your indices.
* View detailed information about the fields in checked indices.
* Track unsuccessful mappings by creating a case or Markdown report based on data quality results.


::::{note}
* On {{serverless-short}} deployments, index `Size` data is not available.
* The Data Quality dashboard doesn’t show data from cold or frozen [data tiers](/manage-data/lifecycle/data-tiers.md). It also doesn’t display data from remote clusters using cross-cluster search. To view data from another cluster, log in to that cluster’s {{kib}} instance.
::::


::::{admonition} Requirements
To use the Data Quality dashboard, you need at least the following [privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) for each index you want to check:

* `monitor` or `manage` (required for the [Index stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-stats))
* `view_index_metadata` or `manage_ilm` (required for the [Explain lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-explain-lifecycle))
* `view_index_metadata` or `manage` (required for the [Get mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-mapping))
* `read` (required for the [Search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search))

::::



## Check indices [data-quality-dash-check-indices]

Data does not appear in the dashboard until a user selects indices to check.

* **Check multiple indices**: To check all indices in the current data view, click **Check all** at the top of the dashboard. A progress indicator will appear.

::::{important}
To customize which indices are checked when you click **Check all**, [change the current data view](/solutions/security/get-started/data-views-elastic-security.md).
::::


* **Check a single index**: To check a single index, click the **Check now** button under **Actions**. Checking a single index is faster than checking all indices.

Once checked, an index’s data quality results persist indefinitely. You can see when the index was last checked, and generate updated results at any time.

::::{important}
Data quality results are stored in a data stream using the following index pattern: `.kibana-data-quality-dashboard-results-<spaceId>`, where `<spaceId>` is the ID of the active {{kib}} [space](/deploy-manage/manage-spaces.md). For example, results from the default space are stored in: `.kibana-data-quality-dashboard-results-default`.
::::



## Visualize checked indices [_visualize_checked_indices]

The treemap that appears at the top of the dashboard shows the relative size of your indices. The color of each index’s node refers to its status:

* **Blue:** Not yet checked.
* **Green:** Checked, no incompatible fields found.
* **Red:** Checked, one or more incompatible fields found.

Click a node in the treemap to expand the corresponding index.


## Learn more about checked index fields [_learn_more_about_checked_index_fields]

After an index is checked, a **Pass** or **Fail** status appears. **Fail** indicates mapping problems in an index. To view index check details, including which fields weren’t successfully mapped, click the **Check now** button under **Actions**.

:::{image} /solutions/images/security-data-qual-dash-detail.png
:alt: An expanded index with some failed results in the Data Quality dashboard
:screenshot:
:::

The index check flyout provides more information about the status of fields in that index. Each of its tabs describe fields grouped by mapping status.

::::{note}
Fields in the **Same family** category have the correct search behavior, but might have different storage or performance characteristics (for example, you can index strings to both `text` and `keyword` fields). To learn more, refer to [Field data types](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md).
::::



## View historical data quality results [_view_historical_data_quality_results]

You can review an index’s data quality history by clicking **View history** under **Actions**, or by clicking the **History** tab in the details flyout. You can filter the results by time and **Pass** / **Fail** status. Click a historical check to expand it and view more details.

:::{image} /solutions/images/security-data-qual-dash-history.png
:alt: The Data Quality dashboard
:::

::::{note}
Recent historical data includes the **Incompatible fields** and **Same family** views. Legacy historical data only includes the **Incompatible fields** view.
::::



## Export data quality results [_export_data_quality_results]

You can share data quality results to help track your team’s remediation efforts. First, follow the instructions under [Check indices](/solutions/security/dashboards/data-quality-dashboard.md#data-quality-dash-check-indices) to generate results, then either:

* Export results for all indices in the current data view:

    1. At the top of the dashboard, under the **Check all** button, are two buttons that allow you to share results. Exported results include all the data which appears in the dashboard.
    2. Click **Add to new case** to open a new [case](/solutions/security/investigate/cases.md).
    3. Click **Copy to clipboard** to copy a Markdown report to your clipboard.

* Export results for one index:

    1. View details for a checked index by clicking the **Check now** button under **Actions**.
    2. From the **Incompatible fields** tab, select **Add to new case** to open a new [case](/solutions/security/investigate/cases.md).


::::{note}
For more information about how to fix mapping problems, refer to [Mapping](/manage-data/data-store/mapping.md).
::::
