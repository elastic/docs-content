---
navigation_title: Set up
applies_to:
  stack: ga
  serverless: unavailable
---

# Set up APM Server

:::{tip}
Just getting started?
The fastest way to get started with Elastic APM is with Elastic Cloud Serverless.
Read more in [](/solutions/observability/apm/get-started.md).
:::

APM Server receives performance data from your APM agents and Elastic Distribution of OpenTelemetry (EDOT) SDKs, validates and processes it, and then transforms the data into {{es}} documents. If you’re on this page, then you’ve chosen to self-manage the Elastic Stack, and you now must decide how to run and configure the APM Server. There are two options, and the components required are different for each:

* [Fleet-managed APM Server](#apm-setup-fleet-managed-apm)
* [APM Server binary](#apm-setup-apm-server-binary)

## Fleet-managed APM Server [apm-setup-fleet-managed-apm]

Fleet is a web-based UI in {{kib}} that is used to centrally manage {{agent}}s. In this deployment model, use {{agent}} to spin up APM Server instances that can be centrally-managed in a custom-curated user interface.

:::{image} /solutions/images/observability-fm-ov.png
:alt: APM Server fleet overview
:::

**Pros**:

* Conveniently manage one, some, or many different integrations from one central {{fleet}} UI.
* Centrally manage multiple APM Servers running on edge machines.

**Supported outputs**:

* {{es}}
* {{ech}}

::::{note}
Fleet-managed APM Server does *not* support all the outputs that are supported by the APM Server binary method of running Elastic APM.
::::

**Required components**:

* EDOT SDKs or APM agents
* {{agent}} (which runs multiple subprocesses including APM Server, Fleet Server, and {{stack}})

**Configuration method**: {{kib}} UI

## APM Server binary [apm-setup-apm-server-binary]

Install, configure, and run the APM Server binary wherever you need it.

:::{image} /solutions/images/observability-bin-ov.png
:alt: APM Server binary overview
:::

**Pros**:

* Simplest self-managed option
* No addition component knowledge required
* YAML configuration simplifies automation

**Supported outputs**:

* {{es}}
* {{ech}}
* {{ls}}
* Kafka
* Redis
* File
* Console

**Required components**:

* EDOT SDKs or APM agents
* APM Server
* {{stack}}

**Configuration method**: YAML

## Help me decide [_help_me_decide]

This decision tree highlights key factors to help you make an informed decision about implementing Elastic APM. It provides practical guidance and is not intended to serve as a comprehensive reference of all possible implementations and capabilities.

:::{image} /solutions/images/observability-apm-help-me-decide.svg
:alt: APM decision tree
:::