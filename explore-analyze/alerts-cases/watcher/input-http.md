---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "HTTP input"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/input-http.html
---

# HTTP input [input-http]

Use the `http` input to submit a request to an HTTP endpoint and load the response into the watch execution context when the watch is triggered. See [HTTP input attributes](#http-input-attributes) for all of the supported attributes.

With the `http` input, you can:

* Query external Elasticsearch clusters. The `http` input provides a way to submit search requests to clusters other than the one {{watcher}} is running on. This is useful when you’re running a dedicated {{watcher}} cluster or if you need to search clusters that are running different Elasticsearch versions.
* Query Elasticsearch APIs other than the search API. For example, you might want to load data from the [nodes stats](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats), [cluster health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) or [cluster state](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-state) APIs.
* Query external web services. The `http` input enables you to load data from any service that exposes an HTTP endpoint. This provides a bridge between Elasticsearch clusters and other systems.

## Querying external Elasticsearch clusters [_querying_external_elasticsearch_clusters]

To query an external Elasticsearch cluster, you specify the cluster’s `host` and `port` attributes and the index’s search endpoint as the `path`. If you omit the search body, the request returns all documents in the specified index:

```js
"input" : {
  "http" : {
    "request" : {
      "host" : "example.com",
      "port" : 9200,
      "path" : "/idx/_search"
    }
  }
}
```
%  NOTCONSOLE

You can use the full Elasticsearch [Query DSL](../../query-filter/languages/querydsl.md) to perform more sophisticated searches. For example, the following `http` input retrieves all documents that contain `event` in the `category` field:

```js
"input" : {
  "http" : {
    "request" : {
      "host" : "host.domain",
      "port" : 9200,
      "path" : "/idx/_search",
      "body" :  "{\"query\" :  {  \"match\" : { \"category\" : \"event\"}}}"
    }
  }
}
```
%  NOTCONSOLE

## Calling Elasticsearch APIs [_calling_elasticsearch_apis]

To load the data from other Elasticsearch APIs, specify the API endpoint as the `path` attribute. Use the `params` attribute to specify query string parameters. For example, the following `http` input calls the [cluster stats](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-stats) API and enables the `human` attribute:

```js
"input" : {
  "http" : {
    "request" : {
      "host" : "host.domain",
      "port" : 9200,
      "path" : "/_cluster/stats",
      "params" : {
        "human" : "true" <1>
      }
    }
  }
}
```

1. Enabling this attribute returns the `bytes` values in the response in human readable format.
%  NOTCONSOLE

## Calling external web services [input-http-auth-basic-example]

You can use `http` input to get data from any external web service. The `http` input supports basic authentication. For example, the following input provides a username and password to access `myservice`:

```js
"input" : {
  "http" : {
    "request" : {
      "host" : "host.domain",
      "port" : 9200,
      "path" : "/myservice",
      "auth" : {
        "basic" : {
          "username" : "user",
          "password" : "pass"
        }
      }
    }
  }
}
```
%  NOTCONSOLE

You can also pass in service-specific API keys and other information through the `params` attribute. For example, the following `http` input loads the current weather forecast for Amsterdam from the [OpenWeatherMap](http://openweathermap.org/appid) service:

```js
"input" : {
  "http" : {
    "request" : {
      "url" : "http://api.openweathermap.org/data/2.5/weather",
      "params" : {
        "lat" : "52.374031",
        "lon" : "4.88969",
        "appid" : "<your openweathermap appid>"
      }
    }
  }
}
```
%  NOTCONSOLE

### Using token-based authentication [_using_token_based_authentication]

You can also call an API using a `Bearer token` instead of basic authentication. The `request.headers` object contains the HTTP headers:

```js
"input" : {
  "http" : {
    "request" : {
      "url": "https://api.example.com/v1/something",
      "headers": {
        "authorization" : "Bearer ABCD1234...",
        "content-type": "application/json"
        # other headers params..
        },
      "connection_timeout": "30s"
    }
  }
}
```
%  NOTCONSOLE

## Using templates [_using_templates_2]

The `http` input supports templating. You can use [templates](how-watcher-works.md#templates) when specifying the `path`, `body`, header values, and parameter values.

For example, the following snippet uses templates to specify what index to query and restrict the results to documents added within the last five minutes:

```js
"input" : {
  "http" : {
    "request" : {
      "host" : "host.domain",
      "port" : 9200,
      "path" : "/{{ctx.watch_id}}/_search",
      "body" : "{\"query\" : {\"range\": {\"@timestamp\" : {\"from\": \"{{ctx.trigger.triggered_time}}||-5m\",\"to\": \"{{ctx.trigger.triggered_time}}\"}}}}"
      }
    }
  }
```
%  NOTCONSOLE

## Accessing the HTTP response [_accessing_the_http_response]

If the response body is formatted in JSON or YAML, it is parsed and loaded into the execution context. If the response body is not formatted in JSON or YAML, it is loaded into the payload’s `_value` field.

Conditions, transforms, and actions access the response data through the execution context. For example, if the response contains a `message` object, you can use `ctx.payload.message` to access the message data.

In addition all the headers from the response can be accessed using the `ctx.payload._headers` field as well as the HTTP status code of the response using `ctx.payload._status_code`.

## HTTP input attributes [http-input-attributes]

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `request.scheme` | no | http | Url scheme. Valid values are: `http` or `https`. |
| `request.host` | yes | - | The host to connect to. |
| `request.port` | yes | - | The port the http service is listening on. |
| `request.path` | no | - | The URL path. The path can be static text or contain `mustache`                                                       [templates](how-watcher-works.md#templates). URL query string parameters must be                                                       specified via the `request.params` attribute. |
| `request.method` | no | get | The HTTP method. Supported values are: `head`, `get`, `post`,                                                       `put` and `delete`. |
| `request.headers` | no | - | The HTTP request headers. The header values can be static text                                                       or include `mustache` [templates](how-watcher-works.md#templates). |
| `request.params` | no | - | The URL query string parameters. The parameter values can be                                                       static text or contain `mustache` [templates](how-watcher-works.md#templates). |
| `request.url` | no | - | Allows you to set `request.scheme`, `request.host`, `request.port`                                                       and `request.params` add once by specifying a real URL, like                                                       `https://www.example.org:1234/mypath?foo=bar`. May not be combined                                                       with on of those four parameters. As those parameters are set,                                                       specifying them individually might overwrite them. |
| `request.auth.basic.username` | no | - | HTTP basic authentication username |
| `request.auth.basic.password` | no | - | HTTP basic authentication password |
| `request.proxy.host` | no | - | The proxy host to use when connecting to the host. |
| `request.proxy.port` | no | - | The proxy port to use when connecting to the host. |
| `request.connection_timeout` | no | 10s | The timeout for setting up the http connection. If the connection                                                       could not be set up within this time, the input will timeout and                                                       fail. |
| `request.read_timeout` | no | 10s | The timeout for reading data from http connection. If no response                                                       was received within this time, the input will timeout and fail. |
| `request.body` | no | - | The HTTP request body. The body can be static text or include                                                       `mustache` [templates](how-watcher-works.md#templates). |
| `extract` | no | - | A array of JSON keys to extract from the input response and                                                       use as payload. In cases when an input generates a large                                                       response this can be used to filter the relevant piece of                                                       the response to be used as payload. |
| `response_content_type` | no | json | The expected content type the response body will contain.                                                       Supported values are `json`, `yaml` and `text`. If the                                                       format is `text` the `extract` attribute cannot exist.                                                       Note that this overrides the header that is returned in the                                                       HTTP response. If this is set to `text` the body of the                                                       response will be assigned and accessible to/via the `_value`                                                       variable of the payload. |

You can reference the following variables in the execution context when specifying the `path`, `params`, `headers` and `body` values:

| Name | Description |
| --- | --- |
| `ctx.watch_id` | The id of the watch that is currently executing. |
| `ctx.execution_time` | The time execution of this watch started. |
| `ctx.trigger.triggered_time` | The time this watch was triggered. |
| `ctx.trigger.scheduled_time` | The time this watch was supposed to be triggered. |
| `ctx.metadata.*` | Any metadata associated with the watch. |
