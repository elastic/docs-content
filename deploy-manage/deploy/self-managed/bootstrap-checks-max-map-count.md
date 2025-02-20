---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-max-map-count.html
---

# Maximum map count check [bootstrap-checks-max-map-count]

Continuing from the previous [point](max-size-virtual-memory-check.md), to use `mmap` effectively, Elasticsearch also requires the ability to create many memory-mapped areas. The maximum map count check checks that the kernel allows a process to have at least 262,144 memory-mapped areas and is enforced on Linux only. To pass the maximum map count check, you must configure `vm.max_map_count` via `sysctl` to be at least `262144`.

Alternatively, the maximum map count check is only needed if you are using `mmapfs` or `hybridfs` as the [store type](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-store-settings.md) for your indices. If you [do not allow](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-store-settings.md#allow-mmap) the use of `mmap` then this bootstrap check will not be enforced.

