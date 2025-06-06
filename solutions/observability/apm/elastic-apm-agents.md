---
navigation_title: APM agents
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agents.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-elastic-apm-agents.html
applies_to:
  stack:
  serverless:
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Elastic APM agents [observability-apm-agents-elastic-apm-agents]

::::{note}

**For Observability Serverless projects**, the **Admin** role or higher is required to use APM agents. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::

Elastic APM agents automatically measure application performance and track errors. They offer built-in support for popular frameworks and technologies, and provide easy-to-use APIs that allow you to instrument any application.

Elastic APM agents are built and maintained by Elastic. While they are similar, different programming languages have different nuances and requirements. Select your preferred language below to learn more about how each agent works.

:::::::{tab-set}

::::::{tab-item} Java
**Elastic APM Java agent**

The Elastic APM Java agent auto-instruments supported technologies and records interesting events, like spans for database queries and transactions for incoming HTTP requests. To do this, it leverages the capability of the JVM to instrument the bytecode of classes. This means that for the supported technologies, there are no code changes required.

Spans are grouped in transactions—by default, one for each incoming HTTP request. But it’s possible to create custom transactions not associated with an HTTP request. Transactions and Spans are sent to Elastic, where they’re transformed, stored, and ready to be visualized.

**Learn more**

If you're ready to give Elastic APM a try, see [Get started with traces and APM](/solutions/observability/apm/get-started.md).

See the [Java agent reference](apm-agent-java://reference/index.md) for full documentation, including:

* [Supported technologies](apm-agent-java://reference/supported-technologies.md)
* [Set up](apm-agent-java://reference/set-up-apm-java-agent.md)
* [Configuration reference](apm-agent-java://reference/configuration.md)
* [API reference](apm-agent-java://reference/tracing-apis.md)

::::{important}
Not all APM agent configuration options are compatible with Elastic Cloud serverless.

::::
::::::

::::::{tab-item} Node.js
**Elastic APM Node.js agent**

The Elastic APM Node.js agent auto-instruments supported frameworks and records interesting events, like HTTP requests and database queries. To do this, it patches modules as they are loaded to capture when module functions and callbacks are called. Additionally, there are some cases where a module will be patched to allow tracing context to be propagated through the asynchronous continuation. This means that for the supported technologies, there are no code changes required.

The Agent automatically links module function calls to callback calls to measure their duration and metadata (like the DB statement), as well as HTTP-related information (like the URL, parameters, and headers).

These events, called Transactions and Spans, are sent to Elastic, where they're transformed, stored, and ready to be visualized.

**Learn more**

If you’re ready to give Elastic APM a try, see [Get started with traces and APM](/solutions/observability/apm/get-started.md).

See the [Node.js agent reference](apm-agent-nodejs://reference/index.md) for full documentation, including:

* [Supported technologies](apm-agent-nodejs://reference/supported-technologies.md)
* [Set up](apm-agent-nodejs://reference/set-up.md)
* [Configuration reference](apm-agent-nodejs://reference/advanced-setup.md)
* [API reference](apm-agent-nodejs://reference/api.md)

::::{important}
Not all APM agent configuration options are compatible with Elastic Cloud serverless.

::::
::::::

::::::{tab-item} Python
**Elastic APM Python agent**

The Elastic APM Python agent has built-in support for Django and Flask performance metrics and error logging, as well as generic support of other WSGI frameworks for error logging.

It instruments your application to collect APM events in a few different ways:

To collect data about incoming requests and background tasks, the Agent integrates with supported technologies to make use of hooks and signals provided by the framework. These framework integrations require limited code changes in your application.

To collect data from database drivers, HTTP libraries, and so on, Elastic APM agents instrument certain functions and methods in these libraries. Instrumentations are set up automatically and do not require any code changes.

In addition to APM and error data, the Python agent also collects system and application metrics in regular intervals. This collection happens in a background thread that is started by the agent.

**Learn more**

If you’re ready to give Elastic APM a try, see [Get started with traces and APM](/solutions/observability/apm/get-started.md).

See the [Python agent reference](apm-agent-python://reference/index.md) for full documentation, including:

* [Supported technologies](apm-agent-python://reference/supported-technologies.md)
* [Set up](apm-agent-python://reference/set-up-apm-python-agent.md)
* [Configuration reference](apm-agent-python://reference/configuration.md)
* [API reference](apm-agent-python://reference/api-reference.md)

::::{important}
Not all APM agent configuration options are compatible with Elastic Cloud serverless.

::::
::::::

::::::{tab-item} Ruby
**Elastic APM Ruby agent**

The Elastic APM Ruby agent auto-instruments supported technologies and records interesting events, like HTTP requests and database queries. To do this, it uses relevant public APIs when they are provided by the libraries. Otherwise, it carefully wraps the necessary internal methods. This means that for the supported technologies, there are no code changes required.

The APM agent automatically keeps track of queries to your data stores to measure their duration and metadata (like the DB statement), as well as HTTP-related information (like the URL, parameters, and headers).

These events, called Transactions and Spans, are sent to Elastic, where they're transformed, stored, and ready to be visualized.

**Learn more**

If you're ready to give Elastic APM a try, see [Get started with traces and APM](/solutions/observability/apm/get-started.md).

See the [Ruby agent reference](apm-agent-ruby://reference/index.md) for full documentation, including:

* [Supported technologies](apm-agent-ruby://reference/supported-technologies.md)
* [Set up](apm-agent-ruby://reference/set-up-apm-ruby-agent.md)
* [Configuration reference](apm-agent-ruby://reference/configuration.md)
* [API reference](apm-agent-ruby://reference/api-reference.md)

::::{important}
Not all APM agent configuration options are compatible with Elastic Cloud serverless.

::::
::::::

::::::{tab-item} Go
**Elastic APM Go agent**

The Elastic APM Go agent enables you to trace the execution of operations in your [Go](https://golang.org/) applications. It has built-in support for popular frameworks and toolkits, like [Gorilla](http://www.gorillatoolkit.org/) and [Gin](https://gin-gonic.com/), as well as support for instrumenting Go’s built-in [net/http](https://golang.org/pkg/net/http/), [database/sql](https://golang.org/pkg/database/sql/) drivers.

The Agent includes instrumentation modules for supported technologies, each providing middleware or wrappers for recording interesting events, such as incoming HTTP requests, outgoing HTTP requests, and database queries.

To collect data about incoming HTTP requests, install router middleware for one of the supported web frameworks. Incoming requests will be recorded as transactions, along with any related panics or errors.

To collect data for outgoing HTTP requests, instrument an `http.Client` or `http.Transport` using `module/apmhttp`. To collect data about database queries, use `module/apmsql`, which provides instrumentation for well-known database drivers.

In order to connect transactions with related spans and errors, and propagate traces between services (distributed tracing), the agent relies on Go’s built-in [context](https://golang.org/pkg/context/) package: transactions and spans are stored in context objects. For example, for incoming HTTP requests, in-flight trace data will be recorded in the `context` object accessible through [net/http.Context](https://golang.org/pkg/net/http/#Request.Context).

In addition to capturing events like those mentioned here, the agent also collects system and application metrics at regular intervals. This collection happens in a background goroutine that is automatically started when the agent is initialized.

**Learn more**

If you're ready to give Elastic APM a try, see [Get started with traces and APM](/solutions/observability/apm/get-started.md).

See the [Go agent reference](apm-agent-go://reference/index.md) for full documentation, including:

* [Supported technologies](apm-agent-go://reference/supported-technologies.md)
* [Set up](apm-agent-go://reference/set-up-apm-go-agent.md)
* [Configuration reference](apm-agent-go://reference/configuration.md)
* [API reference](apm-agent-go://reference/api-documentation.md)

::::{important}
Not all APM agent configuration options are compatible with Elastic Cloud serverless.

::::
::::::

::::::{tab-item} .NET
**Elastic APM .NET agent**

The Elastic APM .NET agent auto-instruments supported technologies and records interesting events, like HTTP requests and database queries. To do this, it uses built-in capabilities of the instrumented frameworks like [Diagnostic Source](https://docs.microsoft.com/en-us/dotnet/api/system.diagnostics.diagnosticsource?view=netcore-3.0), an HTTP module for IIS, or [IDbCommandInterceptor](https://docs.microsoft.com/en-us/dotnet/api/system.data.entity.infrastructure.interception.idbcommandinterceptor?view=entity-framework-6.2.0) for Entity Framework. This means that for the supported technologies, there are no code changes required beyond enabling auto-instrumentation.

The Agent automatically registers callback methods for built-in Diagnostic Source events. With this, the supported frameworks trigger Agent code for relevant events to measure their duration and collect metadata, like DB statements, as well as HTTP related information, like the URL, parameters, and headers. These events, called Transactions and Spans, are sent to Elastic, where they're transformed, stored, and ready to be visualized.

**Learn more**

If you're ready to give Elastic APM a try, see [Get started with traces and APM](/solutions/observability/apm/get-started.md).

See the [.NET agent reference](apm-agent-dotnet://reference/index.md) for full documentation, including:

* [Supported technologies](apm-agent-dotnet://reference/supported-technologies.md)
* [Set up](apm-agent-dotnet://reference/set-up-apm-net-agent.md)
* [Configuration reference](apm-agent-dotnet://reference/configuration.md)
* [API reference](apm-agent-dotnet://reference/public-api.md)

::::{important}
Not all APM agent configuration options are compatible with Elastic Cloud serverless.

::::
::::::

::::::{tab-item} PHP
**Elastic APM PHP agent**

The Elastic APM PHP agent measures application performance and tracks errors. This extension must be installed in your PHP environment.

**Learn more**

If you're ready to give Elastic APM a try, see [Get started with traces and APM](/solutions/observability/apm/get-started.md).

See the [PHP agent reference](apm-agent-php://reference/index.md)  for full documentation, including:

* [Supported technologies](apm-agent-php://reference/supported-technologies.md)
* [Set up](apm-agent-php://reference/set-up-apm-php-agent.md)
* [Configuration reference](apm-agent-php://reference/configuration.md)
* [API reference](apm-agent-php://reference/public-api.md)

::::{important}
Not all APM agent configuration options are compatible with Elastic Cloud serverless.

::::
::::::

:::::::

## Minimum supported versions [observability-apm-agents-elastic-apm-agents-minimum-supported-versions]

The following versions of Elastic APM agents are supported:

| Agent name | Agent version |
| --- | --- |
| **APM AWS Lambda extension** | ≥`1.x` |
| **Go agent** | ≥`1.x` |
| **Java agent** | ≥`1.x` |
| **.NET agent** | ≥`1.x` |
| **Node.js agent** | ≥`4.x` |
| **PHP agent** | ≥`1.x` |
| **Python agent** | ≥`6.x` |
| **Ruby agent** | ≥`3.x` |

::::{note}
Some recently added features may require newer agent versions than those listed above. In these instances, the required APM agent versions will be documented with the feature.

::::