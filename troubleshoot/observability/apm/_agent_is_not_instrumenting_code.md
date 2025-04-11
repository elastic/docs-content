---
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/php/current/_agent_is_not_instrumenting_code.html
applies_to:
  stack: all
  serverless:
    observability: all
---

# Agent is not instrumenting code [_agent_is_not_instrumenting_code]

## `open_basedir` PHP configuration option [_open_basedir_php_configuration_option]

If you see a similar entry in the agent log, this indicates an incorrect open_basedir configuration. For more details see [the corresponding Limitations sub-section](apm-agent-php://reference/set-up-apm-php-agent.md#limitation-open_basedir).

```
[Elastic APM PHP Tracer] 2023-08-23 14:38:12.223397+02:00 [PID: 268995] [TID: 268995] [WARNING]  [Lifecycle] [lifecycle.cpp:558] [elasticApmModuleInit] Elastic Agent bootstrap file (/home/paplo/sources/apm-agent-php/agent/php/bootstrap_php_part.php) is located outside of paths allowed by open_basedir ini setting. Read more details here https://www.elastic.co/guide/en/apm/agent/php/current/setup.html
```


