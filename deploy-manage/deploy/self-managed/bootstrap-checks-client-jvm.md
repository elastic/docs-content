---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-client-jvm.html
---

# Client JVM check [bootstrap-checks-client-jvm]

There are two different JVMs provided by OpenJDK-derived JVMs: the client JVM and the server JVM. These JVMs use different compilers for producing executable machine code from Java bytecode. The client JVM is tuned for startup time and memory footprint while the server JVM is tuned for maximizing performance. The difference in performance between the two VMs can be substantial. The client JVM check ensures that Elasticsearch is not running inside the client JVM. To pass the client JVM check, you must start Elasticsearch with the server VM. On modern systems and operating systems, the server VM is the default.

