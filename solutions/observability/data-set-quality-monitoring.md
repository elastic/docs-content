---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-datasets.html
  - https://www.elastic.co/guide/en/serverless/current/observability-monitor-datasets.html
applies_to:
  stack: beta
  serverless: beta
navigation_title: "Data set quality"
applies_to:
  stack: beta
  serverless: beta
---

# Data set quality monitoring [observability-monitor-datasets]

::::{note}:

**Required roles and privileges**

With the `viewer` role, users can view the Data Sets Quality summary.

You need the `monitor` [index privilege](../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) for the `logs-*-*` index to view the Active Data Sets and Estimated Data summaries on the Data set quality page.
::::

The **Data Set Quality** page provides an overview of your log, metric, trace, and synthetic data sets. Use this information to get an idea of your overall data set quality and find data sets that contain incorrectly parsed documents.

To open **Data Set Quality**, find **Stack Management** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). By default, the page only shows log data sets. To see other data set types, select them from the **Type** menu.

The quality of your data sets is based on the percentage of degraded documents in each data set. A degraded document in a data set contains the [`_ignored`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-ignored-field.md) property because one or more of its fields were ignored during indexing. Fields are ignored for a variety of reasons. For example, when the [`ignore_malformed`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-ignored-field.md) parameter is set to true, if a document field contains the wrong data type, the malformed field is ignored and the rest of the document is indexed.

From the data set table, you’ll find information for each data set such as its namespace, when the data set was last active, and the percentage of degraded docs. The percentage of degraded documents determines the data set’s quality according to the following scale:

* Good (![Good icon](/solutions/images/serverless-green-dot-icon.png "")): 0% of the documents in the data set are degraded.
* Degraded (![Degraded icon](/solutions/images/serverless-yellow-dot-icon.png "")): Greater than 0% and up to 3% of the documents in the data set are degraded.
* Poor (![Poor icon](/solutions/images/serverless-red-dot-icon.png "")): Greater than 3% of the documents in the data set are degraded.

Opening the details of a specific data set shows the degraded documents history, a summary for the data set, and other details that can help you determine if you need to investigate any issues.

## Investigate issues [observability-monitor-datasets-investigate-issues]

The Data Set Quality page provides several ways to help you investigate issues. From the data set table, you can open the data set’s details page, open failed docs sent to the failure store in Discover, and view ignored fields.

### Failure store

::::{note}:

**Required privileges**

You need the `read_failure_store` or `all` [index privilege](../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) to access failure store.

::::

To help diagnose issues with ingestion or mapping, documents that are rejected during ingestion are sent to a dedicated data stream called failure store. From the Data Set Quality page, data streams with documents in the failure store will show a percentage in the **Failed docs (%)**. The failed docs percentage gives you a quick overview of the magnitude of potential problems in your ingestion process.

Select the percentage for a specific data stream to open Discover and see the raw documents that were sent to failure store.

% screenshot.

To diagnose issues in a specific data stream:
1. Select the data set name from the main table.
1. Open **failed documents**.

% screenshot

### Find ignored fields in data sets [observability-monitor-datasets-find-ignored-fields-in-data-sets]

To open the details page for a data set with poor or degraded quality and view ignored fields and failed documents:

1. From the data set table, select a data set name.
2. Scroll down to **Quality issues**.

The **Quality issues** section shows fields that have been ignored, the number of documents that contain ignored fields, the timestamp of last occurrence of the field being ignored, and failed documents.

% Screenshot

### Find ignored fields in individual logs [observability-monitor-datasets-find-ignored-fields-in-individual-logs]

To use Discover to find ignored fields in individual logs:

1. From the Data Set Quality page, use the **Degraded Docs** column to find data sets with degraded documents.
2. Select the percentage in the **Degraded Docs** column to open the data set in Discover.

The **Documents** table in Discover is automatically filtered to show documents that were not parsed correctly. You’ll find the degraded document icon (![degraded document icon](/solutions/images/serverless-indexClose.svg "")) next to documents that weren't parsed correctly. You can also go directly to Discover and look for this icon to find documents that weren't parsed correctly.

Now that you know which documents contain ignored fields, examine them more closely to find the origin of the issue:

1. Under the **actions** column, click ![expand icon](/solutions/images/serverless-expand.svg "") to open the document details.
2. Select the **JSON** tab.
3. Scroll towards the end of the JSON to find the `ignored_field_values`.

Here, you’ll find all of the `_ignored` fields in the document and their values, which should provide some clues as to why the fields were ignored.