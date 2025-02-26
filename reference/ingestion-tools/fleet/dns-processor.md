---
navigation_title: "dns"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/dns-processor.html
---

# DNS Reverse Lookup [dns-processor]


The `dns` processor performs reverse DNS lookups of IP addresses. It caches the responses that it receives in accordance to the time-to-live (TTL) value contained in the response. It also caches failures that occur during lookups. Each instance of this processor maintains its own independent cache.

The processor uses its own DNS resolver to send requests to nameservers and does not use the operating system’s resolver. It does not read any values contained in `/etc/hosts`.

This processor can significantly slow down your pipeline’s throughput if you have a high latency network or slow upstream nameserver. The cache will help with performance, but if the addresses being resolved have a high cardinality, cache benefits are diminished due to the high miss ratio.

For example, if each DNS lookup takes 2 milliseconds, the maximum throughput you can achieve is 500 events per second (1000 milliseconds / 2 milliseconds). If you have a high cache hit ratio, your throughput can be higher.


## Examples [_examples_8]

This is a minimal configuration example that resolves the IP addresses contained in two fields.

```yaml
  - dns:
      type: reverse
      fields:
        source.ip: source.hostname
        destination.ip: destination.hostname
```

This examples shows all configuration options.

```yaml
  - dns:
    type: reverse
    action: append
    transport: tls
    fields:
      server.ip: server.hostname
      client.ip: client.hostname
    success_cache:
      capacity.initial: 1000
      capacity.max: 10000
      min_ttl: 1m
    failure_cache:
      capacity.initial: 1000
      capacity.max: 10000
      ttl: 1m
    nameservers: ['192.0.2.1', '203.0.113.1']
    timeout: 500ms
    tag_on_failure: [_dns_reverse_lookup_failed]
```


## Configuration settings [_configuration_settings_28]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `type` | Yes |  | Type of DNS lookup to perform. The only supported type is `reverse`, which queries for a PTR record. |
| `action` | No | `append` | Defines the behavior of the processor when the target field already exists in the event. The options are `append` and `replace`. |
| `fields` | Yes |  | Mapping of source field names to target field names. The value of the source field is used in the DNS query, and the result is written to the target field. |
| `success_cache.capacity.initial` | No | `1000` | Initial number of items that the success cache is allocated to hold. When initialized, the processor will allocate memory for this number of items. |
| `success_cache.capacity.max` | No | `10000` | Maximum number of items that the success cache can hold. When the maximum capacity is reached, a random item is evicted. |
| `success_cache.min_ttl` | Yes | `1m` | Duration of the minimum alternative cache TTL for successful DNS responses. Ensures that `TTL=0` successful reverse DNS responses can be cached. Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h". |
| `failure_cache.capacity.initial` | No | `1000` | Initial number of items that the failure cache is allocated to hold. When initialized, the processor will allocate memory for this number of items. |
| `failure_cache.capacity.max` | No | `10000` | Maximum number of items that the failure cache can hold. When the maximum capacity is reached, a random item is evicted. |
| `failure_cache.ttl` | No | `1m` | Duration for which failures are cached. Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h". |
| `nameservers` | Yes (on Windows) |  | List of nameservers to query. If there are multiple servers, the resolver queries them in the order listed. If none are specified, it reads the nameservers listed in `/etc/resolv.conf` once at initialization. On Windows you must always supply at least one nameserver. |
| `timeout` | No | `500ms` | Duration after which a DNS query will timeout. This is timeout for each DNS request, so if you have two nameservers, the total timeout will be 2 times this value. Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h". |
| `tag_on_failure` | No | `false` | List of tags to add to the event when any lookup fails. The tags are only added once even if multiple lookups fail. By default no tags are added upon failure. |
| `transport` | No | `udp` | Type of transport connection that should be used: `tls` (DNS over TLS) or `udp`. |

