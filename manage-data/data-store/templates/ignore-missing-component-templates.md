---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ignore_missing_component_templates.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_usage_example.html
applies_to:
  stack: ga
  serverless: ga
---

# Ignore missing component templates

% What needs to be done: Refine

% GitHub issue: docs-projects#372

% Scope notes: Combine with "Usage example" subpage.

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/elasticsearch/elasticsearch-reference/ignore_missing_component_templates.md
% - [x] ./raw-migrated-files/elasticsearch/elasticsearch-reference/_usage_example.md

When an index template references a component template that might not exist, the `ignore_missing_component_templates` configuration option can be used. With this option, every time a data stream is created based on the index template, the existence of the component template will be checked. If it exists, it will used to form the index’s composite settings. If it is missing, it will be ignored.

The following example demonstrates how this configuration option works.

## Example: Use the `ignore_missing_component_templates` option

In this example, an index template and one component template are created. The index template references two component templates, but only one exists.

Suppose the `logs-foo_component1` component template is created *before* the index template:

```console
PUT _component_template/logs-foo_component1
{
  "template": {
    "mappings": {
      "properties": {
        "host.name": {
          "type": "keyword"
        }
      }
    }
  }
}
```

Next, an index template is created, referencing two component templates:

```JSON
  "composed_of": ["logs-foo_component1", "logs-foo_component2"]
```

Since only the `logs-foo_component1` component template was created previously, the `logs-foo_component2` component template is missing. The following entry is added to the configuration:

```JSON
  "ignore_missing_component_templates": ["logs-foo_component2"],
```

The `logs-foo` index template will successfully be created, but it will not validate that `logs-foo_component2` exists:

```console
PUT _index_template/logs-foo
{
  "index_patterns": ["logs-foo-*"],
  "data_stream": { },
  "composed_of": ["logs-foo_component1", "logs-foo_component2"],
  "ignore_missing_component_templates": ["logs-foo_component2"],
  "priority": 500
}
```
%  TEST[continued]

A data stream can be created based on this template:

```console
PUT _data_stream/logs-foo-bar
```
%  TEST[continued]
The mappings of the data stream will contain the `host.name` field.

The missing component template can be added later:

```console
PUT _component_template/logs-foo_component2
{
  "template": {
    "mappings": {
      "properties": {
        "host.ip": {
          "type": "ip"
        }
      }
    }
  }
}
```
%  TEST[continued]

This will not have an immediate effect on the data stream. The mapping `host.ip` will only show up in the data stream mappings when the data stream is rolled over automatically next time or a manual rollover is triggered:

```console
POST logs-foo-bar/_rollover
```
%  TEST[continued]
%  TEST[teardown:data_stream_cleanup]

