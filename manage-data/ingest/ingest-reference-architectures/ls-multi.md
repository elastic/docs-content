---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/ls-multi.html
products:
  - id: elastic-agent
  - id: logstash
---

# Elastic Agent to Logstash for routing to multiple Elasticsearch clusters and additional destinations [ls-multi]

:::{image} /manage-data/images/ingest-ea-ls-multi.png
:alt: Image showing {{agent}} collecting and routing data to multiple destinations
:::

Ingest model
:   {{agent}} to {{ls}} to {{es}} clusters and additional destinations

Use when
:   Data collected by {{agent}} needs to be routed to different {{es}} clusters or non-{{es}} destinations depending on the content

Example
:   Let’s take an example of a Windows workstation, for which we are collecting different types of logs using the System and Windows integrations. These logs need to be sent to different {{es}} clusters and to S3 for backup and a mechanism to send it to other destinations such as different SIEM solutions. In addition, the {{es}} destination is derived based on the type of data stream and an organization identifier.

    In such use cases, agents send the data to {{ls}} as a routing mechanism to different destinations. The System and Windows integrations must be installed on all {{es}} clusters to which the data is routed.


Sample config
:   ```ruby
input {
  elastic_agent {
    port => 5044
  }
}
filter {
  translate {
    source => "[http][host]"
    target => "[@metadata][tenant]"
    dictionary_path => "/etc/conf.d/logstash/tenants.yml"
  }
}
output {
  if [@metadata][tenant] == "tenant01" {
    elasticsearch {
      cloud_id => "<cloud id>"
      api_key => "<api key>"
    }
  } else if [@metadata][tenant] == "tenant02" {
    elasticsearch {
      cloud_id => "<cloud id>"
      api_key => "<api key>"
    }
  }
}
```



## Resources [multi-resources]

Info on configuring {{agent}}:

* [Fleet and Elastic Agent Guide](/reference/fleet/index.md)
* [Configuring outputs for {{agent}}](/reference/fleet/elastic-agent-output-configuration.md)

Info on {{ls}} and {{ls}} outputs:

* [{{ls}} Reference](logstash://reference/index.md)
* [{{ls}} {{es}} output plugin](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md)
* [{{ls}} output plugins](logstash-docs-md://lsr/output-plugins.md)

Info on {{es}}:

* [{{es}} Guide](elasticsearch://reference/index.md)

