---
applies_to:
  serverless: preview
  stack: preview 9.1
---

:::{warning}
Streams is currently in Technical Preview. This feature may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
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

## Access the Streams UI

In {{obs-serverless}}, Streams is automatically available.

In {{stack}} version 9.1 and later, you can enable Streams in the {{observability}} Advanced Settings. To do this:

1. Go to the **Advanced Settings** page in the navigation menu or by searching fo, or search for "Advanced Settings" in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Enable **Streams UI** under **Observability**.

In {{serverless-short}} or after enabling Streams in {{stack}}, access the UI in one of the following ways:

- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

- From **Discover**, expand a document's details flyout and select **Stream** or an action associated with the document's data stream. Streams will open filtered to only the selected stream. This only works for documents stored in a data stream.

## Manage individual streams [streams-management-tab]

Interact with and configure your streams in the following ways:

- [Data retention](./management/retention.md): Manage how your stream retains data and get insight into data ingestion and storage size under the **Data retention** tab.
- [Processing](./management/extract.md): Parse and extract information from log messages into dedicated fields under the **Processing** tab.
- [Advanced](./management/advanced.md): Review and manually modify the inner workings of your stream under the **Advanced** tab.