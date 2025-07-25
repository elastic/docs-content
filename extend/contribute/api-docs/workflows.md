---
navigation_title: API docs by product
---
# How each Elastic product manages API docs

Each product has a specific process for producing OpenAPI files in the respective repositories. This page provides a quick reference to help you navigate to the right resources.

:::{important}
Some of the content on this page is relevant to Elastic employees only and therefore some links are to private repos.
:::

## Quick reference

| Product | Repo | OpenAPI spec file | Live docs |
|---------|------------|---------------------|-----------|
| Elasticsearch | [elastic/elasticsearch-specification](https://github.com/elastic/elasticsearch-specification) | [elasticsearch-openapi.json](https://github.com/elastic/elasticsearch-specification/blob/main/output/openapi/elasticsearch-openapi.json) | [elasticsearch](https://www.elastic.co/docs/api/doc/elasticsearch) |
| Elasticsearch Serverless | [elastic/elasticsearch-specification](https://github.com/elastic/elasticsearch-specification) | [elasticsearch-serverless-openapi.json](https://github.com/elastic/elasticsearch-specification/blob/main/output/openapi/elasticsearch-serverless-openapi.json) | [elasticsearch-serverless](https://www.elastic.co/docs/api/doc/elasticsearch-serverless) |
| Kibana | [elastic/kibana](https://github.com/elastic/kibana/tree/main/oas_docs#kibana-api-reference-documentation) | [bundle.json](https://github.com/elastic/kibana/blob/main/oas_docs/bundle.json) | [kibana](https://www.elastic.co/docs/api/doc/kibana) |
| Kibana Serverless | [elastic/kibana](https://github.com/elastic/kibana/tree/main/oas_docs#kibana-api-reference-documentation) | [kibana.serverless.yaml](https://github.com/elastic/kibana/blob/main/oas_docs/output/kibana.serverless.yaml) | [serverless](https://www.elastic.co/docs/api/doc/serverless) |
| Elastic Cloud | [elastic/cloud](https://github.com/elastic/cloud) (private) | [apidocs-user.json](https://github.com/elastic/cloud/blob/master/scala-services/adminconsole/src/main/resources/apidocs-user.json) | [cloud](https://www.elastic.co/docs/api/doc/cloud) |
| Elastic Cloud Enterprise | [elastic/cloud](https://github.com/elastic/cloud) (private) | [apidocs.json](https://github.com/elastic/cloud/blob/master/scala-services/adminconsole/src/main/resources/apidocs.json) | [cloud-enterprise](https://www.elastic.co/docs/api/doc/cloud-enterprise) |
| Elastic Cloud Billing | [elastic/cloud](https://github.com/elastic/cloud) (private) | [billing-service.external.yaml](https://github.com/elastic/cloud/blob/master/python-services-v3/openapi/billing-service.external.yaml) | [cloud-billing](https://www.elastic.co/docs/api/doc/cloud-billing) |
| Elastic Cloud Serverless | Multiple repos (private) | Multiple files | [elastic-cloud-serverless](https://www.elastic.co/docs/api/doc/elastic-cloud-serverless) |
| Logstash | [elastic/logstash](https://github.com/elastic/logstash) | [logstash-api.yaml](https://github.com/elastic/logstash/blob/main/docs/static/spec/openapi/logstash-api.yaml) | [logstash](https://www.elastic.co/docs/api/doc/logstash) |
| Observability Intake | [elastic/apm-managed-service](https://github.com/elastic/apm-managed-service) (private) | [bundled-apm-mis-openapi.json](https://github.com/elastic/apm-managed-service/blob/main/docs/spec/openapi/bundled-apm-mis-openapi.json) | [observability-serverless](https://www.elastic.co/docs/api/doc/observability-serverless) |

