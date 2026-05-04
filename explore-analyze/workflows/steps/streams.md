---
navigation_title: Streams
applies_to:
  stack: preview 9.4+
  serverless: preview
description: Reference for the three Streams action steps that operate on Observability Streams from a workflow.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Streams action steps [workflows-streams-steps]

Streams action steps operate on Observability [Streams](/solutions/observability/streams/streams.md) from a workflow. Use them to list available streams, fetch a specific stream's configuration, or pull significant events from a stream's time window.

:::{warning}
Streams action steps, along with the Streams feature itself, are in technical preview in 9.4. Schemas and semantics can change in future releases. Use these steps for prototypes and investigation workflows; hold off on critical automation until Streams reaches GA.
:::

## Step types

- [`kibana.streams.list`](#kibana-streams-list): Enumerate available streams.
- [`kibana.streams.get`](#kibana-streams-get): Fetch a stream by name.
- [`kibana.streams.getSignificantEvents`](#kibana-streams-getsignificantevents): Pull significant events from a stream.

---

## `kibana.streams.list` [kibana-streams-list]

List every available stream in the current {{kib}} space. This step takes no parameters.

```yaml
- name: list_streams
  type: kibana.streams.list
```

## `kibana.streams.get` [kibana-streams-get]

Fetch a stream by name. The `name` is the human-readable stream identifier shown in the Kibana UI.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | `with` | string | Yes | Stream name. |

```yaml
- name: get_logs_stream
  type: kibana.streams.get
  with:
    name: "logs-default"
```

## `kibana.streams.getSignificantEvents` [kibana-streams-getsignificantevents]

Fetch significant events from a stream in a specified time range, optionally filtered by a query.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | `with` | string | Yes | Stream name. |
| `from` | `with` | string | No | Start of the time range. Accepts ISO timestamps (`2026-04-01T00:00:00Z`) or relative values (`now-1h`). |
| `to` | `with` | string | No | End of the time range. |
| `bucketSize` | `with` | string | No | Aggregation bucket size. |
| `query` | `with` | string | No | Filter query. |

```yaml
- name: recent_significant_events
  type: kibana.streams.getSignificantEvents
  with:
    name: "logs-default"
    from: "now-1h"
    to: "now"
```

## Related

- [Streams overview](/solutions/observability/streams/streams.md): The Observability Streams feature.
- [Kibana action steps](/explore-analyze/workflows/steps/kibana.md): The generic `kibana.request` for Kibana APIs that don't have a named step.
