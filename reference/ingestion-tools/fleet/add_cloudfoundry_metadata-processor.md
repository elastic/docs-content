---
navigation_title: "add_cloudfoundry_metadata"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_cloudfoundry_metadata-processor.html
---

# Add Cloud Foundry metadata [add_cloudfoundry_metadata-processor]


The `add_cloudfoundry_metadata` processor annotates each event with relevant metadata from Cloud Foundry applications.

For events to be annotated with Cloud Foundry metadata, they must have a field called `cloudfoundry.app.id` that contains a reference to a Cloud Foundry application, and the configured Cloud Foundry client must be able to retrieve information for the application.

Each event is annotated with:

* Application Name
* Space ID
* Space Name
* Organization ID
* Organization Name

::::{note}
Pivotal Application Service and Tanzu Application Service include this metadata in all events from the firehose since version 2.8. In these cases the metadata in the events is used, and `add_cloudfoundry_metadata` processor doesn’t modify these fields.
::::


For efficient annotation, application metadata retrieved by the Cloud Foundry client is stored in a persistent cache on the filesystem. This is done so the metadata can persist across restarts of {{agent}} and its underlying programs. For control over this cache, use the `cache_duration` and `cache_retry_delay` settings.


## Example [_example_3]

```yaml
  - add_cloudfoundry_metadata:
      api_address: https://api.dev.cfdev.sh
      client_id: uaa-filebeat
      client_secret: verysecret
      ssl:
        verification_mode: none
      # To connect to Cloud Foundry over verified TLS you can specify a client and CA certificate.
      #ssl:
      #  certificate_authorities: ["/etc/pki/cf/ca.pem"]
      #  certificate:              "/etc/pki/cf/cert.pem"
      #  key:                      "/etc/pki/cf/cert.key"
```


## Configuration settings [_configuration_settings_2]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `api_address` | No | `http://api.bosh-lite.com` | URL of the Cloud Foundry API. |
| `doppler_address` | No | `${api_address}/v2/info` | URL of the Cloud Foundry Doppler Websocket. |
| `uaa_address` | No | `${api_address}/v2/info` | URL of the Cloud Foundry UAA API. |
| `rlp_address` | No | `${api_address}/v2/info` | URL of the Cloud Foundry RLP Gateway. |
| `client_id` | Yes |  | Client ID to authenticate with Cloud Foundry. |
| `client_secret` | Yes |  | Client Secret to authenticate with Cloud Foundry. |
| `cache_duration` | No | `120s` | Maximum amount of time to cache an application’s metadata. |
| `cache_retry_delay` | No | `20s` | Time to wait before trying to obtain an application’s metadata again in case of error. |
| `ssl` | No |  | SSL configuration to use when connecting to Cloud Foundry. For a list ofavailable settings, refer to [SSL/TLS](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md), specificallythe settings under [Table 7, Common configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#common-ssl-options) and [Table 8, Client configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#client-ssl-options). |

