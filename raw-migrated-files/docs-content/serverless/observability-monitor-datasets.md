---
navigation_title: "Data set quality"
---

# Data set quality monitoring [observability-monitor-datasets]


[beta]

The **Data Set Quality** page provides an overview of your log, metric, trace, and synthetic data sets. Use this information to get an idea of your overall data set quality and find data sets that contain incorrectly parsed documents.

Access the Data Set Quality page from the main menu at **Project settings** → **Management*** → ***Data Set Quality**. By default, the page only shows log data sets. To see other data set types, select them from the **Type** menu.

::::{admonition} Requirements
:class: note

Users with the `viewer` role can view the Data Sets Quality summary. To view the Active Data Sets and Estimated Data summaries, users need the `monitor` [index privilege](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) for the `logs-*-*` index.

::::


The quality of your data sets is based on the percentage of degraded documents in each data set. A degraded document in a data set contains the [`_ignored`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/mapping-ignored-field.md) property because one or more of its fields were ignored during indexing. Fields are ignored for a variety of reasons. For example, when the [`ignore_malformed`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/mapping-ignored-field.md) parameter is set to true, if a document field contains the wrong data type, the malformed field is ignored and the rest of the document is indexed.

From the data set table, you’ll find information for each data set such as its namespace, when the data set was last active, and the percentage of degraded docs. The percentage of degraded documents determines the data set’s quality according to the following scale:

* Good (![Good icon](../../../images/serverless-green-dot-icon.png "")): 0% of the documents in the data set are degraded.
* Degraded (![Degraded icon](../../../images/serverless-yellow-dot-icon.png "")): Greater than 0% and up to 3% of the documents in the data set are degraded.
* Poor (![Poor icon](../../../images/serverless-red-dot-icon.png "")): Greater than 3% of the documents in the data set are degraded.

Opening the details of a specific data set shows the degraded documents history, a summary for the data set, and other details that can help you determine if you need to investigate any issues.


## Investigate issues [observability-monitor-datasets-investigate-issues]

The Data Set Quality page has a couple of different ways to help you find ignored fields and investigate issues. From the data set table, you can open the data set’s details page, and view commonly ignored fields and information about those fields. Open a logs data set in Logs Explorer or other data set types in Discover to find ignored fields in individual documents.


### Find ignored fields in data sets [observability-monitor-datasets-find-ignored-fields-in-data-sets]

To open the details page for a data set with poor or degraded quality and view ignored fields:

1. From the data set table, click ![expand icon](../../../images/serverless-expand.svg "") next to a data set with poor or degraded quality.
2. From the details, scroll down to **Quality issues**.

The **Quality issues** section shows fields that have been ignored, the number of documents that contain ignored fields, and the timestamp of last occurrence of the field being ignored.


### Find ignored fields in individual logs [observability-monitor-datasets-find-ignored-fields-in-individual-logs]

To use Logs Explorer or Discover to find ignored fields in individual logs:

1. Find data sets with degraded documents using the **Degraded Docs** column of the data sets table.
2. Click the percentage in the **Degraded Docs** column to open the data set in Logs Explorer or Discover.

The **Documents** table in Logs Explorer or Discover is automatically filtered to show documents that were not parsed correctly. Under the **actions** column, you’ll find the degraded document icon (![degraded document icon](../../../images/serverless-indexClose.svg "")).

Now that you know which documents contain ignored fields, examine them more closely to find the origin of the issue:

1. Under the **actions** column, click ![expand icon](../../../images/serverless-expand.svg "") to open the document details.
2. Select the **JSON** tab.
3. Scroll towards the end of the JSON to find the `ignored_field_values`.

Here, you’ll find all of the `_ignored` fields in the document and their values, which should provide some clues as to why the fields were ignored.
