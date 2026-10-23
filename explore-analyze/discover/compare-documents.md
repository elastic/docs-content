---
navigation_title: Compare documents
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Compare the field values of several results side by side in Discover to spot what differs between them, then adjust how differences show.
---

# Compare documents

To spot what differs between results, such as two log lines from the same service, compare their field values next to each other.

## Before you begin

Open **Discover** and run a query that returns at least two results.

## Compare results

1. Select the results you want to compare from the **Results** tab (**Documents** in classic mode).
2. From the **Selected** menu in the table toolbar, select **Compare selected**. The comparison view opens and shows the selected results next to each other.
3. Compare the values of each field. By default the first result selected shows as the reference for displaying differences in the other results. When the value remains the same for a given field, it’s displayed in green. When the value differs, it’s displayed in red.
   ::::{tip}
   You can change the result used as reference by selecting **Pin for comparison** in the contextual menu of any other result.
   ::::


   ![Comparison view in Discover](/explore-analyze/images/kibana-discover-compare-rows.png "")

4. Optionally, customize the **Comparison settings** to your liking. You can for example choose to not highlight the differences, to show them more granularly at the line, word, or character level, or even to hide fields where the value matches for all results.
5. Exit the comparison view at any time using the **Exit comparison mode** button.

## Related pages

- [Inspect documents and requests in Discover](inspect-documents.md)
- [Copy results and share links to documents](copy-and-share-documents.md)
