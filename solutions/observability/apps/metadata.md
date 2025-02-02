---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-data-model-metadata.html
---

# Metadata [apm-data-model-metadata]

Metadata can enrich your events and make application performance monitoring even more useful. Let’s explore the different types of metadata that Elastic APM offers.


## Labels [apm-data-model-labels] 

Labels add **indexed** information to transactions, spans, and errors. Indexed means the data is searchable and aggregatable in {{es}}. Add additional key-value pairs to define multiple labels.

* Indexed: Yes
* {{es}} type: [object](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html)
* {{es}} field: `labels`
* Applies to: [Transactions](transactions.md) | [Spans](spans.md) | [Errors](errors.md)

Label values can be a string, boolean, or number, although some agents only support string values at this time. Because labels for a given key, regardless of agent used, are stored in the same place in {{es}}, all label values of a given key must have the same data type. Multiple data types per key will throw an exception, for example: `{foo: bar}` and `{foo: 42}` is not allowed.

::::{important} 
Avoid defining too many user-specified labels. Defining too many unique fields in an index is a condition that can lead to a [mapping explosion](../../../manage-data/data-store/mapping.md#mapping-limit-settings).
::::



### Agent API reference [_agent_api_reference] 

* Go: [`SetLabel`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/api.html#context-set-label)
* Java: [`setLabel`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/public-api.html#api-transaction-add-tag)
* .NET: [`SetLabel`](https://www.elastic.co/guide/en/apm/agent/dotnet/{{apm-dotnet-branch}}/public-api.html#api-transaction-set-label)
* Node.js: [`setLabel`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/agent-api.html#apm-set-label) | [`addLabels`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/agent-api.html#apm-add-labels)
* PHP: [`Transaction` `setLabel`](https://www.elastic.co/guide/en/apm/agent/php/current/public-api.html#api-transaction-interface-set-label) | [`Span` `setLabel`](https://www.elastic.co/guide/en/apm/agent/php/current/public-api.html#api-span-interface-set-label)
* Python: [`elasticapm.label()`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/api.html#api-label)
* Ruby:  [`set_label`](https://www.elastic.co/guide/en/apm/agent/ruby/{{apm-ruby-branch}}/api.html#api-agent-set-label)
* Rum: [`addLabels`](https://www.elastic.co/guide/en/apm/agent/rum-js/{{apm-rum-branch}}/agent-api.html#apm-add-labels)


## Custom context [apm-data-model-custom] 

Custom context adds **non-indexed**, custom contextual information to transactions and errors. Non-indexed means the data is not searchable or aggregatable in {{es}}, and you cannot build dashboards on top of the data. This also means you don’t have to worry about [mapping explosions](../../../manage-data/data-store/mapping.md#mapping-limit-settings), as these fields are not added to the mapping.

Non-indexed information is useful for providing contextual information to help you quickly debug performance issues or errors.

* Indexed: No
* {{es}} type: [object](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html)
* {{es}} fields: `transaction.custom` | `error.custom`
* Applies to: [Transactions](transactions.md) | [Errors](errors.md)

::::{important} 
Setting a circular object, a large object, or a non JSON serializable object can lead to errors.
::::



### Agent API reference [_agent_api_reference_2] 

* Go: [`SetCustom`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/api.html#context-set-custom)
* iOS: *coming soon*
* Java: [`addCustomContext`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/public-api.html#api-transaction-add-custom-context)
* .NET: *coming soon*
* Node.js: [`setCustomContext`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/agent-api.html#apm-set-custom-context)
* PHP: *coming soon*
* Python: [`set_custom_context`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/api.html#api-set-custom-context)
* Ruby: [`set_custom_context`](https://www.elastic.co/guide/en/apm/agent/ruby/{{apm-ruby-branch}}/api.html#api-agent-set-custom-context)
* Rum: [`setCustomContext`](https://www.elastic.co/guide/en/apm/agent/rum-js/{{apm-rum-branch}}/agent-api.html#apm-set-custom-context)


## User context [apm-data-model-user] 

User context adds **indexed** user information to transactions and errors. Indexed means the data is searchable and aggregatable in {{es}}.

* Indexed: Yes
* {{es}} type: [keyword](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html)
* {{es}} fields: `user.email` | `user.name` | `user.id`
* Applies to: [Transactions](transactions.md) | [Errors](errors.md)


### Agent API reference [_agent_api_reference_3] 

* Go: [`SetUsername`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/api.html#context-set-username) | [`SetUserID`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/api.html#context-set-user-id) | [`SetUserEmail`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/api.html#context-set-user-email)
* iOS: *coming soon*
* Java: [`setUser`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/public-api.html#api-transaction-set-user)
* .NET *coming soon*
* Node.js: [`setUserContext`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/agent-api.html#apm-set-user-context)
* PHP: *coming soon*
* Python: [`set_user_context`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/api.html#api-set-user-context)
* Ruby: [`set_user`](https://www.elastic.co/guide/en/apm/agent/ruby/{{apm-ruby-branch}}/api.html#api-agent-set-user)
* Rum: [`setUserContext`](https://www.elastic.co/guide/en/apm/agent/rum-js/{{apm-rum-branch}}/agent-api.html#apm-set-user-context)

