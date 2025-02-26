---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/fields-reference.html
---

# Fields and object schemas [fields-reference]

This section lists Elastic Common Schema (ECS) fields the Logs and Infrastructure apps use to display data.

ECS is an open source specification that defines a standard set of fields to use when storing event data in {{es}}, such as logs and metrics.

Beat modules (for example, [{{filebeat}} modules](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-modules.md)) are ECS-compliant, so manual field mapping is not required, and all data is populated automatically in the Logs and Infrastructure apps. If you cannot use {{beats}}, map your data to [ECS fields](ecs://docs/reference/ecs-converting.md)). You can also try using the experimental [ECS Mapper](https://github.com/elastic/ecs-mapper) tool.

This reference covers:

* [Logs Explorer fields](/reference/observability/fields-and-object-schemas/logs-app-fields.md)
* [{{infrastructure-app}} fields](/reference/observability/fields-and-object-schemas/metrics-app-fields.md)



