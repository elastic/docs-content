---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-kafka-es.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elastic-agent
---

# Elastic Agent to Elasticsearch with Kafka as middleware message queue [agent-kafka-es]

:::{image} /manage-data/images/ingest-ea-kafka.png
:alt: Image showing {{agent}} collecting data and using Kafka as a message queue enroute to {{es}}
:::

Ingest models
:   [{{agent}} to {{ls}} to Kafka to {{ls}} to {{es}}: Kafka as middleware message queue](agent-kafka-ls.md).<br> {{ls}} reads data from Kafka and routes it to {{es}} clusters and other destinations.

    [{{agent}} to {{ls}} to Kafka to Kafka ES Sink to {{es}}: Kafka as middleware message queue](agent-kafka-essink.md).<br> Kafka ES sink connector reads from Kafka and writes to {{es}}.


Use when
:   You are standardizing on Kafka as middleware message queue between {{agent}} and {{es}}

Notes
:   The transformation from raw data to Elastic Common Schema (ECS) and any other enrichment can be handled by {{ls}} as described in [{{agent}} to {{ls}} (for enrichment) to {{es}}](ls-enrich.md).


## {{agent}} with Kafka as middleware message queue architectures [agent-kafka-es-flavors]

* [{{agent}} to {{ls}} to Kafka to {{ls}} to {{es}}: Kafka as middleware message queue](agent-kafka-ls.md)
* [{{agent}} to {{ls}} to Kafka to Kafka ES Sink to {{es}}: Kafka as middleware message queue](agent-kafka-essink.md)



