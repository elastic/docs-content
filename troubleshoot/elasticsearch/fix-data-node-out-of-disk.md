---
navigation_title: Data nodes out of disk
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/fix-data-node-out-of-disk.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

% marciw move to new "out of disk" subsection

# Fix data nodes out of disk [fix-data-node-out-of-disk]

{{es}} is using data nodes to distribute your data inside the cluster. If one or more of these nodes are running out of space, {{es}} takes action to redistribute your data within the nodes so all nodes have enough available disk space. If {{es}} cannot facilitate enough available space in a node, then you can intervene in one of two ways:

1. [Increase the disk capacity of your cluster](increase-capacity-data-node.md)
2. [Reduce the disk usage by decreasing your data volume](decrease-disk-usage-data-node.md)



