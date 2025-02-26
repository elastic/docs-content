---
navigation_title: "Outputs"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-output-configuration.html
---

# Configure outputs for standalone {{agent}}s [elastic-agent-output-configuration]


The `outputs` section of the `elastic-agent.yml` file specifies where to send data. You can specify multiple outputs to pair specific inputs with specific outputs.

This example configures two outputs: `default` and  `monitoring`:

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: [127.0.0.1:9200]
    api_key: "my_api_key"

  monitoring:
    type: elasticsearch
    api_key: VuaCfGcBCdbkQm-e5aOx:ui2lp2axTNmsyakw9tvNnw
    hosts: ["localhost:9200"]
    ca_sha256: "7lHLiyp4J8m9kw38SJ7SURJP4bXRZv/BNxyyXkCcE/M="
```

::::{note}
A default output configuration is required.

::::


{{agent}} currently supports these outputs:

* [{{es}}](/reference/ingestion-tools/fleet/elasticsearch-output.md)
* [Kafka](/reference/ingestion-tools/fleet/kafka-output.md)
* [{{ls}}](/reference/ingestion-tools/fleet/logstash-output.md)




