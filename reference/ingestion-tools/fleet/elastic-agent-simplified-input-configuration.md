---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-simplified-input-configuration.html
---

# Simplified log ingestion [elastic-agent-simplified-input-configuration]

There is a simplified option for ingesting log files with {{agent}}. The simplest input configuration to ingest the file `/var/log/my-application/log-file.log` is:

```yaml
inputs:
  - type: filestream <1>
    id: unique-id-per-input <2>
    paths: <3>
      - /var/log/my-application/log-file.log
```

1. The input type must be `filestream`.
2. A unique ID for the input.
3. An array containing all log file paths.


For other custom options to configure the input, refer to the [filestream input](beats://docs/reference/filebeat/filebeat-input-filestream.md) in the {{filebeat}} documentation.

