---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-heap-size.html
---

# Heap size check [bootstrap-checks-heap-size]

By default, {{es}} automatically sizes JVM heap based on a node’s [roles](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md#node-roles) and total memory. If you manually override the default sizing and start the JVM with different initial and max heap sizes, the JVM may pause as it resizes the heap during system usage. If you enable [`bootstrap.memory_lock`](setup-configuration-memory.md#bootstrap-memory_lock), the JVM locks the initial heap size on startup. If the initial heap size is not equal to the maximum heap size, some JVM heap may not be locked after a resize. To avoid these issues, start the JVM with an initial heap size equal to the maximum heap size.

