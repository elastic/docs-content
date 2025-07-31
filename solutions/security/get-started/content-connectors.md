---
applies_to:
  stack: preview 9.1
  serverless: preview
---

# Content connectors

Elastic's content connectors allow you to extract, transform, index, and sync data from third-party applications including Github, PagerDuty, Jira, Teams, Google Drive, Slack, email, and more ([view all connectors](elasticsearch://reference/search-connectors/index.md)).

{{stack}} supports two deployment methods for your connectors: Elastic managed, and self-managed. Self-managed connectors require you to deploy on your own infrastructure (for example, run some Python code on a server you manage). When you use an Elastic managed connector, Elastic runs the infrastructure for you. Self-managed connectors can be customized, whereas Elastic managed connectors do not allow customization. 

{{sec-serverless}} only supports Elastic managed connectors. {{stack}} deployments support either self-managed or Elastic managed deployments.

## Setup 

To learn about set up for self-managed connectors, refer to [Self managed connectors](elasticsearch://reference/search-connectors/self-managed-connectors.md). To set up an Elastic managed connector:

- Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find "Content conectors".
- Click **New Connector**.
- Under **Connector**, select your desired data source.
- Under **Setup**, select your deployment method. 
- Under **Configure index & API key**, click **Generate configuration**. After a few seconds, this will create a new connector and a new index for its data, and display their names and IDs. You can click their names to view details about each. 
- Click **Next** to continue to the **Configuration** page. This is where you can select details related to your specific data source. For more information about configuring your selected data source, follow the link on the left to the **Connector reference**.
- When configuration is complete, click **Next**. The **Finish up** page appears. Here you can set up recurring connector syncs, run a manual sync, or use queries and dev tools to interact with your data. Each sync updates the data in the connector's {{es}} index. You can also manage the connector.


## Manage a connector 

To manage an existing connector:

- Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find "Content connectors". 
- Click the connector you want to manage to open its settings page, which has six tabs:
  - **Overview**: View general information such as the connector's name, ID, status, pipeline, and content sync history. Manage the connector's pipeline and attached index.
  - **Documents**: View data from the connector.
  - **Mappings**: Update index mappings for the connector's data.
  - **Sync rules**: Manage basic and advanced [sync rules](elasticsearch://reference/search-connectors/es-sync-rules.md) to control which documents are synced from your third-party data source.
  - **Scheduling**: Define when data from this connector gets synced, and set up document level security. A `Full content sync` deletes existing data in your index before fetching from your data source again. An `Incremental content sync` fetches updated data only, without deleting existing data. 
  - **Configuration**: Edit the connector's data source-specific configuration.