---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-data-model-metadata.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
---

# Metadata [apm-data-model-metadata]

Metadata can enrich your events and make application performance monitoring even more useful. Let’s explore the different types of metadata that Elastic APM offers.

## Labels [apm-data-model-labels]

Labels add **indexed** information to transactions, spans, and errors. Indexed means the data is searchable and aggregatable in {{es}}. Add additional key-value pairs to define multiple labels.

* Indexed: Yes
* {{es}} type: [object](elasticsearch://reference/elasticsearch/mapping-reference/object.md)
* {{es}} field: `labels`
* Applies to: [Transactions](/solutions/observability/apm/transactions.md) | [Spans](/solutions/observability/apm/spans.md) | [Errors](/solutions/observability/apm/errors.md)

Label values can be a string, boolean, or number, although some agents only support string values at this time. Because labels for a given key, regardless of agent used, are stored in the same place in {{es}}, all label values of a given key must have the same data type. Multiple data types per key will throw an exception, for example: `{foo: bar}` and `{foo: 42}` is not allowed.

::::{important}
Avoid defining too many user-specified labels. Defining too many unique fields in an index is a condition that can lead to a [mapping explosion](/manage-data/data-store/mapping.md#mapping-limit-settings).
::::

### Agent API reference [_agent_api_reference]

* Go: [`SetLabel`](apm-agent-go://reference/api-documentation.md#context-set-label)
* Java: [`setLabel`](apm-agent-java://reference/public-api.md#api-transaction-add-tag)
* .NET: [`SetLabel`](apm-agent-dotnet://reference/public-api.md#api-transaction-set-label)
* Node.js: [`setLabel`](apm-agent-nodejs://reference/agent-api.md#apm-add-labels)
* PHP: [`Transaction` `setLabel`](apm-agent-php://reference/public-api.md#api-transaction-interface-set-label) | [`Span` `setLabel`](apm-agent-php://reference/public-api.md#api-span-interface-set-label)
* Python: [`elasticapm.label()`](apm-agent-python://reference/api-reference.md#api-label)
* Ruby:  [`set_label`](apm-agent-ruby://reference/api-reference.md#api-agent-set-label)
* Rum: [`addLabels`](apm-agent-rum-js://reference/agent-api.md#apm-add-labels)

## Custom context [apm-data-model-custom]

Custom context adds **non-indexed**, custom contextual information to transactions and errors. Non-indexed means the data is not searchable or aggregatable in {{es}}, and you cannot build dashboards on top of the data. This also means you don’t have to worry about [mapping explosions](/manage-data/data-store/mapping.md#mapping-limit-settings), as these fields are not added to the mapping.

Non-indexed information is useful for providing contextual information to help you quickly debug performance issues or errors.

* Indexed: No
* {{es}} type: [object](elasticsearch://reference/elasticsearch/mapping-reference/object.md)
* {{es}} fields: `transaction.custom` | `error.custom`
* Applies to: [Transactions](/solutions/observability/apm/transactions.md) | [Errors](/solutions/observability/apm/errors.md)

::::{important}
Setting a circular object, a large object, or a non JSON serializable object can lead to errors.
::::

### Agent API reference [_agent_api_reference_2]

* Go: [`SetCustom`](apm-agent-go://reference/api-documentation.md#context-set-custom)
* iOS: *coming soon*
* Java: [`addCustomContext`](apm-agent-java://reference/public-api.md#api-transaction-add-custom-context)
* .NET: *coming soon*
* Node.js: [`setCustomContext`](apm-agent-nodejs://reference/agent-api.md#apm-set-custom-context)
* PHP: *coming soon*
* Python: [`set_custom_context`](apm-agent-python://reference/api-reference.md#api-set-custom-context)
* Ruby: [`set_custom_context`](apm-agent-ruby://reference/api-reference.md#api-agent-set-custom-context)
* Rum: [`setCustomContext`](apm-agent-rum-js://reference/agent-api.md#apm-set-custom-context)

## User context [apm-data-model-user]

User context adds **indexed** user information to transactions and errors. Indexed means the data is searchable and aggregatable in {{es}}.

* Indexed: Yes
* {{es}} type: [keyword](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md)
* {{es}} fields: `user.email` | `user.name` | `user.id`
* Applies to: [Transactions](/solutions/observability/apm/transactions.md) | [Errors](/solutions/observability/apm/errors.md)

### Agent API reference [_agent_api_reference_3]

* Go: [`SetUsername`](apm-agent-go://reference/api-documentation.md#context-set-user-email)
* iOS: *coming soon*
* Java: [`setUser`](apm-agent-java://reference/public-api.md#api-transaction-set-user)
* .NET *coming soon*
* Node.js: [`setUserContext`](apm-agent-nodejs://reference/agent-api.md#apm-set-user-context)
* PHP: *coming soon*
* Python: [`set_user_context`](apm-agent-python://reference/api-reference.md#api-set-user-context)
* Ruby: [`set_user`](apm-agent-ruby://reference/api-reference.md#api-agent-set-user)
* Rum: [`setUserContext`](apm-agent-rum-js://reference/agent-api.md#apm-set-user-context)

