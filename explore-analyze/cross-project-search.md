---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
---

# Cross-project search [cross-project-search]

**{{cps-cap}}** lets you run a single search request against one or more of your projects. For example, you can use a {{cps}} to filter and analyze log data stored accross your linked projects.

## Prerequisites

* {{cps-cap}} requires linked projects. To set up linked projects, refer to [**TODO**]().
* To use {{cps}} with ES|QL, both the origin and linked projects must have the appropriate [subscription level](https://www.elastic.co/subscriptions).
* {{cps-cap}} requires [UIAM]() set up.

## Project linking



## Supported APIs [cps-supported-apis]

The following APIs support {{cps}}:

* [Async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit)
* [CAT count](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-cat-count)
* Datafeeds [PUT](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-ml-put-datafeed), [GET](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-ml-get-datafeeds), [DELETE](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-ml-delete-datafeed)
* [EQL search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search)
* [Field capabilities](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-field-caps)
* [Multi search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch)
* [Multi search template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch-template)
* [Painless execute API](elasticsearch://reference/scripting-languages/painless/painless-api-examples.md)
* PIT (point in time) [close](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-close-point-in-time), [open](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-open-point-in-time)
* [Reindex](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-reindex)
* [Resolve Index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index)
* [SQL](https://www.elastic.co/docs/api/doc/elasticsearch/v9/group/endpoint-sql)
* [Search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
* Search scroll [clear](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-clear-scroll), [run](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-scroll)
* [Search template](/solutions/search/search-templates.md)
* [Transforms](https://www.elastic.co/docs/api/doc/elasticsearch/v9/group/endpoint-transform)

### {{cps-cap}} specific APIs

**Project routing**: `_project_routing`

* [PUT](TODO)
* [GET](TODO)
* [DELETE](TODO)

**Project tags**: `_project/tags`

* [PUT](TODO)
* [GET](TODO)
* [DELETE](TODO)

## Limitations

## {{cps-cap}} examples