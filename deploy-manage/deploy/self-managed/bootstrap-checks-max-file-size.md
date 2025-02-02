---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-max-file-size.html
---

# Max file size check [bootstrap-checks-max-file-size]

The segment files that are the components of individual shards and the translog generations that are components of the translog can get large (exceeding multiple gigabytes). On systems where the max size of files that can be created by the Elasticsearch process is limited, this can lead to failed writes. Therefore, the safest option here is that the max file size is unlimited and that is what the max file size bootstrap check enforces. To pass the max file check, you must configure your system to allow the Elasticsearch process the ability to write files of unlimited size. This can be done via `/etc/security/limits.conf` using the `fsize` setting to `unlimited` (note that you might have to increase the limits for the `root` user too).

