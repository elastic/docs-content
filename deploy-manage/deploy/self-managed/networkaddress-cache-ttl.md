---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/networkaddress-cache-ttl.html
---

# DNS cache settings [networkaddress-cache-ttl]

Elasticsearch runs with a security manager in place. With a security manager in place, the JVM defaults to caching positive hostname resolutions indefinitely and defaults to caching negative hostname resolutions for ten seconds. Elasticsearch overrides this behavior with default values to cache positive lookups for sixty seconds, and to cache negative lookups for ten seconds. These values should be suitable for most environments, including environments where DNS resolutions vary with time. If not, you can edit the values `es.networkaddress.cache.ttl` and `es.networkaddress.cache.negative.ttl` in the [JVM options](https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html#set-jvm-options). Note that the values [`networkaddress.cache.ttl=<timeout>`](https://docs.oracle.com/javase/8/docs/technotes/guides/net/properties.md) and [`networkaddress.cache.negative.ttl=<timeout>`](https://docs.oracle.com/javase/8/docs/technotes/guides/net/properties.md) in the [Java security policy](https://docs.oracle.com/javase/8/docs/technotes/guides/security/PolicyFiles.md) are ignored by Elasticsearch unless you remove the settings for `es.networkaddress.cache.ttl` and `es.networkaddress.cache.negative.ttl`.

