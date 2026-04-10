---
navigation_title: Programmatic access
applies_to:
  stack: ga 9.1
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Query Attack Discovery indices with the Search API, ES|QL, and Kibana APIs, and learn how to guard against injection risks.
---

# Query Attack Discovery data programmatically [attack-discovery-programmatic-access]

You can query Attack Discovery data directly to build custom dashboards, feed automated triage pipelines, export discoveries to external tools, or integrate Attack Discovery results with third-party SIEM and SOAR platforms. This page explains how to query the correct indices, provides example queries, and covers security considerations for consuming Attack Discovery data.

## Prerequisites [attack-discovery-programmatic-prerequisites]

Before you query Attack Discovery data programmatically, make sure you have the following:

- **Index privileges**: `read` and `view_index_metadata` privileges on the Attack Discovery alert indices. Refer to [Attack Discovery RBAC](/solutions/security/ai/attack-discovery.md#attack-discovery-rbac) for the full list of required privileges.
- **Authentication**: An [{{es}} API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) to authenticate API requests. Scope the key to the minimum required privileges.

## Attack Discovery index aliases [attack-discovery-index-aliases]

Attack Discovery alerts use a dedicated index alias, separate from detection rule alerts:

`.alerts-security.attack.discovery.alerts-<space-id>`

Replace `<space-id>` with your {{kib}} space ID (for example, `default`). Always query the alias rather than the internal backing indices. For background on alert index naming conventions, including backing index patterns and rollover behavior, refer to [Query alert indices](/explore-analyze/alerting/alerts/query-alerts.md).

## Query with the Search API [attack-discovery-search-api]

Use the {{es}} [Search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) to query Attack Discovery alerts. The following example retrieves the 10 most recent alerts from the `default` {{kib}} space:

```json
GET /.alerts-security.attack.discovery.alerts-default/_search
{
  "size": 10,
  "query": {
    "match_all": {}
  },
  "fields": [
    "kibana.alert.rule.name",
    "kibana.alert.severity",
    "kibana.alert.workflow_status",
    "host.name",
    "user.name",
    "@timestamp"
  ],
  "_source": false,
  "sort": [
    { "@timestamp": { "order": "desc" } }
  ]
}
```

:::{tip}
Use the [`fields` option](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) instead of `_source` when querying alert indices. Alert index mappings can change between versions, and `fields` handles this more reliably.
:::

For additional query patterns (filtering by time range, severity, status, and more), refer to [Query alert indices](/explore-analyze/alerting/alerts/query-alerts.md#_sample_queries) and adapt those examples by replacing the index pattern with the Attack Discovery alias. You can also use [{{esql}}](/solutions/security/detect-and-alert/query-alert-indices.md#example_queries) with the same alias. For a list of common alert fields, refer to [Common alert fields](/solutions/security/detect-and-alert/query-alert-indices.md#common-alert-fields).

## Query with the Attack Discovery API [attack-discovery-kibana-api]

Elastic provides REST APIs for working with Attack Discovery data:

- `GET /api/attack_discovery/_find`: Search, filter, and paginate through saved discoveries.
- `POST /api/attack_discovery/_generate`: Trigger a new discovery generation from alerts.
- `GET /api/attack_discovery/generations/{execution_uuid}`: Retrieve results for a specific generation.

For the full list of endpoints and parameters, refer to the [Attack Discovery API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-attack-discovery-api).

:::{note}
The Find and Generate APIs accept an `enable_field_rendering` parameter. When set to `true`, markdown fields include a `{{ field_name value }}` syntax used by {{kib}} to render interactive pivot links. If you're building a custom renderer, set this to `false` (the default) or implement dedicated handling for this syntax.
:::

## Security considerations [attack-discovery-security-considerations]

Attack Discovery data can contain values derived from adversary-controlled sources: hostnames, usernames, process names, and other fields that originate from raw alert data. LLM-generated fields like `detailsMarkdown` and `summaryMarkdown` can also reflect this untrusted content. When you pass this data to other systems, treat every field value as untrusted input.

The following sections describe common injection risks and how to mitigate them.

### Avoid KQL injection when building queries from discovery data [ad-kql-injection]

If you build KQL query strings by interpolating values from Attack Discovery fields, an adversary who controls a field value could alter the query logic.


For example, suppose you use a `host.name` value from a discovery to find related alerts:

```python
# UNSAFE: field value is interpolated directly into a KQL string
host = discovery_fields["host.name"]
kql = f'host.name: "{host}" AND kibana.alert.workflow_status: "open"'
```

If an adversary sets the `host.name` value to `" OR _id: "`, the resulting KQL becomes `host.name: "" OR _id: "" AND kibana.alert.workflow_status: "open"`, which changes the query's intended scope.

Instead, use {{es}} `term` filters, which treat the value as a literal and don't interpret query syntax:

```python
query = {
    "bool": {
        "filter": [
            {"term": {"host.name": host}},
            {"term": {"kibana.alert.workflow_status": "open"}}
        ]
    }
}
```

### Avoid shell injection when running automated actions [ad-shell-injection]

If you pass field values from Attack Discovery alerts to shell commands, for example to run remediation scripts against a host, an adversary who controls the field value can inject arbitrary commands.


```python
import subprocess

host = discovery_fields["host.name"]

# UNSAFE: passes the value through a shell interpreter
subprocess.run(f"ssh {host} 'systemctl restart service'", shell=True)

# SAFE: passes arguments as a list, bypassing shell interpretation
subprocess.run(["ssh", host, "systemctl", "restart", "service"])
```

The unsafe pattern passes the entire string to `/bin/sh`, which interprets shell metacharacters in the `host` value. The safe pattern passes each argument directly to the `ssh` process without shell interpretation.
