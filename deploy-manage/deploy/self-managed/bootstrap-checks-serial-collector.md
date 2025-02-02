---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-serial-collector.html
---

# Use serial collector check [bootstrap-checks-serial-collector]

There are various garbage collectors for the OpenJDK-derived JVMs targeting different workloads. The serial collector in particular is best suited for single logical CPU machines or extremely small heaps, neither of which are suitable for running Elasticsearch. Using the serial collector with Elasticsearch can be devastating for performance. The serial collector check ensures that Elasticsearch is not configured to run with the serial collector. To pass the serial collector check, you must not start Elasticsearch with the serial collector (whether it’s from the defaults for the JVM that you’re using, or you’ve explicitly specified it with `-XX:+UseSerialGC`). Note that the default JVM configuration that ships with Elasticsearch configures Elasticsearch to use the G1GC garbage collector with JDK14 and later versions. For earlier JDK versions, the configuration defaults to the CMS collector.

