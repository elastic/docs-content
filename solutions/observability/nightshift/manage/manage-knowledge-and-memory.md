---
applies_to:
  serverless:
    observability: preview
description: Review what Elastic nightshift has learned on the Knowledge page, archive or restore Wiki pages and memories, and give Elastic nightshift context through automation instructions and custom context.
products:
  - id: observability
  - id: cloud-serverless
---

# Manage knowledge and memory [nightshift-manage-knowledge]

Elastic nightshift keeps knowledge about your systems so that investigations start from an understanding of your environment. It manages this knowledge itself, saving what it learns to the Wiki and Memory. You can review what it has learned, archive anything that isn't useful, and give it more context through automation instructions and custom context.

## Before you begin [nightshift-manage-knowledge-prereqs]

You need read access to Elastic nightshift to view knowledge. To archive or restore it, you need write access. To add custom context, you need a role that can manage engines, because only those users see the **Settings** page.

## View what Elastic nightshift knows [nightshift-manage-knowledge-view]

From the Elastic nightshift home page, select {icon}`boxes_vertical` → **Knowledge**. The page has these tabs:

- **Knowledge Indicators**: Facts that detection extracted about your systems, such as services, infrastructure, and dependencies.
- **Wiki**: Durable knowledge that the investigator reads before each run, organized into pages by type, such as services, runbooks, postmortems, and queries. Each page shows its type and whether it's established or tentative.
- **Memory**: Lessons that the investigator saves after a run and recalls when it works on a similar problem, such as how a previous problem was resolved or which checks found its cause. Memory is free-form and searched semantically, so only the relevant parts load.

## Archive or restore knowledge [nightshift-manage-knowledge-archive]

Elastic nightshift manages the Wiki and Memory itself, so you can't edit them. To stop Elastic nightshift from using a Wiki page or a memory that isn't correct or useful, archive it. Archiving keeps it, so you can restore it later.

1. Open the Wiki page or memory.
1. Select **Archive**.

To use an archived entry again, filter the list by **Archived**, open the entry, and select **Restore**. To remove a memory permanently, select **Delete**.

## Give Elastic nightshift context [nightshift-manage-knowledge-context]

To give Elastic nightshift context about your systems, such as your architecture, runbooks, and skills, add it to an automation's instructions. Point Elastic nightshift to where the context lives, for example the GitHub repositories that hold your architecture. After the automation runs once, Elastic nightshift explores what you pointed it to and adds it to the Wiki and Memory to reuse in later investigations. Refer to [Give Elastic nightshift context in the instructions](../set-up-an-automation.md).

## Add custom context [nightshift-manage-knowledge-custom-context]

Custom context is a set of short notes, called snippets, about your environment, such as investigation conventions, service ownership, and known quirks. Elastic nightshift adds them to its instructions for every investigation and every chat in the space.

1. On the Elastic nightshift home page, select the {icon}`boxes_vertical` menu, then **Settings**, and select the **Investigations** tab.
1. In **Custom context**, select **Edit investigation context**.
1. In the **Custom context** flyout, select **Add snippet**.
1. Enter your note in the text box, for example "While debugging alerts, always rule out a release or config regression first."
1. Select **Save**.
1. Select **Close**.

## Next steps [nightshift-manage-knowledge-next]

- [Context engine](../memory.md): Learn how Elastic nightshift stores and uses knowledge
- [Set up an automation](../set-up-an-automation.md): Give Elastic nightshift context through instructions