---
applies_to:
  serverless: preview
---

:::{warning}
Streams is currently in Technical Preview and only available on Elastic Cloud Serverless deployments. This feature may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
:::

# Streams

Streams provides a single, centralized UI within {{kib}} that streamlines common tasks, reducing the need to navigate multiple applications or manually configure underlying {{es}} components. Key workflows include:
- [Extract fields](../streams/management/extract.md) from your documents.
- [Change the data retention](../streams/management/retention.md) of a stream.

A Stream directly corresponds to an {{es}} data stream (for example, `logs-myapp-default`). Operations performed in the Streams UI configure that specific data stream.


## Required permissions

Streams requires the following Elastic Cloud Serverless roles:

- Admin: ability to manage all Streams.
- Editor/Viewer: limited access, unable to perform all actions.

## Access Streams

Access streams in one of the following ways:

- From the navigation menu, select **Streams**.

- From **Discover**, expand a document's details flyout and select **Stream** or an action associated with the document's data stream. Streams will open filtered to only the selected stream. This only works for documents stored in a data stream.

## Manage stream [streams-management-tab]

Interact with and configure your stream in the following ways:

- [Data retention](./management/retention.md): Manage how your stream retains data and get insight into data ingestion and storage size under the **Data retention** tab.
- [Processing](./management/extract.md): Parse and extract information from log messages into dedicated fields under the **Processing** tab.
- [Advanced](./management/advanced.md): Review and manually modify the inner workings of your stream under the **Advanced** tab.