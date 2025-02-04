---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-onerror.html
---

# OnError and OnOutOfMemoryError checks [bootstrap-checks-onerror]

The JVM options `OnError` and `OnOutOfMemoryError` enable executing arbitrary commands if the JVM encounters a fatal error (`OnError`) or an `OutOfMemoryError` (`OnOutOfMemoryError`). However, by default, Elasticsearch system call filters (seccomp) are enabled and these filters prevent forking. Thus, using `OnError` or `OnOutOfMemoryError` and system call filters are incompatible. The `OnError` and `OnOutOfMemoryError` checks prevent Elasticsearch from starting if either of these JVM options are used and system call filters are enabled. This check is always enforced. To pass this check do not enable `OnError` nor `OnOutOfMemoryError`; instead, upgrade to Java 8u92 and use the JVM flag `ExitOnOutOfMemoryError`. While this does not have the full capabilities of `OnError` nor `OnOutOfMemoryError`, arbitrary forking will not be supported with seccomp enabled.

