You need:

- An Elastic deployment that can ingest metrics.
- An API key for the ingest path you use. Managed inputs, the Managed OTLP and Managed Prometheus Remote Write endpoints that {{ecloud}} runs for you, authenticate with the `event:write` privilege for the `apm` application. The {{es}} remote write endpoint authenticates with an API key that can ingest metrics.
- Your existing pipeline left running. Send data to both systems until you have rebuilt the queries, dashboards, and alerts you rely on.
