---
navigation_title: KV processor
applies_to:
    serverless: preview
---
# Key value processor [streams-kv-processor]

The key value (KV) processor allows you to extract key-value pairs from a field and assign them to a target field or the root of the document.

This functionality uses the {{es}} kv pipeline processor. Refer to [KV processor](elasticsearch://reference/enrich-processor/kv-processor.md) in the {{es}} docs for more information.

## Required fields [streams-kv-required-fields]

The KV processor requires the following fields:

| Field | Description|
| ------- | --------------- |
| Field | The field to be parsed.|
| Field split | Regex pattern used to delimit the key-value pairs. Typically a space character (" "). |
| Value split | Regex pattern used to delimit the key from the value. Typically an equals sign (=). |

## Optional fields [streams-kv-optional-fields]

The following fields are optional for the KV processor:

| Field | Description|
| ------- | --------------- |
| Target field | The field to assign the parsed key-value pairs to. If not specified, the key-value pairs are assigned to the root of the document. |
| Include keys | A list of extracted keys to include in the output. If not specified, all keys are included by default. Type and then hit "ENTER" to add keys. |
| Exclude keys | A list of extracted keys to exclude from the output. Type and then hit "ENTER" to add keys. |
| Prefix | A prefix to add to extracted keys. |
| Trim key | A string of characters to trim from extracted keys. |
| Trim value | A string of characters to trim from extracted values. |
| Strip brackets | Removes brackets ( (), <>, []) and quotes (', ") from extracted values.|
