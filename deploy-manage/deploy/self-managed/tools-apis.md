---
navigation_title: "Tools and APIs"
applies_to:
  deployment:
    self:
---
# Tools and APIs for self-managed clusters

Review key resources that can be used to interact with and manage self-managed clusters.

## APIs

* [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/): The core API for interacting with a self-managed {{es}} cluster, or any cluster running {{stack}}. Configure {{es}} functionality and settings, query your data, and more.
  
    Refer to [REST APIs](elasticsearch://reference/elasticsearch/rest-apis/index.md) to learn about API conventions and view API usage examples.
* [{{kib}} API](https://www.elastic.co/docs/api/doc/kibana/): manage {{kib}} resources such as connectors, data views, and saved objects.

:::{tip}
Learn how to [generate API keys for your self-managed cluster](/deploy-manage/api-keys/elasticsearch-api-keys.md).
:::

## Clients

* [{{es}} clients](/reference/elasticsearch/clients/index.md): Interact with {{es}} programmatically to integrate {{es}} into your app or website.

## Other

* [{{es}} command line tools](elasticsearch://reference/elasticsearch/command-line-tools/index.md): Utilities for configuring security and performing other tasks from the command line.
* [{{kib}} command line tools](kibana://reference/commands.md): Utilities for performing security and connectivity related tasks for {{kib}} from the command line.
* [Plugins](elasticsearch://reference/elasticsearch-plugins/index.md): Plugins extend core {{es}} functionality. Choose from an existing plugin, or [build your own](elasticsearch://extend/index.md).