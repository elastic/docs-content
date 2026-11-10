---
navigation_title: Compare documents
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Compare several results side by side in Discover to see which field values differ, and change how the differences are highlighted.
---

# Compare documents in Discover

When two results look almost the same, such as two log lines from the same service, comparing their field values side by side shows exactly which values differ.

## Before you begin

Open **Discover** and run a query that returns at least two results.

## Compare results

1. In the results table (the **Results** tab, or **Documents** in classic mode), select the checkbox of each result you want to compare. Select at least two. You can compare up to 100 results at a time.
2. From the **Selected** menu in the table toolbar, select **Compare selected**. The comparison view opens and shows the selected results next to each other.
3. Compare the values of each field. By default, the first result you selected is the reference for the other results. A value that matches the reference is highlighted in green, and a value that differs is highlighted in red.

   :::{image} /explore-analyze/images/kibana-discover-compare-rows.png
   :alt: Comparison view in Discover showing selected documents next to each other, with matching values in green and differing values in red
   :screenshot:
   :::

   To use a different result as the reference, open the contextual menu of that result and select **Pin for comparison**.

4. Optional: To change how differences show, open **Comparison settings**. You can turn off difference highlighting, show differences by line, word, or character, or turn off **Show matching fields** to hide fields whose value matches in every result.
5. To leave the comparison view, select **Exit comparison mode**.

**Result:** The comparison view shows the selected results next to each other, with the differences highlighted.

## Next steps

To read every field of a single result, refer to [Inspect documents and requests in Discover](inspect-documents.md).

## Related pages

- [Copy results and share links to documents](copy-and-share-documents.md)
