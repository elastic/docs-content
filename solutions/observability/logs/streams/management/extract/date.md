---
applies_to:
  serverless: preview
  stack: preview 9.1
---

# Date processor [streams-date-processor]

The date processor parses date strings and uses them as the timestamp of the document.

This functionality uses the {{es}} date pipeline processor. Refer to the [date processor](elasticsearch://reference/enrich-processor/date-processor.md) {{es}} documentation for more information.

## Examples

The following list provides some common examples of date formats and how to parse them.

**Common formats**
```
2025-04-04T09:04:45+00:00 => ISO8601
1618886400 => UNIX
1618886400123 => UNIX_MS
4000000049c9f0ca => TAI64N
```

**Custom formats**
```
2023-10-15 => yyyy-MM-dd
15/10/2023 => dd/MM/yyyy
10-15-2023 => MM-dd-yyyy
2023-288 => yyyy-DDD
15 Oct 2023 => dd MMM yyyy
Sunday, October 15, 2023 => EEEE, MMMM dd, yyyy
2023-10-15T14:30:00Z => yyyy-MM-dd'T'HH:mm:ssX
2023-10-15 14:30:00 => yyyy-MM-dd HH:mm:ss
```


## Optional fields [streams-date-optional-fields]
The following fields are optional for the date processor:

| Field | Description|
| ------- | --------------- |
| Target field | The field that will hold the parsed date. Defaults to `@timestamp`. |
| Timezone | The timezone to use when parsing the date. Supports template snippets. Defaults to `UTC`. |
| Locale | The locale to use when parsing the date, relevant when parsing month names or weekdays. Supports template snippets. Defaults to `ENGLISH`. |
| Output format | The format to use when writing the date to `target_field`. Must be a valid Java time pattern. Defaults to `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`. |