---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Scripting [modules-scripting]

With scripting, you can evaluate custom expressions in {{es}}. For example, you can use a script to return a computed value as a field or evaluate a custom score for a query.

The default scripting language is [Painless](scripting/modules-scripting-painless.md). Additional `lang` plugins are available to run scripts written in other languages. You can specify the language of the script anywhere that scripts run.


## Available scripting languages [scripting-available-languages] 

Painless is purpose-built for {{es}}, can be used for any purpose in the scripting APIs, and provides the most flexibility. The other languages are less flexible, but can be useful for specific purposes.

| Language | Sandboxed | Required plugin | Purpose |
| --- | --- | --- | --- |
| [`painless`](scripting/modules-scripting-painless.md) | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | Built-in | Purpose-built for {{es}} |
| [`expression`](scripting/modules-scripting-expression.md) | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | Built-in | Fast custom ranking and sorting |
| [`mustache`](../solutions/search/search-templates.md) | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | Built-in | Templates |
| [`java`](scripting/modules-scripting-engine.md) | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | Not available | Expert API |

