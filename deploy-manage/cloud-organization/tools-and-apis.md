---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-work-with-apis.html
---

# Tools and APIs [ec-work-with-apis]

Most Elastic resources can be accessed and managed through RESTful APIs. While the Elasticsearch Service API is used to manage your deployments and their components, the Elasticsearch and Kibana APIs provide direct access to your data and your visualizations, respectively.

Elasticsearch Service API
:   You can use the Elasticsearch Service API to manage your deployments and all of the resources associated with them. This includes performing deployment CRUD operations, scaling or autoscaling resources, and managing traffic filters, deployment extensions, remote clusters, and Elastic Stack versions. You can also access cost data by deployment and by organization.

    To learn more about the Elasticsearch Service API, read through the [API overview](https://www.elastic.co/guide/en/cloud/current/ec-restful-api.html), try out some [getting started examples](https://www.elastic.co/guide/en/cloud/current/ec-api-examples.html), and check our [API reference documentation](https://www.elastic.co/docs/api/doc/cloud).

    Calls to the  Elasticsearch Service API are subject to [Rate limiting](https://www.elastic.co/guide/en/cloud/current/ec-api-rate-limiting.html).


Elasticsearch APIs
:   This set of APIs allows you to interact directly with the Elasticsearch nodes in your deployment. You can ingest data, run search queries, check the health of your clusters, manage snapshots, and more.

    To use these APIs in Elasticsearch Service read our topic [Access the Elasticsearch API console](https://www.elastic.co/guide/en/cloud/current/ec-api-console.html), and to learn about all of the available endpoints check the [Elasticsearch API reference documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html).

    Some [restrictions](../deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-apis-elasticsearch) apply when using the Elasticsearch APIs in Elasticsearch Service.


Kibana APIs
:   Many Kibana features can be accessed through these APIs, including Kibana objects, patterns, and dashboards, as well as user roles and user sessions. You can use these APIs to configure alerts and actions, and to access health details for the Kibana Task Manager.

    The Kibana APIs cannot be accessed directly from the Elasticsearch Service console; you need to use `curl` or another HTTP tool to connect. Check the [Kibana API reference documentation](https://www.elastic.co/guide/en/kibana/current/api.html) to learn about using the APIs and for details about all available endpoints.

    Some [restrictions](../deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-apis-kibana) apply when using these APIs with an Elasticsearch Service Kibana instance as compared to an on-prem installation.


Other Products
:   Most other Elastic products have APIs to support machine-to-machine operations. You can find the documentation for these at the following links:

    * [APM event intake API Reference](/solutions/observability/apps/elastic-apm-events-intake-api.md)
    * [App Search API Reference](https://www.elastic.co/guide/en/app-search/current/api-reference.html)
    * [Elastic Security APIs](https://www.elastic.co/guide/en/security/current/security-apis.html)
    * [Enterprise Search management APIs](https://www.elastic.co/guide/en/enterprise-search/current/management-apis.html)
    * [Fleet APIs](https://www.elastic.co/guide/en/fleet/current/fleet-api-docs.html)
    * [Logstash APIs](https://www.elastic.co/guide/en/logstash/current/monitoring-logstash.html)
    * [Workplace Search API Reference](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-api-overview.html)



