---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/controlling-user-cache.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Controlling the user cache [controlling-user-cache]

User credentials are cached in memory on each node to avoid connecting to a remote authentication service or hitting the disk for every incoming request. You can configure characteristics of the user cache with the `cache.ttl`, `cache.max_users`, and `cache.hash_algo` realm settings.

::::{note}
JWT realms use `jwt.cache.ttl` and `jwt.cache.size` realm settings.
::::


::::{note}
PKI and JWT realms do not cache user credentials, but do cache the resolved user object to avoid unnecessarily needing to perform role mapping on each request.
::::


The cached user credentials are hashed in memory. By default, the {{es}} {{security-features}} use a salted `sha-256` hash algorithm. You can use a different hashing algorithm by setting the `cache.hash_algo` realm settings. See [User cache and password hash algorithms](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#hashing-settings).

## Evicting users from the cache [cache-eviction-api]

You can use the [clear cache API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-clear-cached-realms) to force the eviction of cached users . For example, the following request evicts all users from the `ad1` realm:

```js
$ curl -XPOST 'http://localhost:9200/_security/realm/ad1/_clear_cache'
```

To clear the cache for multiple realms, specify the realms as a comma-separated list:

```js
$ curl -XPOST 'http://localhost:9200/_security/realm/ad1,ad2/_clear_cache'
```

You can also evict specific users:

```java
$ curl -XPOST 'http://localhost:9200/_security/realm/ad1/_clear_cache?usernames=rdeniro,alpacino'
```


