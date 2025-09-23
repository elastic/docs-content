---
applies_to:
  serverless: preview
  stack: preview 9.1
---
# Dissect processor [streams-dissect-processor]

The dissect processor parses structured log messages and extracts fields from them. Unlike Grok, it does not use a set of predefined patterns to match the log messages. Instead, it uses a set of delimiters to split the log message into fields.
Dissect is much faster than Grok and is ideal for log messages that follow a consistent, structured format.

This functionality uses the {{es}} dissect pipeline processor. Refer to the [dissect processor](elasticsearch://reference/enrich-processor/dissect-processor.md) {{es}} documentation for more information.

To parse a log message, simply name the field and list the delimiters you want to use. The dissect processor will then split the log message into fields based on the delimiters provided.

Example:

Log Message
```
2025-04-04T09:04:45+00:00 ERROR 160.200.87.105 127.79.135.127 21582
```
Dissect Pattern
```
%{timestamp} %{log.level} %{source.ip} %{destination.ip} %{destination.port}
```