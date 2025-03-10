---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-template.html
applies_to:
  stack:
  serverless:
---

# Search templates [search-template]

A search template is a stored search you can run with different variables.

If you use {{es}} as a search backend, you can pass user input from a search bar as parameters for a search template. This lets you run searches without exposing {{es}}'s query syntax to your users.

If you use {{es}} for a custom application, search templates let you change your searches without modifying your app’s code.


### Create a search template [create-search-template]

To create or update a search template, use the [create stored script API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-put-script).

The request’s `source` supports the same parameters as the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)'s request body.`source` also accepts [Mustache](https://mustache.github.io/) variables, from an open source project [mustache.java](https://github.com/spullara/mustache.java).

Typically [Mustache](https://mustache.github.io/) variables are enclosed in double curly brackets: `{{my-var}}`. When you run a templated search, {{es}} replaces these variables with values from `params`. To learn more about mustache syntax - see [Mustache.js manual](http://mustache.github.io/mustache.5.html) Search templates must use a `lang` of `mustache`.

The following request creates a search template with an `id` of `my-search-template`.

```console
PUT _scripts/my-search-template
{
  "script": {
    "lang": "mustache",
    "source": {
      "query": {
        "match": {
          "message": "{{query_string}}"
        }
      },
      "from": "{{from}}",
      "size": "{{size}}"
    }
  }
}
```

{{es}} stores search templates as Mustache [scripts](../../explore-analyze/scripting.md) in the cluster state. {{es}} compiles search templates in the `template` script context. Settings that limit or disable scripts also affect search templates.


### Validate a search template [validate-search-template]

$$$_validating_templates$$$
To test a template with different `params`, use the [render search template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-render-search-template).

```console
POST _render/template
{
  "id": "my-search-template",
  "params": {
    "query_string": "hello world",
    "from": 20,
    "size": 10
  }
}
```
%  TEST[continued]

When rendered, the template outputs a [search request body](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search).

```console-result
{
  "template_output": {
    "query": {
      "match": {
        "message": "hello world"
      }
    },
    "from": "20",
    "size": "10"
  }
}
```

You can also use the API to test inline templates.

```console
POST _render/template
{
    "source": {
      "query": {
        "match": {
          "message": "{{query_string}}"
        }
      },
      "from": "{{from}}",
      "size": "{{size}}"
    },
  "params": {
    "query_string": "hello world",
    "from": 20,
    "size": 10
  }
}
```
%  TEST[continued]


### Run a templated search [run-templated-search]

To run a search with a search template, use the [search template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-template). You can specify different `params` with each request.

```console
GET my-index/_search/template
{
  "id": "my-search-template",
  "params": {
    "query_string": "hello world",
    "from": 0,
    "size": 10
  }
}
```
%  TEST[continued]

The response uses the same properties as the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)'s response.

```console-result
{
  "took": 36,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.5753642,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 0.5753642,
        "_source": {
          "message": "hello world"
        }
      }
    ]
  }
}
```
%  TESTRESPONSE[s/"took": 36/"took": "$body.took"/]


### Run multiple templated searches [run-multiple-templated-searches]

To run multiple templated searches with a single request, use the [multi search template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch-template). These requests often have less overhead and faster speeds than multiple individual searches.

```console
GET my-index/_msearch/template
{ }
{ "id": "my-search-template", "params": { "query_string": "hello world", "from": 0, "size": 10 }}
{ }
{ "id": "my-other-search-template", "params": { "query_type": "match_all" }}
```
%  TEST[continued]
%  TEST[s/my-other-search-template/my-search-template/]


### Get search templates [get-search-templates]

To retrieve a search template, use the [get stored script API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get-script).

```console
GET _scripts/my-search-template
```
%  TEST[continued]

To get a list of all search templates and other stored scripts, use the [cluster state API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-state).

```console
GET _cluster/state/metadata?pretty&filter_path=metadata.stored_scripts
```
%  TEST[continued]


### Delete a search template [delete-search-template]

To delete a search template, use the [delete stored script API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-script).

```console
DELETE _scripts/my-search-template
```
%  TEST[continued]


### Set default values [search-template-set-default-values]

To set a default value for a variable, use the following syntax:

```handlebars
{{my-var}}{{^my-var}}default value{{/my-var}}
```

If a templated search doesn’t specify a value in its `params`, the search uses the default value instead. For example, the following template sets defaults for `from` and `size`.

```console
POST _render/template
{
  "source": {
    "query": {
      "match": {
        "message": "{{query_string}}"
      }
    },
    "from": "{{from}}{{^from}}0{{/from}}",
    "size": "{{size}}{{^size}}10{{/size}}"
  },
  "params": {
    "query_string": "hello world"
  }
}
```


### URL encode strings [search-template-url-encode-strings]

Use the `{{#url}}` function to URL encode a string.

```console
POST _render/template
{
  "source": {
    "query": {
      "term": {
        "url.full": "{{#url}}{{host}}/{{page}}{{/url}}"
      }
    }
  },
  "params": {
    "host": "http://example.com",
    "page": "hello-world"
  }
}
```

The template renders as:

```console-result
{
  "template_output": {
    "query": {
      "term": {
        "url.full": "http%3A%2F%2Fexample.com%2Fhello-world"
      }
    }
  }
}
```


### Concatenate values [search-template-concatenate-values]

Use the `{{#join}}` function to concatenate array values as a comma-delimited string. For example, the following template concatenates two email addresses.

```console
POST _render/template
{
  "source": {
    "query": {
      "match": {
        "user.group.emails": "{{#join}}emails{{/join}}"
      }
    }
  },
  "params": {
    "emails": [ "user1@example.com", "user_one@example.com" ]
  }
}
```

The template renders as:

```console-result
{
  "template_output": {
    "query": {
      "match": {
        "user.group.emails": "user1@example.com,user_one@example.com"
      }
    }
  }
}
```

You can also specify a custom delimiter.

```console
POST _render/template
{
  "source": {
    "query": {
      "range": {
        "user.effective.date": {
          "gte": "{{date.min}}",
          "lte": "{{date.max}}",
          "format": "{{#join delimiter='||'}}date.formats{{/join delimiter='||'}}"
	      }
      }
    }
  },
  "params": {
    "date": {
      "min": "2098",
      "max": "06/05/2099",
      "formats": ["dd/MM/yyyy", "yyyy"]
    }
  }
}
```

The template renders as:

```console-result
{
  "template_output": {
    "query": {
      "range": {
        "user.effective.date": {
          "gte": "2098",
          "lte": "06/05/2099",
          "format": "dd/MM/yyyy||yyyy"
        }
      }
    }
  }
}
```


### Convert to JSON [search-template-convert-json]

Use the `{{#toJson}}` function to convert a variable value to its JSON representation.

For example, the following template uses `{{#toJson}}` to pass an array. To ensure the request body is valid JSON, the `source` is written in the string format.

```console
POST _render/template
{
  "source": "{ \"query\": { \"terms\": { \"tags\": {{#toJson}}tags{{/toJson}} }}}",
  "params": {
    "tags": [
      "prod",
      "es01"
    ]
  }
}
```

The template renders as:

```console-result
{
  "template_output": {
    "query": {
      "terms": {
        "tags": [
          "prod",
          "es01"
        ]
      }
    }
  }
}
```

You can also use `{{#toJson}}` to pass objects.

```console
POST _render/template
{
  "source": "{ \"query\": {{#toJson}}my_query{{/toJson}} }",
  "params": {
    "my_query": {
      "match_all": { }
    }
  }
}
```

The template renders as:

```console-result
{
  "template_output" : {
    "query" : {
      "match_all" : { }
    }
  }
}
```

You can also pass an array of objects.

```console
POST _render/template
{
  "source": "{ \"query\": { \"bool\": { \"must\": {{#toJson}}clauses{{/toJson}} }}}",
  "params": {
    "clauses": [
      {
        "term": {
          "user.id": "kimchy"
        }
      },
      {
        "term": {
          "url.domain": "example.com"
        }
      }
    ]
  }
}
```

The template renders as:

```console-result
{
  "template_output": {
    "query": {
      "bool": {
        "must": [
          {
            "term": {
              "user.id": "kimchy"
            }
          },
          {
            "term": {
              "url.domain": "example.com"
            }
          }
        ]
      }
    }
  }
}
```


### Use conditions [search-template-use-conditions]

To create if conditions, use the following syntax:

```handlebars
{{#condition}}content{{/condition}}
```

If the condition variable is `true`, {{es}} displays its content. For example, the following template searches data from the past year if `year_scope` is `true`.

```console
POST _render/template
{
  "source": "{ \"query\": { \"bool\": { \"filter\": [ {{#year_scope}} { \"range\": { \"@timestamp\": { \"gte\": \"now-1y/d\", \"lt\": \"now/d\" } } }, {{/year_scope}} { \"term\": { \"user.id\": \"{{user_id}}\" }}]}}}",
  "params": {
    "year_scope": true,
    "user_id": "kimchy"
  }
}
```

The template renders as:

```console-result
{
  "template_output" : {
    "query" : {
      "bool" : {
        "filter" : [
          {
            "range" : {
              "@timestamp" : {
                "gte" : "now-1y/d",
                "lt" : "now/d"
              }
            }
          },
          {
            "term" : {
              "user.id" : "kimchy"
            }
          }
        ]
      }
    }
  }
}
```

If `year_scope` is `false`, the template searches data from any time period.

```console
POST _render/template
{
  "source": "{ \"query\": { \"bool\": { \"filter\": [ {{#year_scope}} { \"range\": { \"@timestamp\": { \"gte\": \"now-1y/d\", \"lt\": \"now/d\" } } }, {{/year_scope}} { \"term\": { \"user.id\": \"{{user_id}}\" }}]}}}",
  "params": {
    "year_scope": false,
    "user_id": "kimchy"
  }
}
```

The template renders as:

```console-result
{
  "template_output" : {
    "query" : {
      "bool" : {
        "filter" : [
          {
            "term" : {
              "user.id" : "kimchy"
            }
          }
        ]
      }
    }
  }
}
```

To create if-else conditions, use the following syntax:

```handlebars
{{#condition}}if content{{/condition}} {{^condition}}else content{{/condition}}
```

For example, the following template searches data from the past year if `year_scope` is `true`. Otherwise, it searches data from the past day.

```console
POST _render/template
{
  "source": "{ \"query\": { \"bool\": { \"filter\": [ { \"range\": { \"@timestamp\": { \"gte\": {{#year_scope}} \"now-1y/d\" {{/year_scope}} {{^year_scope}} \"now-1d/d\" {{/year_scope}} , \"lt\": \"now/d\" }}}, { \"term\": { \"user.id\": \"{{user_id}}\" }}]}}}",
  "params": {
    "year_scope": true,
    "user_id": "kimchy"
  }
}
```

## Search template examples with Mustache [search-template-with-mustache-examples]

The mustache templating language defines various tag types you can use within templates. The following sections describe some of these tag types and provide examples of using them in {{es}} search templates.


### Mustache variables [search-template-mustache-variable]

Mustache tags are typically enclosed in double curly brackets. A mustache variable: `{{my-variable}}` is a type of mustache tag. When you run a templated search, {{es}} replaces these variables with values from `params`.

For example, consider the following search template:

```console
PUT _scripts/my-search-template
{
  "script": {
    "lang": "mustache",
    "source": {
      "query": {
        "match": {
          "message": "{{query_string}}"
        }
      },
      "from": "{{from}}",
      "size": "{{size}}"
    }
  }
}
```

Testing the above search template with `params`:

```console
POST _render/template
{
  "id": "my-search-template",
  "params": {
    "query_string": "hello world",
    "from": 20,
    "size": 10
  }
}
```
%  TEST[continued]

When rendered, the `{{query_string}}` in `message` is replaced with `hello world` passed in `params`.

```console-result
{
  "template_output": {
    "query": {
      "match": {
        "message": "hello world"
      }
    },
    "from": "20",
    "size": "10"
  }
}
```

If your search template doesn’t pass a value to your `query_string` the message would be replaced with a empty string.

For example:

```console
POST _render/template
{
  "id": "my-search-template",
  "params": {
    "from": 20,
    "size": 10
  }
}
```
%  TEST[continued]

When rendered, template outputs as:

```console-result
{
  "template_output": {
    "query": {
      "match": {
        "message": ""
      }
    },
    "from": "20",
    "size": "10"
  }
}
```


### Sections [search-template-sections]

Sections are also a type of Mustache tags. You can use `sections` in your search template with a nested or unnested object. A section begins with `{{#my-section-variable}}` and ends with `{{/my-section-variable}}`.

The following search template shows an example using sections with nested objects:

```console
POST _render/template
{
  "source":
  """
  {
    "query": {
      "match": {
        {{#query_message}}
          {{#query_string}}
        "message": "Hello {{#first_name_section}}{{first_name}}{{/first_name_section}} {{#last_name_section}}{{last_name}}{{/last_name_section}}"
          {{/query_string}}
        {{/query_message}}
      }
    }
  }
  """,
  "params": {
    "query_message": {
       "query_string": {
         "first_name_section": {"first_name": "John"},
         "last_name_section": {"last_name": "kimchy"}
       }
    }
  }
}
```

The template renders as:

```console-result
{
  "template_output": {
    "query": {
      "match": {
        "message": "Hello John kimchy"
      }
    }
  }
}
```


#### Lists [search-template-lists]

You can pass a list of objects and loop over each item in your search template.

For example, following search template combines [sections](#search-template-sections) and matches all the usernames:

```console
PUT _scripts/my-search-template
{
  "script": {
    "lang": "mustache",
    "source": {
      "query":{
        "multi_match":{
          "query": "{{query_string}}",
          "fields": """[{{#text_fields}}{{user_name}},{{/text_fields}}]"""
        }
      }
    }
  }
}
```

Testing the template:

```console
POST _render/template
{
  "id": "my-search-template",
  "params": {
    "query_string": "My string",
    "text_fields": [
      {
        "user_name": "John"
      },
      {
        "user_name": "kimchy"
      }
    ]
  }
}
```
%  TEST[continued]

When rendered, template outputs:

```console-result
{
  "template_output": {
    "query": {
      "multi_match": {
        "query": "My string",
        "fields": "[John,kimchy,]"
      }
    }
  }
}
```

::::{note}
The above will cause a trailing comma issue, which causes invalid JSON. A workaround would be to include an [inverted section](#search-template-inverted-section) and adding a variable to make sure it’s the last item in the array.
::::


For example:

```console
PUT _scripts/my-search-template
{
  "script": {
    "lang": "mustache",
    "source": {
      "query":{
        "multi_match":{
          "query": "{{query_string}}",
          "fields": """[{{#text_fields}}{{user_name}}{{^last}},{{/last}}{{/text_fields}}]"""
        }
      }
    }
  }
}
```

Testing the `my-search-template` again with a variable: `last` to determine it’s the last item in the array:

```console
POST _render/template
{
  "id": "my-search-template",
  "params": {
    "query_string": "My string",
    "text_fields": [
      {
        "user_name": "John",
        "last": false
      },
      {
        "user_name": "kimchy",
        "last": true
      }
    ]
  }
}
```
%  TEST[continued]

When rendered the template outputs:

```console-result
{
  "template_output": {
    "query": {
      "multi_match": {
        "query": "My string",
        "fields": "[John,kimchy]"
      }
    }
  }
}
```


#### Lambdas [search-template-lambdas]

{{es}} has pre-built custom functions to support converting the text into a specific format.

To Learn more about usage of mustache lambdas, check out the examples in [Url encode strings](#search-template-url-encode-strings), [Concatenate values](#search-template-concatenate-values), and [Convert to json](#search-template-convert-json).


### Inverted sections [search-template-inverted-section]

Inverted sections are useful when you want to set a value once.

To use inverted sections use following syntax:

```handlebars
{{^my-variable}} content {{/my-variable}}
```

For example, in the following search template if `name_exists` is `false`, `message` is set with `Hello World`, else it is set to empty string.

```console
POST _render/template
{
  "source": {
    "query": {
      "match": {
        "message": "{{^name_exists}}Hello World{{/name_exists}}"
      }
    }
  },
  "params": {
     "name_exists": false
  }
}
```

They can also be combined with  [conditions](#search-template-use-conditions) and [default values](#search-template-set-default-values).

For example, in the following search template, if `name_exists` is `true`, the value of `{{query_string}}` is replaced.   If `name_exists` is `false`, it is set to the default value `World`.

```console
POST _render/template
{
  "source": {
    "query": {
      "match": {
        "message": "Hello {{#name_exists}}{{query_string}}{{/name_exists}}{{^name_exists}}World{{/name_exists}}"
      }
    }
  },
  "params": {
    "query_string": "Kimchy",
     "name_exists": true
  }
}
```

When rendered, template output:

```console-result
{
  "template_output": {
    "query": {
      "match": {
        "message": "Hello Kimchy"
      }
    }
  }
}
```


### Set delimiter [search-template-set-delimiter]

You can change the default delimiter: double curly brackets `{{my-variable}}` to any custom delimiter in your search template.

For example, the following search template changes the default delimiter to a single round bracket `(query_string)`.

```console
PUT _scripts/my-search-template
{
  "script": {
    "lang": "mustache",
    "source":
    """
    {
      "query": {
        "match": {
           {{=( )=}}
          "message": "(query_string)"
          (={{ }}=)
        }
      }
    }
    """
  }
}
```

Testing the template with new delimiter:

```console
POST _render/template
{
  "id": "my-search-template",
  "params": {
    "query_string": "hello world"
  }
}
```
%  TEST[continued]

When rendered, template outputs:

```console-result
{
  "template_output": {
    "query": {
      "match": {
        "message": "hello world"
      }
    }
  }
}
```


### Unsupported features [search-template-unsupported-features]

The following mustache features are not supported in {{es}} search templates:

* Partials


