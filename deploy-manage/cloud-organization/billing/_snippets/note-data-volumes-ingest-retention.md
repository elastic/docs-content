:::{note}
Data volumes for ingest and retention are based on the fully enriched normalized data size at the end of the ingest pipeline, before {{es}} compression is performed, and will be higher than the volumes traditionally reported by {{es}} index size.

In addition, these volumes might be larger than those reported by cloud provider proxy logs for data going into {{es}}. This allows you to have flexibility in choosing your preferred ingest architecture for enrichment, whether it's through {{agent}}, {{ls}}, OpenTelemetry, or collectors — with no impact on the cost.
:::