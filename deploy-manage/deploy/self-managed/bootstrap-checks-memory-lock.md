---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-memory-lock.html
---

# Memory lock check [bootstrap-checks-memory-lock]

When the JVM does a major garbage collection it touches every page of the heap. If any of those pages are swapped out to disk they will have to be swapped back in to memory. That causes lots of disk thrashing that Elasticsearch would much rather use to service requests. There are several ways to configure a system to disallow swapping. One way is by requesting the JVM to lock the heap in memory through `mlockall` (Unix) or virtual lock (Windows). This is done via the Elasticsearch setting [`bootstrap.memory_lock`](setup-configuration-memory.md#bootstrap-memory_lock). However, there are cases where this setting can be passed to Elasticsearch but Elasticsearch is not able to lock the heap (e.g., if the `elasticsearch` user does not have `memlock unlimited`). The memory lock check verifies that **if** the `bootstrap.memory_lock` setting is enabled, that the JVM was successfully able to lock the heap. To pass the memory lock check, you might have to configure [`bootstrap.memory_lock`](setup-configuration-memory.md#bootstrap-memory_lock).

