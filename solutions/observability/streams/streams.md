---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---

# Streams
% can we document when to use streams vs when to not use streams?

Streams provides a single, centralized UI within {{kib}} that streamlines common tasks like extracting fields, setting data retention, and rerouting data, so you don't need to use multiple applications or manually configure underlying {{es}} components.

A Stream directly corresponds to an {{es}} data stream (for example, `logs-myapp-default`). Any updates you perform in Streams configures a specific [data stream](../../../manage-data/data-store/data-streams.md).

% need to add a wired vs classic streams section

## Required permissions

Streams requires the following Elastic Cloud Serverless roles:

- Admin: ability to manage all Streams.
- Editor/Viewer: limited access, unable to perform all actions.

## Access Streams

Open Streams from one of the following places in {{kib}}:

- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

- You can open the data stream for a specific document from **Discover**. To do this, expand a document's details flyout and select **Stream** or an action associated with the document's data stream. Streams will open filtered to the selected data stream. This only works for documents stored in a data stream.

## Manage individual streams [streams-management-tab]

Interact with and configure your streams in the following ways:

- [Retention](./management/retention.md): Manage how your stream retains data and get insight into data ingestion and storage size.
- [Processing](./management/extract.md): Parse and extract information from documents into dedicated fields.
- [Schema](./management/schema.md): Manage field mappings.
- [Data quality](./management/data-quality.md): Get information about failed and degraded documents in your stream.
- [Advanced](./management/advanced.md): Review and manually modify underlying {{es}} components of your stream.