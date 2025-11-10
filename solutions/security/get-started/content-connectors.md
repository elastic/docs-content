---
applies_to:
  stack: 
  serverless:
---

# Content connectors

Elastic's content connectors allow you to extract, transform, index, and sync data from third-party applications including Github, Jira, Teams, Google Drive, Slack, email, and more ([view all connectors](elasticsearch://reference/search-connectors/index.md)).

## Managed vs self-managed connectors

Content connectors are available in two deployment options: you can run them yourself or let Elastic run them within your managed deployment on {{ecloud}}.

### Elastic managed connectors
```yaml {applies_to}
stack: preview 9.1
deployment:
    self: unavailable
serverless:
    security: preview
```

Elastic managed connectors are deployed within your managed Elastic environment. These connectors:
- Require no infrastructure management
- Offer simplified setup and maintenance
- Do not support customization
- Only send data to the serverless/hosted deployment they're deployed within

### Self-managed connectors
Self-managed connectors run on your own infrastructure, independent of where your {{es}} instance is running. These connectors:
- Require you to deploy the connector service (Python) on your infrastructure
- Can send data to any {{es}} instance (managed or self-managed)
- Can be customized

## Setup 

To learn about setup for self-managed connectors, refer to [Self-managed connectors](elasticsearch://reference/search-connectors/self-managed-connectors.md). To set up an Elastic managed connector:

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find "Content conectors".
1. Click **New Connector**.
1. Under **Connector**, select your desired data source.
1. Under **Setup**, select your deployment method. 
1. Under **Configure index & API key**, click **Generate configuration**. After a few seconds, this will create a new connector and a new index for its data, and display their names and IDs. You can click their names to view details about each. 
1. Click **Next** to continue to the **Configuration** page. This is where you can select details related to your specific data source. For more information about configuring your selected data source, follow the link on the left to the **Connector reference**.
1. When configuration is complete, click **Next**. The **Finish up** page appears. Here you can set up recurring connector syncs, run a manual sync, or use queries and dev tools to interact with your data. Each sync updates the data in the connector's {{es}} index. You can also manage the connector.


## Manage a connector 

To manage an existing connector:

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find "Content connectors". 
1. Click the connector you want to manage to open its settings page, which has six tabs:
  - **Overview**: View general information such as the connector's name, ID, status, pipeline, and content sync history. Manage the connector's pipeline and attached index.
  - **Documents**: View data from the connector.
  - **Mappings**: Update index mappings for the connector's data.
  - **Sync rules**: Manage basic and advanced [sync rules](elasticsearch://reference/search-connectors/es-sync-rules.md) to control which documents are synced from your third-party data source.
  - **Scheduling**: Define when data from this connector gets synced, and set up document level security. A `Full content sync` deletes existing data in your index before fetching from your data source again. An `Incremental content sync` fetches updated data only, without deleting existing data. 
  - **Configuration**: Edit the connector's data source-specific configuration.