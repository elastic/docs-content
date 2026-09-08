The {{motlp}} stores OpenTelemetry data **without schema translation**, preserving OpenTelemetry semantic conventions and resource attributes in OTel-native format. Custom attributes are stored under `attributes.*` with dots preserved. It supports ingesting OTLP logs, metrics, and traces.

The {{apm-server-or-mis}} OTLP intake (the `.apm` endpoint) is a legacy path that **translates OTLP data to ECS format** before storage. Custom attributes land in `labels.*` with dots replaced by underscores. This path is not recommended for new users, and EDOT SDKs are not supported here.

For a full comparison of ingest paths and their data format implications, refer to [How your ingest path determines the data format](opentelemetry://reference/compatibility/data-streams.md#ingest-path-data-format).
