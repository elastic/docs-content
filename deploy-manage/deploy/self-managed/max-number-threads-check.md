---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/max-number-threads-check.html
---

# Maximum number of threads check [max-number-threads-check]

Elasticsearch executes requests by breaking the request down into stages and handing those stages off to different thread pool executors. There are different [thread pool executors](elasticsearch://reference/elasticsearch/configuration-reference/thread-pool-settings.md) for a variety of tasks within Elasticsearch. Thus, Elasticsearch needs the ability to create a lot of threads. The maximum number of threads check ensures that the Elasticsearch process has the rights to create enough threads under normal use. This check is enforced only on Linux. If you are on Linux, to pass the maximum number of threads check, you must configure your system to allow the Elasticsearch process the ability to create at least 4096 threads. This can be done via `/etc/security/limits.conf` using the `nproc` setting (note that you might have to increase the limits for the `root` user too).

