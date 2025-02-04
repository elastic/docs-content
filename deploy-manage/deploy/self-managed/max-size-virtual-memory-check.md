---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/max-size-virtual-memory-check.html
---

# Maximum size virtual memory check [max-size-virtual-memory-check]

Elasticsearch and Lucene use `mmap` to great effect to map portions of an index into the Elasticsearch address space. This keeps certain index data off the JVM heap but in memory for blazing fast access. For this to be effective, the Elasticsearch should have unlimited address space. The maximum size virtual memory check enforces that the Elasticsearch process has unlimited address space and is enforced only on Linux. To pass the maximum size virtual memory check, you must configure your system to allow the Elasticsearch process the ability to have unlimited address space. This can be done via adding `<user> - as unlimited` to `/etc/security/limits.conf`. This may require you to increase the limits for the `root` user too.

