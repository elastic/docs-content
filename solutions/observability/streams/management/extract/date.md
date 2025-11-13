---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---

# Date processor [streams-date-processor]

The date processor parses dates from fields, and then uses the date or timestamp as the timestamp for the document.

To extract a timestamp field using the date processor:

1. Select **Create** → **Create processor**.
1. Select **Date** from the **Processor** menu.
1. Set the **Source Field** to the field containing the timestamp.
1. Set the **Format** field to one of the accepted date formats (ISO8602, UNIX, UNIX_MS, or TAI64N) or use a Java time pattern. Refer to the [example formats](#streams-date-examples) for more information.

This functionality uses the {{es}} date pipeline processor. Refer to the [date processor](elasticsearch://reference/enrich-processor/date-processor.md) {{es}} documentation for more information.

## Example formats [streams-date-examples]

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
You can set the following optional fields for the date processor in the **Advanced settings**:

| Field | Description|
| ------- | --------------- |
| Target field | The field that will hold the parsed date. Defaults to `@timestamp`. |
| Timezone | The timezone to use when parsing the date. Supports template snippets. Defaults to `UTC`. |
| Locale | The locale to use when parsing the date, relevant when parsing month names or weekdays. Supports template snippets. Defaults to `ENGLISH`. |
| Output format | The format to use when writing the date to `target_field`. Must be a valid Java time pattern. Defaults to `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`. |