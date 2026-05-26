Streams supports the following processors:

- [**Append**](../observability/streams/management/extract/append.md): Adds a value to an existing array field, or creates the field as an array if it doesn't exist.
- [**Concat**](../observability/streams/management/extract/concat.md): Concatenates a mix of field values and literal strings into a single field.
- [**Convert**](../observability/streams/management/extract/convert.md): Converts a field in the currently ingested document to a different type, such as converting a string to an integer.
- [**Date**](../observability/streams/management/extract/date.md): Converts date strings into timestamps, with options for timezone, locale, and output formatting.
- [**Dissect**](../observability/streams/management/extract/dissect.md): Extracts fields from structured log messages using defined delimiters instead of patterns, making it faster than Grok and ideal for consistently formatted logs.
- [**Drop**](../observability/streams/management/extract/drop.md): Drops the document without raising any errors. This is useful to prevent the document from getting indexed based on a condition.
- [**Enrich**](../observability/streams/management/extract/enrich.md): Adds data from an enrich policy to incoming documents, such as geographic coordinates from an IP address or account details from a user ID.
- [**Grok**](../observability/streams/management/extract/grok.md): Extracts fields from unstructured log messages using predefined or custom patterns, supports multiple match attempts in sequence, and can automatically generate patterns with an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
- [**Join**](../observability/streams/management/extract/join.md): Concatenates the values of multiple fields with a delimiter.
- [**Lowercase**](../observability/streams/management/extract/lowercase.md): Converts a string field to lowercase.
- [**Math**](../observability/streams/management/extract/math.md): Evaluates arithmetic or logical expressions.
- [**Network direction**](../observability/streams/management/extract/network-direction.md): Determines network traffic direction based on source and destination IP addresses.
- [**Redact**](../observability/streams/management/extract/redact.md): Redacts sensitive data in a string field by matching grok patterns.
- [**Remove**](../observability/streams/management/extract/remove.md): Removes existing fields or removes fields by prefix.
- [**Rename**](../observability/streams/management/extract/rename.md): Changes the name of a field, moving its value to a new field name and removing the original.
- [**Replace**](../observability/streams/management/extract/replace.md): Replaces parts of a string field according to a regular expression pattern with a replacement string.
- [**Set**](../observability/streams/management/extract/set.md): Assigns a specific value to a field, creating the field if it doesn't exist or overwriting its value if it does.
- [**Trim**](../observability/streams/management/extract/trim.md): Removes leading and trailing whitespace from a string field.
- [**Uppercase**](../observability/streams/management/extract/uppercase.md): Converts a string field to uppercase.

### Processor limitations and inconsistencies [streams-processor-inconsistencies]

Streams exposes a [Streamlang](../observability/streams/management/streamlang.md) configuration, but internally it relies on {{es}} ingest pipeline processors and ES|QL. Streamlang doesn't always have 1:1 parity with the ingest processors because it needs to support options that work in both ingest pipelines and ES|QL. In most cases, you won't need to worry about these details, but the underlying design decisions still affect the UI and available configuration options. The following are some limitations and inconsistencies when using Streamlang processors:

- **Consistently typed fields**: ES|QL requires one consistent type per column, so workflows that produce mixed types across documents won't transpile.
- **Conversion of types**: ES|QL and ingest pipelines accept different conversion combinations and strictness (especially for strings), so `convert` can behave differently across targets.
- **Multi-value commands/functions**: Fields can contain one or multiple values. ES|QL and ingest processors don't always handle these cases the same way. For example, grok in ES|QL handles multiple values automatically, while the grok processor does not
- **Conditional execution**: ES|QL's enforced table shape limits conditional casting, parsing, and wildcard field operations that ingest pipelines can do per-document.
- **Arrays of objects / flattening**: Ingest pipelines preserve nested JSON arrays, while ES|QL flattens to columns, so operations like rename and delete on parent objects can differ or fail.