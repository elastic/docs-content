---
navigation_title: "add_host_metadata"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_host_metadata-processor.html
---

# Add Host metadata [add_host_metadata-processor]


::::{tip}
Inputs that collect logs and metrics use this processor by default, so you do not need to configure it explicitly.
::::


The `add_host_metadata` processor annotates each event with relevant metadata from the host machine.

::::{note}
If you are using {{agent}} to monitor external system, use the [`add_observer_metadata`](/reference/ingestion-tools/fleet/add_observer_metadata-processor.md) processor instead of `add_host_metadata`.
::::



## Example [_example_5]

```yaml
  - add_host_metadata:
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
   "host":{
      "architecture":"x86_64",
      "name":"example-host",
      "id":"",
      "os":{
         "family":"darwin",
         "type":"macos",
         "build":"16G1212",
         "platform":"darwin",
         "version":"10.12.6",
         "kernel":"16.7.0",
         "name":"Mac OS X"
      },
      "ip": ["192.168.0.1", "10.0.0.1"],
      "mac": ["00:25:96:12:34:56", "72:00:06:ff:79:f1"],
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


## Configuration settings [_configuration_settings_5]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


::::{important}
If `host.*` fields already exist in the event, they are overwritten by default unless you set `replace_fields` to `true` in the processor configuration.
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `netinfo.enabled` | No | `true` | Whether to include IP addresses and MAC addresses as fields `host.ip` and `host.mac`. |
| `cache.ttl` | No | `5m` | Sets the cache expiration time for the internal cache used by the processor. Negative values disable caching altogether. |
| `geo.name` | No |  | User-definable token to be used for identifying a discrete location. Frequently a data center, rack, or similar. |
| `geo.location` | No |  | Longitude and latitude in comma-separated format. |
| `geo.continent_name` | No |  | Name of the continent. |
| `geo.country_name` | No |  | Name of the country. |
| `geo.region_name` | No |  | Name of the region. |
| `geo.city_name` | No |  | Name of the city. |
| `geo.country_iso_code` | No |  | ISO country code. |
| `geo.region_iso_code` | No |  | ISO region code. |
| `replace_fields` | No | `true` | Whether to replace original host fields from the event. If set `false`, original host fields from the event are not replaced by host fields from `add_host_metadata`. |

