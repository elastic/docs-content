---
applies_to:
  serverless:
    observability: preview
description: Connect Elastic nightshift to your data and tools with External Elasticsearch, GitHub, Slack, and HTTP connectors, so investigations have more to work with.
products:
  - id: observability
  - id: cloud-serverless
---

# Connect your data and tools [nightshift-connect]

Add connectors so the investigation agent can query your data and read the code and documentation behind your systems, and connect Slack to chat with Elastic nightshift and receive results. For supported connectors and what data each gives the investigation agent, refer to [Connectors and integrations](../core-components/connectors-and-integrations.md). For how connectors work in {{kib}}, refer to [Kibana connectors](kibana://reference/connectors-kibana.md).

You add connectors from the Elastic nightshift **Settings** page.

## Before you begin [nightshift-connect-prereqs]

Make sure you have the following:

- An {{obs-serverless}} project on the Complete tier with Elastic nightshift [enabled](../get-started.md#nightshift-get-started-enable).
- A role that can manage engines. Refer to [Grant access to Elastic nightshift](./privileges.md).

## Open the Add connector flyout [nightshift-connect-open]

1. On the Elastic nightshift home page, select the {icon}`boxes_vertical` menu, then **Settings**.
1. On the **General** tab, in **Connectors**, select **Add connector**.

The **Add connector** flyout lists each connector type that you can use, with the number of connectors that you've already created for it. Select **Create connector** next to a type to create one.

### Add an External {{es}} connector [nightshift-connect-elasticsearch]

Add an External {{es}} connector so the investigation agent can query your data.

1. In the **Add connector** flyout, select **Create connector** next to **External Elasticsearch**.
1. Enter a **Connector name** and a **Connector ID**, which is a unique identifier for the connector.
1. Under **Connector settings**, enter the **Elasticsearch URL** of the cluster that you want to query, for example `https://my-cluster.es.us-east-1.aws.elastic.cloud`.
1. Choose how the connector authenticates, and enter the credentials. Either option uses shared credentials, which the connector stores and uses for every request:

   - **Elasticsearch API key** (recommended): Enter the **API key**.
   - **Username and password**.

1. Under **Actions**, choose which actions the investigation agent can use. Select **All**, or select **Custom** and select the actions in the table. The connector has six actions, all of which only read data: `esql`, `getClusterInfo`, `getMapping`, `listIndices`, `request`, and `search`. The `request` action sends any `GET` request to the {{es}} REST API.
1. Select **Save**.

For the connector's settings, refer to [External {{es}} connector](kibana://reference/connectors-kibana/elasticsearch-action-type.md).

### Connect GitHub [nightshift-connect-github]

GitHub holds the source of truth for the code behind your systems, and often your runbooks, architecture diagrams, and Helm charts too. Connect GitHub to give Elastic nightshift more information to investigate problems with your systems.

1. In the **Add connector** flyout, select **Create connector** next to **GitHub**.
1. Enter your credentials. Use a fine-grained personal access token, which lets you limit access to specific repositories.

For the connector's settings, refer to [GitHub connector](kibana://reference/connectors-kibana/github-action-type.md).

## Connect Slack [nightshift-connect-slack]

Connect the Elastic Slack app to get investigation updates in Slack and to ask Elastic nightshift for help from a channel. An admin connects the Slack workspace once, then connects each channel where `@elastic` should answer.

1. On the Elastic nightshift **Settings** page, open the **General** tab. In **Slack channels**, select **Connect Slack**.
1. Authorize the Elastic Slack app in Slack. To use private channels, allow private channel access when you authorize.
1. In Slack, invite `@elastic` to each channel that you want to use. `@elastic` only answers in channels where it's invited and connected.
1. In **Slack channels**, under **Connected channels**, enter the channel's ID or link in **Slack channel ID or link**, then select **Connect channel**.

The channel appears in the **Connected channels** list with a **Connected** status. To stop `@elastic` from answering in a channel, select **Disconnect** next to it. To remove the Slack workspace, select **Disconnect workspace**.

After a channel is connected, ask `@elastic` in a thread to chat with Elastic nightshift. For what you can do in Slack, refer to [Use investigations in Slack](../investigate-and-respond.md#nightshift-investigations-slack).

## Add an HTTP connector [nightshift-connect-http]

Add an HTTP connector so the investigation agent can call any endpoint that returns data, such as an API for your runbooks or the status of your builds. Use it for anything that doesn't have its own connector.

1. In the **Add connector** flyout, select **Create connector** next to **HTTP**.
1. Enter a **Connector name**. {{kib}} suggests a **Connector ID**, which you can edit before you save.
1. In **Base URL**, enter the base URL of the API, for example `https://example.com/api/v1`.
1. Under **Authentication**, select how the connector authenticates:

   - **None**
   - **Basic authentication**: Enter a **Username** and **Password**.
   - **SSL authentication**
   - **OAuth 2.0 Client Credentials**

1. Optionally, turn on **Add HTTP header**, **Add certificate authority**, **Add query parameters**, or **Proxy**.
1. Save the connector.

When you edit the connector, you must enter the username and password again.

## Next steps [nightshift-connect-next]

- [Get started](../get-started.md#nightshift-get-started-first-investigation): Run your first investigation and read the results
- [Connectors and integrations](../core-components/connectors-and-integrations.md): Learn how investigations use connectors
