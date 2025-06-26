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


## Overview tab [streams-overview-tab]

Use the **Overview** tab to find key metrics for the selected stream, such as data retention, document count, storage size, and average ingestion.

![Screenshot of the Overview tab UI](<../../../images/logs-streams-overview.png>)

the **Overview** tab is made up of the following components:

- **Data retention**: Your current data retention policy. For more detailed information, refer to the [**Data Retention**](./management/retention.md) tab on the **Management** page.
- **Document count**: The current total number of documents in your stream, unrelated to the time range.
- **Storage size**: The current total storage size of your stream, unrelated to the time range.
- **Ingestion**: shows the average ingestion per day since the stream was created.
- **Dashboards table**: quick links to [dashboards](#streams-dashboard-tab) you've added to the stream.

% Maybe we want to add something about the documents ingestion graph as well?


## Dashboards tab [streams-dashboard-tab]

Use the **Dashboards** tab to add dashboards to your stream. [Dashboards](../../../../explore-analyze/dashboards.md) are visualizations that group together important assets for your stream.

Add a dashboard to your stream by selecting it from the list of available dashboards.

![Screenshot of the dashboards UI](<../../../images/logs-streams-dashboard.png>)

Added dashboards are also shown on the [**Overview** tab](#streams-overview-tab) as quick links.

## Manage stream [streams-management-tab]

Use the **Manage stream** page to interact with and configure your stream in the following ways:

% Probably want a screenshot here for consistency with the other tabs?

- [Extract field](./management/extract.md): Parse and extract information from log messages into dedicated fields.
- [Data retention](./management/retention.md): Manage how your stream retains data and get insight into data ingestion and storage size.
- [Advanced](./management/advanced.md): Review and manually modify the inner workings of your stream.

% TODO this is very short now. There will likely be more to add here in the future, not sure if it makes sense to fill the space now