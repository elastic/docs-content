---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-work-with-apis.html
---

# Tools and APIs [ec-work-with-apis]

Most Elastic resources can be accessed and managed through RESTful APIs. While the {{ecloud}} API is used to manage your deployments and their components, the Elasticsearch and Kibana APIs provide direct access to your data and your visualizations, respectively.

{{ecloud}} API
:   You can use the {{ecloud}} API to manage your deployments and all of the resources associated with them. This includes performing deployment CRUD operations, scaling or autoscaling resources, and managing traffic filters, deployment extensions, remote clusters, and Elastic Stack versions. You can also access cost data by deployment and by organization.

    To learn more about the {{ecloud}} API, read through the [API overview](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-api-restful.md), try out some [getting started examples](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-api-examples.md), and check our [API reference documentation](https://www.elastic.co/docs/api/doc/cloud).

    Calls to the {{ecloud}} API are subject to [Rate limiting](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-api-rate-limiting.md).


Elasticsearch APIs
:   This set of APIs allows you to interact directly with the Elasticsearch nodes in your deployment. You can ingest data, run search queries, check the health of your clusters, manage snapshots, and more.

    To use these APIs on {{ecloud}} read our topic [Access the API console](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-api-console.md), and to learn about all of the available endpoints check the [Elasticsearch API reference documentation](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/index.md).

    Some [restrictions](../deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-apis-elasticsearch) apply when using the Elasticsearch APIs on {{ecloud}}.


Kibana APIs
:   Many Kibana features can be accessed through these APIs, including Kibana objects, patterns, and dashboards, as well as user roles and user sessions. You can use these APIs to configure alerts and actions, and to access health details for the Kibana Task Manager.

    The Kibana APIs cannot be accessed directly from the {{ecloud}} Console; you need to use `curl` or another HTTP tool to connect. Check the [Kibana API reference documentation](https://www.elastic.co/guide/en/kibana/current/api.html) to learn about using the APIs and for details about all available endpoints.

    Some [restrictions](../deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-apis-kibana) apply when using these APIs with Kibana on {{ecloud}} as compared to an on-prem installation.


Other Products
:   Most other Elastic products have APIs to support machine-to-machine operations. You can find the documentation for these at the following links:

    * [APM event intake API Reference](/solutions/observability/apps/elastic-apm-events-intake-api.md)
    * [App Search API Reference](https://www.elastic.co/guide/en/app-search/current/api-reference.html)
    * [Elastic Security APIs](https://www.elastic.co/guide/en/security/current/security-apis.html)
    * [Fleet APIs](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/fleet-api-docs.md)
    * [Logstash APIs](https://www.elastic.co/guide/en/logstash/current/monitoring-logstash.html)
    * [Workplace Search API Reference](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-api-overview.html)



