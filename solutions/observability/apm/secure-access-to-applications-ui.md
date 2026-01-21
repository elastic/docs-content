---
navigation_title: Secure access to the Applications UI
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-app-users.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Secure access to the Applications UI [apm-app-users]

Use role-based access control to grant users access to secured resources. The roles that you set up depend on your organization’s security requirements and the minimum privileges required to use specific features.

{{es-security-features}} provides [built-in roles](elasticsearch://reference/elasticsearch/roles.md) that grant a subset of the privileges needed by APM users. When possible, assign users the built-in roles to minimize the affect of future changes on your security strategy. If no built-in role is available, you can assign users the privileges needed to accomplish a specific task. In general, there are three types of privileges you’ll work with:

* **Elasticsearch cluster privileges**: Manage the actions a user can perform against your cluster.
* **Elasticsearch index privileges**: Control access to the data in specific indices your cluster.
* **Kibana feature privileges**: Grant users write or read access to features and apps within Kibana.

Select your use-case to get started:

* [Create an APM reader user](/solutions/observability/apm/ui-user-reader.md)
* [Create an annotation user](/solutions/observability/apm/ui-user-annotation.md)
* [Create a central config user](/solutions/observability/apm/ui-user-central-config.md)
* [Create a storage explorer user](/solutions/observability/apm/ui-user-storage-explorer.md)
* [Create an API user](/solutions/observability/apm/ui-user-api.md)
