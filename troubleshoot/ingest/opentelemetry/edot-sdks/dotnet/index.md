---
navigation_title: EDOT .NET
description: Use the information in this section to troubleshoot common problems affecting the {{edot}} .NET.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_dotnet: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshooting the EDOT .NET SDK

Use the information in this section to troubleshoot common problems. As a first step, make sure your stack is compatible with the [supported technologies](elastic-otel-dotnet://reference/edot-dotnet/supported-technologies.md) for EDOT .NET and the OpenTelemetry SDK.

If you have an Elastic support contract, create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). If you don't, post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/elastic-otel-dotnet/issues).

## Obtain EDOT .NET diagnostic logs

For most problems, such as when you don't see data in your Elastic Observability backend, first check the EDOT .NET logs. These logs show initialization details and OpenTelemetry SDK events. If you don't see any warnings or errors in the EDOT .NET logs, switch the log level to `Trace` to investigate further.

The {{edot}} .NET includes built-in diagnostic logging. You can direct logs to a file, STDOUT, or, in common scenarios, an `ILogger` instance. EDOT .NET also observes the built-in diagnostics events from the contrib OpenTelemetry SDK and includes those in its logging output. You can collect the log output and use it to diagnose issues locally during development or when working with Elastic support channels.

## ASP.NET Core (generic host) logging integration

When you build applications based on the generic host, such as those created by the [ASP.NET Core](https://learn.microsoft.com/aspnet/core/introduction-to-aspnet-core) and [worker service](https://learn.microsoft.com/dotnet/core/extensions/workers) templates, the {{edot}} .NET will try to automatically register with the built-in logging components when you use the `IHostApplicationBuilder.AddElasticOpenTelemetry` extension method to register EDOT .NET.

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.AddElasticOpenTelemetry();
```

In this scenario, EDOT .NET tries to access an available `ILoggerFactory` and create an `ILogger`, logging to the event category `Elastic.OpenTelemetry`. EDOT .NET will register this as the additional logger for its diagnostics unless you have already configured a user-provided `ILogger`. This ensures that EDOT .NET and OpenTelemetry SDK logs are written for your application's configured logging providers. In ASP.NET Core, this includes the console logging provider and results in logs such as the following:

```
info: Elastic.OpenTelemetry[0]
      Elastic Distribution of OpenTelemetry (EDOT) .NET: 1.0.0
info: Elastic.OpenTelemetry[0]
      EDOT log file: <disabled>
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: https://localhost:7295
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5247
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Development
```

In the preceding log output, informational level logging is enabled as the default for this application. You can control the output by configuring the log levels.

### Configuring the log level

You can [configure](https://learn.microsoft.com/en-us/dotnet/core/extensions/logging?tabs=command-line#configure-logging) logs sent to the integrated `Microsoft.Extensions.Logging` library in several ways. A common choice is to use the `appsettings.json` file to configure log-level filters for specific categories.

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Elastic.OpenTelemetry": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

In the preceding code, you have filtered `Elastic.OpenTelemetry` to only emit log entries when they have the `Warning` log level or a higher severity. This overrides the `Default` configuration of `Information`.

## Enable global file logging

Integrated logging is helpful because it requires little to no setup. The logging infrastructure is not present by default in some application types, such as console applications. EDOT .NET also offers a global file logging feature, which is the easiest way for you to get diagnostics and debug information. You must enable file logging when you work with Elastic support, as trace logs will be requested.

Specify at least one of the following environment variables to make sure that EDOT .NET logs into a file.

`OTEL_LOG_LEVEL` _(optional)_:
Set the log level at which the profiler should log. Valid values are

* trace
* debug
* information
* warning
* error
* none

The default value is `information`. More verbose log levels like `trace` and `debug` can affect the runtime performance of profiler auto instrumentation, so use them _only_ for diagnostics purposes.

:::{note}
If you don't explicitly set `ELASTIC_OTEL_LOG_TARGETS` to include `file`, global file logging will only be enabled when you configure it with `trace` or `debug`.
:::

`OTEL_DOTNET_AUTO_LOG_DIRECTORY` _(optional)_:
Set the directory in which to write log files. If you don't set this, the default is:

* `%USERPROFILE%\AppData\Roaming\elastic\elastic-otel-dotnet` on Windows
* `/var/log/elastic/elastic-otel-dotnet` on Linux
* `~/Library/Application Support/elastic/elastic-otel-dotnet` on OSX

> ::::{important}
> Make sure the user account under which the profiler process runs has permission to write to the destination log directory. Specifically, when you run on IIS, ensure that the [AppPool identity](https://learn.microsoft.com/en-us/iis/manage/configuring-security/application-pool-identities) has write permissions in the target directory.
> ::::

`ELASTIC_OTEL_LOG_TARGETS` _(optional)_:
A semi-colon separated list of targets for profiler logs. Valid values are

* file
* stdout
* none

The default value is `file` if you set `OTEL_DOTNET_AUTO_LOG_DIRECTORY` or set `OTEL_LOG_LEVEL` to `trace` or `debug`.

## Advanced troubleshooting

### Diagnosing initialization or bootstrap issues

If EDOT for .NET fails before fully bootstrapping its internal components, it won't generate a log file. In such circumstances, you can provide an additional logger for diagnostic purposes. Alternatively, you can enable the `STDOUT` log target.

#### Providing an additional application logger

You can provide an additional `ILogger` that EDOT .NET will use to log pre-bootstrap events by creating an instance of `ElasticOpenTelemetryOptions`.

```csharp
using Elastic.OpenTelemetry;
using Microsoft.Extensions.Logging;
using OpenTelemetry;

using ILoggerFactory loggerFactory = LoggerFactory.Create(static builder =>
{
   builder
      .AddFilter("Elastic.OpenTelemetry", LogLevel.Trace)
      .AddConsole();
});

ILogger logger = loggerFactory.CreateLogger("EDOT");

var options = new ElasticOpenTelemetryOptions
{
   AdditionalLogger = logger
};

using var sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults(options));
```

This example adds the console logging provider, but you can include any provider here. To use this sample code, add a dependency on the `Microsoft.Extensions.Logging.Console` [NuGet package](https://www.nuget.org/packages/microsoft.extensions.logging.console).

You create and configure an `ILoggerFactory`. In this example, you configure the `Elastic.OpenTelemetry` category to capture trace logs, which is the most verbose option. This is the best choice when you diagnose initialization issues.

You use the `ILoggerFactory` to create an `ILogger`, which you then assign to the `ElasticOpenTelemetryOptions.AdditionalLogger` property. Once you pass the `ElasticOpenTelemetryOptions` into the `WithElasticDefaults` method, the provided logger can capture bootstrap logs.

To simplify the preceding code, you can also configure the `ElasticOpenTelemetryOptions` with an `ILoggerFactory` instance that EDOT .NET can use to create its own logger.

```csharp
using var loggerFactory = LoggerFactory.Create(static builder =>
{
   builder
      .AddFilter("Elastic.OpenTelemetry", LogLevel.Debug)
      .AddConsole();
});

var options = new ElasticOpenTelemetryOptions
{
   AdditionalLoggerFactory = loggerFactory
};

using var sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults(options));
```

## Known issues

The following known issues affect EDOT .NET.

### Missing log records

The contrib SDK currently does not [comply with the spec](https://github.com/open-telemetry/opentelemetry-dotnet/issues/4324) regarding the deduplication of attributes when exporting log records. When you create a log within multiple scopes, each scope may store information using the same logical key. In this situation, the exported data will have duplicated attributes.

You are most likely to see this when you log in the scope of a request and enable the `OpenTelemetryLoggerOptions.IncludeScopes` option. ASP.NET Core adds the `RequestId` to multiple scopes. We recommend that you don't enable `IncludeScopes` until the SDK fixes this. When you use the EDOT Collector or the [{{motlp}}](opentelemetry://reference/motlp.md) in serverless, non-compliant log records will fail to be ingested.

EDOT .NET currently emits a warning if it detects that you use `IncludeScopes` in ASP.NET Core scenarios.

This can also happen even when you set `IncludeScopes` to false. The following code will also result in duplicate attributes and the potential for lost log records.

```csharp
Logger.LogInformation("Eat your {fruit} {fruit} {fruit}!", "apple", "banana", "mango");
```

To avoid this scenario, make sure each placeholder uses a unique name. For example:

```csharp
Logger.LogInformation("Eat your {fruit1} {fruit2} {fruit3}!", "apple", "banana", "mango");
```

### Custom processors are not applied to exported data

__TL;DR;__ When using custom processors, they may not run before data is exported.

By default, EDOT .NET simplifies the getting started experience by applying [opinionated defaults](elastic-otel-dotnet://reference/edot-dotnet/setup/edot-defaults.md).

These defaults include registering the OTLP exporter with the OpenTelemetry SDK so that telemetry signal data
is exported without requiring additional code.

In advanced scenarios, you may develop custom processors to enrich signal data with custom logic before it
passes to the next processor in the pipeline. In such circumstances, you will add the processor to the relevant
signal provider builder. 

For example, one may try to use the following code to register a custom processor for trace data using
the `TracerProviderBuilder`.

```c#
builder.AddElasticOpenTelemetry(b => b
  .WithTracing(t => t.AddProcessor<SpanRollupProcessor>())
  .WithMetrics(m => m.AddMeter("MyAppMeter")));
```

This code will not work as desired due to EDOT .NET registering the OTLP exporter before the processor,
therefore running earlier in the pipeline than `SpanRollupProcessor`. The exact behaviour may vary or appear to
work because trace data is exported in batches and the custom processor may partially apply to trace data before
the batch is exported.

EDOT .NET provides a configuration option that should be used in this scenario to disable the automatic registration
of the OTLP exporter. Once disabled, you should manually add the exporter ***after*** registering your custom
processor(s).

Taking the prior example, the correct code should be as follows:

```c#
builder.AddElasticOpenTelemetry(new ElasticOpenTelemetryOptions() { SkipOtlpExporter = true }, b => b
  .WithLogging(l => l.AddOtlpExporter())
  .WithTracing(t =>
  {
    t.AddProcessor<SpanRollupProcessor>();
    t.AddOtlpExporter();
  })
  .WithMetrics(m => m
    .AddMeter("MyAppMeter")
    .AddOtlpExporter()));
```

The preceding code uses an overload of `AddElasticOpenTelemetry` which accepts an `ElasticOpenTelemetryOptions`
instance. The code configures `SkipOtlpExporter` as `true`. If preferred, this may also be configured using the
`appSettings.json` file.

With `SkipOtlpExporter` enabled, the exporter must be added to __each__ signal that should be exported. In
this example, the OTLP exporter is manually added for logs, traces and metrics. Crucially, for traces, the
exporter is registered after the custom `SpanRollupProcessor` to ensure that trace data is batched for export
after the processor has completed.