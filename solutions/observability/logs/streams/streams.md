---
applies_to:
    serverless: preview
---

:::{note}
Streams is currently in Technical Preview and available only on Elastic Cloud Serverless deployments. Features and UI may change.
:::

# Streams

Streams provides a single, centralized UI within {{kib}} that streamlines common tasks, reducing the need to navigate multiple applications or manually configure underlying {{es}} components. Key workflows include:
- [Extract fields](../streams/management/extract.md) from your documents.
- [Change the data retention](../streams/management/retention.md) of a stream.

A Stream in this interface directly corresponds to an {{es}} data stream (for example, `logs-myapp-default`). Operations performed here configure that specific data stream.


## Required permissions
Streams requires the following Elastic Cloud Serverless roles:

% - TODO

## Access Streams
To access Streams:

- From the navigation menu, select **Streams**.

- From discover, expand a document's details flyout.
Select the **Stream** link or action associated with the document's data stream to open the Streams interface, filtered to show only the selected stream.


## Overview tab [streams-overview-tab]

The **Overview** tab provides key metrics for the selected stream, such as data retention, document count, storage size, and average ingestion.

![Screenshot of the Overview tab UI](<overview.png>)

the **Overview** tab is made up of the following components:

- **Data retention**: Your current data retention policy. For more detailed information, visit [**Data Retention**](./management/retention.md) under the **Management** tab.
- **Document count**: The current total number of documents in your stream, unrelated to the time range.
- **Storage size**: The current total storage size of your stream, unrelated to the time range.
- **Ingestion**: shows the average ingestion per day since the stream was created.
- **Dashboards table**: quick links to [dashboards](#streams-dashboard-tab) you've added to the stream.

% Maybe we want to add something about the documents ingestion graph as well?


## Dashboards tab [streams-dashboard-tab]

The **Dashboards** tab is where you can add dashboards to your stream. [Dashboards](../../../../explore-analyze/dashboards.md) are visualizations that group important assets for your stream.

Add a dashboard to your stream by selecting it from the list of available dashboards.

![Screenshot of the dashboards UI](<dashboards.png>)

Added dashboards are also shown on the [**Overview** tab](#streams-overview-tab) as quick links.

## Management tab

The **Management** tab is where you'll interact with and configure your stream:

% Probably want a screenshot here for consistency with the other tabs?

- [Extract field](./management/extract.md): Parse and extract information from log messages into dedicated fields.
- [Data retention](./management/retention.md): Manage how your stream retains data and get insight into data ingestion and storage size.
- [Advanced](./management/advanced.md): Review and manually modify the inner workings of your stream.

% TODO this is very short now. There will likely be more to add here in the future, not sure if it makes sense to fill the space now