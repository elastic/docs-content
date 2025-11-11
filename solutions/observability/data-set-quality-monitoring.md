---
navigation_title: Data set quality
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-datasets.html
  - https://www.elastic.co/guide/en/serverless/current/observability-monitor-datasets.html
applies_to:
  stack: beta
  serverless: beta
products:
  - id: observability
  - id: cloud-serverless
---

# Data set quality [observability-monitor-datasets]

The **Data Set Quality** page provides an overview of your log, metric, trace, and synthetic data sets. You can then use this information to get an idea of your overall data set quality and find data sets that contain incorrectly parsed documents.

To open the **Data Set Quality** management page, find it in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

By default, the page only shows log data sets. To see other data set types, select them from the **Type** menu.

## Required roles and privileges

Users with the `viewer` [role](elasticsearch://reference/elasticsearch/roles.md) can only view the **Data Set Quality** summary. To view the **Active Data Sets** and **Estimated Data** summaries, you need the `monitor` [index privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) for the `logs-*-*` index.

## Monitor data sets

The quality of your data sets is based on the percentage of degraded documents in each data set. A degraded document in a data set contains the [`_ignored`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-ignored-field.md) property because one or more of its fields were ignored during indexing. Fields are ignored for a variety of reasons. For example, when the [`ignore_malformed`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-ignored-field.md) parameter is set to true, if a document field contains the wrong data type, the malformed field is ignored and the rest of the document is indexed.

From the data set table, you’ll find information for each data set such as its namespace, when the data set was last active, and the percentage of degraded docs. The percentage of degraded documents determines the data set’s quality according to the following scale:

* Good (![Good icon](/solutions/images/serverless-green-dot-icon.png "")): 0% of the documents in the data set are degraded.
* Degraded (![Degraded icon](/solutions/images/serverless-yellow-dot-icon.png "")): Greater than 0% and up to 3% of the documents in the data set are degraded.
* Poor (![Poor icon](/solutions/images/serverless-red-dot-icon.png "")): Greater than 3% of the documents in the data set are degraded.

Opening the details of a specific data set shows the degraded documents history, a summary for the data set, and other details that can help you determine if you need to investigate any issues.

## Investigate issues [observability-monitor-datasets-investigate-issues]

The Data Set Quality page provides several ways to help you investigate issues. From the data set table, you can open the data set’s details page, open failed docs sent to the failure store in Discover (serverless only), and view ignored fields.

### Find failed documents with failure store
```{applies_to}
serverless: ga
```

To help diagnose issues with ingestion or mapping, documents that are rejected during ingestion are sent to a dedicated data stream called failure store. On the **Data Set Quality** page, data streams with documents in the failure store will show a percentage in the **Failed docs (%)** column. The failed docs percentage gives you a quick look at the magnitude of potential problems in your ingestion process.

#### Required privileges

Accessing failure store requires the `read_failure_store` or `all` [index privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices).

#### Find failed documents

Select the percentage in the **Failed docs (%)** column for a specific data stream to open Discover and see the raw documents that were sent to failure store.

To understand how persistent an issue is, refer to **Document trends** for the number of failed documents over a selected time range:

1. Select the data set name from the main table.
1. Select the **Failed docs** tab under **Document trends**.

To help diagnose what's causing an issue, refer to **Quality issues** for error messages and failure types related to your documents:

1. From the data set table, select a data set name.
1. Scroll down to **Quality issues**.
1. Click the expand icon to open a summary of why your document failed.

### Find ignored fields in data sets [observability-monitor-datasets-find-ignored-fields-in-data-sets]

To open the details page for a data set with poor or degraded quality and view ignored fields and failed documents:

1. From the data set table, select a data set name.
1. Scroll down to **Quality issues**.

The **Quality issues** section shows fields that have been ignored, the number of documents that contain ignored fields, the timestamp of last occurrence of the field being ignored, and failed documents (serverless only).

### Find ignored fields in individual logs [observability-monitor-datasets-find-ignored-fields-in-individual-logs]

To use Discover to find ignored fields in individual logs:

1. From the Data Set Quality page, use the **Degraded Docs** column to find data sets with degraded documents.
1. Select the percentage in the **Degraded Docs** column to open the data set in Discover.

The **Documents** table in Discover is automatically filtered to show documents that were not parsed correctly. You’ll find the degraded document icon (![degraded document icon](/solutions/images/serverless-indexClose.svg "")) next to documents that weren't parsed correctly. You can also go directly to Discover and look for this icon to find documents that weren't parsed correctly.

Now that you know which documents contain ignored fields, examine them more closely to find the origin of the issue:

1. Under the **actions** column, click ![expand icon](/solutions/images/serverless-expand.svg "") to open the document details.
1. Select the **JSON** tab.
1. Scroll towards the end of the JSON to find the `ignored_field_values`.

Here, you’ll find all of the `_ignored` fields in the document and their values, which should provide some clues as to why the fields were ignored.