---
applies_to:
    serverless: preview
---

:::{note}
Streams is currently in Technical Preview and available only on Elastic Cloud Serverless deployments. Features and UI may change.
:::

# Streams

Streams provides a single, centralized UI within {{kib}} that streamlines common tasks, reducing the need to navigate multiple applications or manually configure underlying {{es}} components. Key workflows supported today include:
- [Extracting fields](../streams/management/extract.md) from your documents.
- [Changing the retention](../streams/management/retention.md) of a stream.

A Stream in this interface directly corresponds to an {{es}} data stream (for example, `logs-myapp-default`). Operations performed here configure that specific data stream.


## Required permissions
Streams requires the following Elastic Cloud Serverless roles:

- TODO

## Access streams
To access streams:

- From the navigation menu, select **Streams**.

- From discover, expand a document's details flyout.
Select the **Stream** link or action associated with the document's data stream to open the streams interface, filtered to show only the selected stream.


TODO: overview, Dashboards, Mangement