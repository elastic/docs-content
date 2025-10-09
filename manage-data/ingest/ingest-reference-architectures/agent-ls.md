---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/agent-ls.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elastic-agent
  - id: logstash
---

# Elastic Agent to Logstash to Elasticsearch [agent-ls]

:::{image} /manage-data/images/ingest-ea-ls-es.png
:alt: Image showing {{agent}} to {{ls}} to {{es}}
:::

Ingest models
:   {{agent}} to {{es}} using {{ls}} for advanced use cases such as enrichment, buffering, network bridging, multiple endpoints


## {{agent}} to {{ls}} to {{es}} architectures [agent-ls-flavors]

* [{{agent}} to {{ls}} (for enrichment) to {{es}}](ls-enrich.md)
* [{{agent}} to {{ls}} to {{es}}: {{ls}} Persistent Queue (PQ) for buffering](lspq.md)
* [{{agent}} to {{ls}} to {{es}}: {{ls}} as a proxy](ls-networkbridge.md)
* [{{agent}} to {{ls}} for routing to multiple {{es}} clusters and additional destinations](ls-multi.md)





