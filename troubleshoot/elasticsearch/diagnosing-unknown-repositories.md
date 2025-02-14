---
navigation_title: Unknown repositories
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/diagnosing-unknown-repositories.html
---

# Diagnose unknown repositories [diagnosing-unknown-repositories]

When a snapshot repository is marked as "unknown", it means that an {{es}} node is unable to instantiate the repository due to an unknown repository type. This is usually caused by a missing plugin on the node. Make sure each node in the cluster has the required plugins by following the following steps:

1. Retrieve the affected nodes from the affected resources section of the health report.
2. Use the [nodes info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-info) to retrieve the plugins installed on each node.
3. Cross reference this with a node that works correctly to find out which plugins are missing and install the missing plugins.

