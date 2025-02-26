---
navigation_title: "add_observer_metadata"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_observer_metadata-processor.html
---

# Add Observer metadata [add_observer_metadata-processor]


::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


The `add_observer_metadata` processor annotates each event with relevant metadata from the observer machine.


## Example [_example_10]

```yaml
  - add_observer_metadata:
      cache.ttl: 5m
      geo:
        name: nyc-dc1-rack1
        location: 40.7128, -74.0060
        continent_name: North America
        country_iso_code: US
        region_name: New York
        region_iso_code: NY
        city_name: New York
```

The fields added to the event look like this:

```json
{
  "observer" : {
    "hostname" : "avce",
    "type" : "heartbeat",
    "vendor" : "elastic",
    "ip" : [
      "192.168.1.251",
      "fe80::64b2:c3ff:fe5b:b974",
    ],
    "mac" : [
      "dc:c1:02:6f:1b:ed",
    ],
    "geo": {
      "continent_name": "North America",
      "country_iso_code": "US",
      "region_name": "New York",
      "region_iso_code": "NY",
      "city_name": "New York",
      "name": "nyc-dc1-rack1",
      "location": "40.7128, -74.0060"
    }
  }
}
```


## Configuration settings [_configuration_settings_12]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `netinfo.enabled` | No | `true` | Whether to include IP addresses and MAC addresses as fields `observer.ip` and `observer.mac`. |
| `cache.ttl` | No | `5m` | Sets the cache expiration time for the internal cache used by the processor. Negative values disable caching altogether. |
| `geo.name` | No |  | User-definable token to be used for identifying a discrete location. Frequently a data center, rack, or similar. |
| `geo.location` | No |  | Longitude and latitude in comma-separated format. |
| `geo.continent_name` | No |  | Name of the continent. |
| `geo.country_name` | No |  | Name of the country. |
| `geo.region_name` | No |  | Name of the region. |
| `geo.city_name` | No |  | Name of the city. |
| `geo.country_iso_code` | No |  | ISO country code. |
| `geo.region_iso_code` | No |  | ISO region code. |

