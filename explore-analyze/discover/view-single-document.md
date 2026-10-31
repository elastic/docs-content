---
navigation_title: View a single document
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Open one document on its own page that you can bookmark and share, or see the documents that occurred before and after it, in Discover classic mode.
---

# View a single document or the documents around it

When you investigate an event, you often need to look at one document on its own, or at what happened just before and after it. In classic mode, **Discover** lets you open a document on a page that you can bookmark and share, and view the documents around it.

## Before you begin

- Open **Discover** in classic mode and run a search that returns results. If **Discover** opens in {{esql}} mode, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode). These actions aren't available in {{esql}} mode.
- To view the surrounding documents, select a data view that has a time field.

## Open a document or its surrounding documents

1. In the document table, select {icon}`maximize` **View details** (**Toggle dialog with details** in earlier {{stack}} versions) on the row of the document you want to look at.
2. In the flyout, select one of the following:
   - **View single document** to open the document on its own page. You can bookmark the page and share its link.
   - **View surrounding documents** to inspect the documents that occurred before and after this document. Only pinned filters remain active in this view.

**Result:** **Discover** opens the document on a page that you can bookmark, or shows the documents that occurred before and after it.

## Related pages

- [Explore individual result or document details in depth](discover-get-started.md#look-inside-a-document)
- [Use Discover in classic mode](use-classic-mode.md)
