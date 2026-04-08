---
navigation_title: Programmatic access
applies_to:
  stack: ga 9.1
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Query Attack Discovery indices with the Search API, ES|QL, and Kibana APIs, and learn how to guard integrations against injection risks.
---

# Query Attack Discovery data programmatically [attack-discovery-programmatic-access]

You can query Attack Discovery data directly to build custom dashboards, feed automated triage pipelines, export discoveries to external tools, or integrate Attack Discovery results with third-party SIEM and SOAR platforms. This page explains how to query the correct indices, provides example queries, and covers security considerations for integrations that consume Attack Discovery data.

## Prerequisites [attack-discovery-programmatic-prerequisites]

Before you query Attack Discovery data programmatically, make sure you have the following:

- **Index privileges**: Your role needs `read` and `view_index_metadata` privileges on the Attack Discovery alert indices. Refer to [Attack Discovery RBAC](/solutions/security/ai/attack-discovery.md#attack-discovery-rbac) for the full list of required privileges.
- **Authentication**: Use an [{{es}} API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) to authenticate requests. Scope the key to the minimum privileges your integration requires.
- **Use the `fields` parameter**: Don't rely on `_source` when querying alert indices. Use the [`fields` option](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) in the Search API instead, because alert index mappings can change between versions.

## Attack Discovery index aliases [attack-discovery-index-aliases]

{{es}} stores Attack Discovery alerts in dedicated indices, separate from detection rule alerts. Query the index *alias* rather than the internal backing indices directly. The alias automatically spans all backing indices as they roll over.

| Type | Pattern | Example |
|------|---------|---------|
| Alias (recommended) | `.alerts-security.attack.discovery.alerts-<space-id>` | `.alerts-security.attack.discovery.alerts-default` |
| Internal index | `.internal.alerts-security.attack.discovery.alerts-<space-id>-NNNNNN` | `.internal.alerts-security.attack.discovery.alerts-default-000001` |

Replace `<space-id>` with your {{kib}} space ID (for example, `default`). Don't add a dash or wildcard after the space ID.

For background on alert index naming conventions across all rule types, refer to [Query alert indices](/explore-analyze/alerting/alerts/query-alerts.md).

## Query with the Search API [attack-discovery-search-api]

Use the {{es}} [Search API](elasticsearch://reference/elasticsearch/rest-apis/search-your-data.md) to query Attack Discovery alerts directly. The following examples target the alias for the `default` {{kib}} space.

### Retrieve recent discoveries [ad-retrieve-recent]

Return the 10 most recent Attack Discovery alerts, sorted by timestamp:

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

- `.alerts-security.attack.discovery.alerts-default`: The index alias for Attack Discovery alerts in the `default` space.
- `fields`: Retrieves specific fields without relying on `_source`, which is the recommended approach for system indices.
- `@timestamp` sort: Returns the newest discoveries first.

### Filter by severity and time range [ad-filter-severity-time]

Return critical Attack Discovery alerts from the last 24 hours:

```json
GET /.alerts-security.attack.discovery.alerts-default/_search
{
  "size": 50,
  "query": {
    "bool": {
      "filter": [
        { "term": { "kibana.alert.severity": "critical" } },
        {
          "range": {
            "@timestamp": {
              "gte": "now-24h",
              "lte": "now"
            }
          }
        }
      ]
    }
  },
  "fields": [
    "kibana.alert.rule.name",
    "kibana.alert.severity",
    "host.name",
    "user.name",
    "@timestamp"
  ],
  "_source": false
}
```

- `kibana.alert.severity`: Filters by severity level (`low`, `medium`, `high`, or `critical`).
- `@timestamp` range: Restricts results to a specific time window. Adjust `gte` for your desired lookback period.

### Filter by status and host [ad-filter-status-host]

Return open Attack Discovery alerts for a specific host:

```json
GET /.alerts-security.attack.discovery.alerts-default/_search
{
  "size": 50,
  "query": {
    "bool": {
      "filter": [
        { "term": { "kibana.alert.workflow_status": "open" } },
        { "term": { "host.name": "web-server-01" } }
      ]
    }
  },
  "fields": [
    "kibana.alert.rule.name",
    "kibana.alert.severity",
    "kibana.alert.workflow_status",
    "host.name",
    "user.name",
    "@timestamp"
  ],
  "_source": false
}
```

- `kibana.alert.workflow_status`: Filters by triage status (`open`, `acknowledged`, or `closed`).
- `host.name`: Filters by the hostname associated with the discovery.

## Query with {{esql}} [attack-discovery-esql]

You can also use {{esql}} to query Attack Discovery data. The following example counts open discoveries grouped by severity:

```esql
FROM .alerts-security.attack.discovery.alerts-default
| WHERE kibana.alert.workflow_status == "open"
| STATS count = COUNT(*) BY kibana.alert.severity
| SORT count DESC
| LIMIT 10
```

You can run {{esql}} queries from **Discover**, **Timeline**, the [Dev Tools Console](elasticsearch://reference/query-languages/esql/esql-rest.md#esql-kibana-console), or the `POST /_query` REST endpoint.

## Query with the Attack Discovery API [attack-discovery-kibana-api]

{{kib}} provides purpose-built REST APIs for working with Attack Discovery data. These APIs return enriched discovery objects, including LLM-generated summaries, MITRE ATT&CK mappings, and entity information, that aren't available in the raw alert index documents.

The following endpoints are commonly used:

Find discoveries
:   `GET /api/attack_discovery/_find`. Search, filter, and paginate through saved discoveries. Supports parameters like `search` (free text), `status` (workflow status filter), `start`/`end` (time range), and `connector_names`.

Generate discoveries
:   `POST /api/attack_discovery/_generate`. Trigger a new discovery generation from alerts. Returns an `execution_uuid` you can use to track progress.

Get a generation
:   `GET /api/attack_discovery/generations/{execution_uuid}`. Retrieve the results and metadata for a specific generation.

For the full list of endpoints and parameters, refer to the [Attack Discovery API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-attack-discovery-api).

:::{note}
The Find and Generation APIs accept an `enable_field_rendering` parameter. When set to `true`, markdown fields include a `{{ field_name value }}` syntax used by {{kib}} to render interactive pivot links. If you're building a custom renderer, set this to `false` (the default) or implement dedicated handling for this syntax.
:::

## Security considerations for integrations [attack-discovery-security-considerations]

Attack Discovery data can contain values derived from adversary-controlled sources: hostnames, usernames, process names, and other fields that originate from raw alert data. LLM-generated fields like `detailsMarkdown` and `summaryMarkdown` can also reflect this untrusted content. When your integration passes this data to other systems, treat every field value as untrusted input.

The following sections describe common injection risks and how to mitigate them.

### Avoid KQL injection when building queries from discovery data [ad-kql-injection]

If your integration builds KQL query strings by interpolating values from Attack Discovery fields, an adversary who controls a field value could alter the query logic.

::::{warning}
Don't construct KQL queries by concatenating untrusted field values. Use structured {{es}} query filters instead.
::::

For example, suppose your integration pivots on a `host.name` value from a discovery to find related alerts:

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

If your integration passes field values from Attack Discovery alerts to shell commands, for example to run remediation scripts against a host, an adversary who controls the field value can inject arbitrary commands.

::::{warning}
Never interpolate untrusted values into shell command strings. Use parameterized APIs that don't invoke a shell interpreter.
::::

```python
import subprocess

host = discovery_fields["host.name"]

# UNSAFE: passes the value through a shell interpreter
subprocess.run(f"ssh {host} 'systemctl restart service'", shell=True)

# SAFE: passes arguments as a list, bypassing shell interpretation
subprocess.run(["ssh", host, "systemctl", "restart", "service"])
```

The unsafe pattern passes the entire string to `/bin/sh`, which interprets shell metacharacters in the `host` value. The safe pattern passes each argument directly to the `ssh` process without shell interpretation.

### Sanitize markdown content before rendering [ad-markdown-injection]

Attack Discovery responses from the {{kib}} API include LLM-generated markdown in fields such as `detailsMarkdown`, `summaryMarkdown`, and `entitySummaryMarkdown`. If your integration renders this markdown as HTML, unsanitized content could introduce:

- **Misleading links** that direct analysts to attacker-controlled sites
- **Tracking pixels** embedded as image references (for example, `![](https://attacker.example.com/pixel)`)
- **Raw HTML** if your markdown renderer doesn't strip it

To mitigate these risks:

- Use a markdown renderer that strips raw HTML tags by default.
- Validate or restrict link URLs to trusted domains before rendering.
- If you enabled the `enable_field_rendering` API parameter, implement dedicated parsing for the `{{ field_name value }}` syntax rather than passing it through to the HTML renderer.

### Guard against prompt injection in LLM pipelines [ad-prompt-injection]

If your integration forwards Attack Discovery content to an LLM for further analysis, for example to generate remediation recommendations, the discovery text might contain adversarial instructions designed to manipulate the model's behavior. This is possible because discovery content reflects alert data that can originate from attacker-controlled sources.

To reduce this risk:

- **Treat discovery content as untrusted data.** Don't insert it directly into the system prompt or instruction portion of your LLM request.
- **Use structured prompts with clear data boundaries.** Separate instructions from data so the LLM can distinguish between them. For example, wrap discovery content in explicit delimiters and instruct the model to treat delimited content as data only.
- **Limit the LLM's available actions.** If your pipeline allows the LLM to call tools or take actions, restrict what actions are available so that a manipulated response can't cause harm.
- **Use built-in anonymization.** [Elastic AI Assistant](/solutions/security/ai/ai-assistant.md) includes anonymization features that obfuscate sensitive field values before sending data to LLMs. Consider using these features when building pipelines that process discovery data.
