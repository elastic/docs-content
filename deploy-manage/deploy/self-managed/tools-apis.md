---
navigation_title: Tools and APIs
applies_to:
  deployment:
    self:
products:
  - id: elastic-stack
  - id: elasticsearch
  - id: kibana
---
# Tools and APIs for self-managed clusters

Review key resources that can be used to interact with and manage self-managed clusters.

## APIs

The following APIs allow you to interact with your {{es}} cluster and its data. 

:::{include} /deploy-manage/deploy/_snippets/core-apis.md
:::

:::{tip}
Refer to [{{es}} API conventions](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md) to learn about headers and request body conventions, and to view examples.

Refer to [](/deploy-manage/api-keys/elasticsearch-api-keys.md) to learn how to generate API keys for your cluster.
:::

:::{include} /deploy-manage/deploy/_snippets/other-apis.md
:::

## Clients

* [{{es}} clients](/reference/elasticsearch-clients/index.md): Interact with {{es}} programmatically to integrate {{es}} into your app or website.

## Tools

* [{{es}} command line tools](elasticsearch://reference/elasticsearch/command-line-tools/index.md): Utilities for configuring security and performing other tasks from the command line.
* [{{kib}} command line tools](kibana://reference/commands.md): Utilities for performing security and connectivity related tasks for {{kib}} from the command line.
* [{{es}} Support Diagnostic tool](/troubleshoot/elasticsearch/diagnostic.md): Captures a point-in-time snapshot of cluster statistics and most {{es}} settings for troubleshooting purposes.