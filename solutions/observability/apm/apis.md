---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-apis.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
---

# APM APIs [apm-apis]

:::{include} _snippets/apm-server-vs-mis.md
:::

There are two kinds of APIs related to Elastic APM:

|     |     |
| --- | --- |
| [APM UI API](/solutions/observability/apm/apm-ui-api.md) | {{kib}} APIs specific to working with the Applications UI including updating configuration options,  uploading real user monitoring (RUM) source maps, adding annotations, and more. |
| [APM Server API](/solutions/observability/apm/apm-server/api.md) | APIs for working with APM Server. These are mainly intake APIs that accept data from APM agents and are used primarily by APM agent developers. |
| [Observability Intake Serverless API](/solutions/observability/apm/managed-intake-service-event-api.md) | The managed intake service exposes an API endpoint to query general server information. This lightweight endpoint is useful as a server up/down health check. This API is exclusively for APM agent developers. |

