---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-mapping.html
---

# Dynamic mapping [dynamic-mapping]

One of the most important features of {{es}} is that it tries to get out of your way and let you start exploring your data as quickly as possible. To index a document, you don’t have to first create an index, define a mapping type, and define your fields — you can just index a document and the index, type, and fields will display automatically:

```console
PUT data/_doc/1 <1>
{ "count": 5 }
```

1. Creates the `data` index, the `_doc` mapping type, and a field called `count` with data type `long`.


The automatic detection and addition of new fields is called *dynamic mapping*. The dynamic mapping rules can be customized to suit your purposes with:

[Dynamic field mappings](dynamic-field-mapping.md)
:   The rules governing dynamic field detection.

[Dynamic templates](dynamic-templates.md)
:   Custom rules to configure the mapping for dynamically added fields.

::::{tip} 
[Index templates](../templates.md) allow you to configure the default mappings, settings and aliases for new indices, whether created automatically or explicitly.
::::




