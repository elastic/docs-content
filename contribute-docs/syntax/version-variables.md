# Version Variables

Version are exposed during build using the `{{versions.VERSIONING_SCHEME}}` variable.

For example `stack` versioning variables are exposed as `{{versions.stack}}`.

## Specialized Suffixes.

Besides the current version, the following suffixes are available:

| Version substitution                 | result                            | purpose                                 |
|--------------------------------------|-----------------------------------|-----------------------------------------| 
| `{{version.stack}}`                 | {{version.stack}}                 | Current version                         |
| `{{version.stack.base}}`            | {{version.stack.base}}            | The first version on the new doc system |

## Formatting

Using specialized [mutation operators](substitutions.md#mutations) versions 
can be printed in any kind of ways.


| Version substitution   | result    |
|------------------------|-----------|
| `{{version.stack| M.M}}`    |  {{version.stack|M.M}} |
| `{{version.stack.base | M }}`     | {{version.stack.base | M }} |
| `{{version.stack | M+1       | M }}` | {{version.stack | M+1 | M }} |
| `{{version.stack.base | M.M+1 }}` | {{version.stack.base | M.M+1 }} |

## Mutation Operators in Links and Code Blocks

Mutation operators also work correctly in links and code blocks, making them versatile for various documentation contexts.

### In Links

Mutation operators can be used in both link URLs and link text:

```markdown subs=false
[Download version {{version.stack | M.M}}](https://download.elastic.co/{{version.stack | M.M}}/elasticsearch.tar.gz)
[Latest major version](https://elastic.co/guide/en/elasticsearch/reference/{{version.stack | M}}/index.html)
```

Which renders as:

[Download version {{version.stack | M.M}}](https://download.elastic.co/{{version.stack | M.M}}/elasticsearch.tar.gz)
[Latest major version](https://elastic.co/guide/en/elasticsearch/reference/{{version.stack | M}}/index.html)

### In Code Blocks

Mutation operators work in enhanced code blocks when `subs=true` is specified:

````markdown subs=false
```bash subs=true
curl -X GET "localhost:9200/_cluster/health?v&pretty"
echo "Elasticsearch {{version.stack | M.M}} is running"
```
````

Which renders as:

```bash subs=true
curl -X GET "localhost:9200/_cluster/health?v&pretty"
echo "Elasticsearch {{version.stack | M.M}} is running"
```

### Whitespace Handling

Mutation operators are robust and handle whitespace around the pipe character correctly:

| Syntax | Result | Notes |
|--------|--------| ----- |
| `{{version.stack|M.M}}` | {{version.stack|M.M}} | No spaces |
| `{{version.stack | M.M}}` | {{version.stack | M.M}} | Spaces around pipe |
| `{{version.stack |M.M}}` | {{version.stack |M.M}} | Space before pipe |
| `{{version.stack| M.M}}` | {{version.stack| M.M}} | Space after pipe |

## Available versioning schemes

This is dictated by the [`versions.yml`](https://github.com/elastic/docs-builder/blob/main/config/versions.yml) configuration file

* `stack`
* `ece`
* `ech`
* `eck`
* `ess`
* `esf`
* `search_ui`
* `self`
* `ecctl`
* `curator`
* `security`
* `apm_agent_android`
* `apm_agent_ios`
* `apm_agent_dotnet`
* `apm_agent_go`
* `apm_agent_java`
* `apm_agent_node`
* `apm_agent_php`
* `apm_agent_python`
* `apm_agent_ruby`
* `apm_agent_rum`
* `edot_ios`
* `edot_android`
* `edot_dotnet`
* `edot_java`
* `edot_node`
* `edot_php`
* `edot_python`
* `edot_cf_aws`
* `edot_cf_azure`
* `edot_collector`
* `apm_attacher`
* `apm_lambda`
* `ecs_logging_dotnet`
* `ecs_logging_go_logrus`
* `ecs_logging_go_zap`
* `ecs_logging_go_zerolog`
* `ecs_logging_java`
* `ecs_logging_nodejs`
* `ecs_logging_php`
* `ecs_logging_python`
* `ecs_logging_ruby`

The following are available but should not be used. These map to serverless projects and have a fixed high version number.

* `all`
* `ech`
* `ess` (This is deprectated but was added for backwards-compatibility.)

* `serverless`
* `elasticsearch`
* `observability`
