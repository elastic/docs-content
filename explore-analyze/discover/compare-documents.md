---
navigation_title: Compare documents
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html#compare-documents-in-discover
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Compare field values across multiple documents in Discover to identify differences, troubleshoot issues, and understand how values change across records.
---

# Compare documents in Discover [compare-documents-in-discover]

Compare multiple documents side by side in **Discover** to identify differences in field values. This feature helps you troubleshoot issues by spotting variations between similar documents, track how values change across records, or identify patterns in your data.

## Compare documents side by side

1. In **Discover**, run your search to display the documents you want to compare.
2. Select the results you want to compare from the **Documents** or **Results** tab. You can select multiple documents by clicking the checkbox next to each one.
3. From the **Selected** menu in the table toolbar, choose **Compare selected**. 
   
   The comparison view opens and shows the selected results next to each other.

4. Compare the values of each field. By default, the first result you selected serves as the reference for displaying differences in the other results:
   
   * When the value remains the same for a given field across all documents, it's displayed in **green**.
   * When the value differs from the reference document, it's displayed in **red**.

   ::::{tip}
   You can change the result used as reference by selecting **Pin for comparison** from the contextual menu of any other result.
   ::::

   ![Comparison view in Discover](/explore-analyze/images/kibana-discover-compare-rows.png "")

5. Optionally, customize the **Comparison settings** to adjust how differences are displayed:
   
   * Choose to not highlight differences at all
   * Show differences more granularly at the line, word, or character level
   * Hide fields where the value matches across all results to focus only on differences

6. Exit the comparison view at any time using the **Exit comparison mode** button at the top of the screen.

## Copy selected documents

After comparing documents, you may want to export the selected results for further analysis or record-keeping.

1. Select the results you want to copy from the table.
2. Open the **Selected** menu in the table toolbar.
3. Choose one of the copy options:
   
   * **Copy selection as text** - Copies the visible fields in a human-readable text format
   * **Copy documents as JSON** - Copies the complete document data in JSON format

The content is copied to your clipboard in the selected format. Only fields that are currently added to the table as columns are included in the text format. The JSON format includes all fields.

:::{tip}
You can also copy the content of a single cell to your clipboard using the quick actions that appear when hovering over the cell.
:::

## Filter to show only selected documents

If you want to temporarily narrow your view to only the documents you've selected:

1. Select the documents you want to focus on.
2. Click the **Selected** menu in the table toolbar.
3. Select **Show selected documents only**.

**Discover** applies a filter to show only those documents. You can remove this filter at any time to return to your full result set.

## Use cases

Document comparison is particularly useful for:

* **Troubleshooting**: Compare error logs to identify patterns or differences in failures
* **Configuration analysis**: Check how settings vary across different hosts or environments
* **Version comparison**: See what changed between different versions of a document
* **Pattern recognition**: Identify common fields and values across similar events

