---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-support-matrix.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Synthetics support matrix [synthetics-support-matrix]

There are various components that make up the Synthetics solution, which are supported in the following configurations:

## {{synthetics-app}} [_synthetics_app]

* **GA support**: 8.8.0 and higher
* **Notes**:

    * For creating and managing lightweight and browser monitors configured through the [{{synthetics-app}}](/solutions/observability/synthetics/create-monitors-ui.md)
    * For reporting for lightweight and browser monitors configured through the [{{synthetics-app}}](/solutions/observability/synthetics/create-monitors-ui.md) and/or [{{project-monitors-cap}}](/solutions/observability/synthetics/create-monitors-with-projects.md)

## {{project-monitors-cap}} [_project_monitors_cap]

* **GA support**: 8.8.0 and higher
* **Notes**: For creating and managing lightweight and browser monitors configured as [{{project-monitors-cap}}](/solutions/observability/synthetics/create-monitors-with-projects.md)

## Elastic’s global managed testing infrastructure [_elastics_global_managed_testing_infrastructure_2]

* **GA support**: 8.8.0 and higher
* **Notes**: Elastic’s infrastructure for running lightweight and browser monitors configured through the [{{synthetics-app}}](/solutions/observability/synthetics/create-monitors-ui.md) and/or [{{project-monitors-cap}}](/solutions/observability/synthetics/create-monitors-with-projects.md)

    Executing synthetic tests on Elastic’s global managed testing infrastructure incurs an additional charge. Tests are charged under one of two new billing dimensions depending on the monitor type. For *browser monitor* usage, there is a fee per test run. For *lightweight monitor* usage, there is a fee per region in which you run any monitors regardless of the number of test runs. For more details, refer to [full details and current pricing](https://www.elastic.co/pricing).

## {{private-location}}s [_private_locations_2]

* **GA support**: 8.8.0 and higher
* **Notes**:

    * For running lightweight and browser monitors from your self-managed infrastructure
    * Relies on the Synthetics integration 1.0.0 or above

        * Any *inline* or *Zip URL* monitors configured with the beta Synthetics integration prior to 1.0.0, are not supported and will stop running in the future

    * Shipped as the `elastic-agent-complete` Docker image
    * Must have a direct connection to {{es}}

        * Do not configure any ingest pipelines or Logstash output

## Heartbeat with Uptime [_heartbeat_with_uptime]

```{applies_to}
stack: deprecated 8.15.0
serverless: unavailable
```

* **GA support**: As defined in the standard [Support matrix](https://www.elastic.co/support/matrix)
* **Notes**:

    * For running lightweight monitors via YML configuration running on self-managed infrastructure
    * Browser-based monitors are not supported in this configuration

## Standalone {{agent}} [_standalone_agent]

* **GA support**: As defined in the standard [Support matrix](https://www.elastic.co/support/matrix)
* **Notes**:

    * For running lightweight monitors via YML configuration running on self-managed infrastructure with standalone {{agent}}
    * Browser-based monitors are not supported in this configuration
    * Results for monitors configured using the standalone {{agent}} are available in the {{uptime-app}} (*not* the {{synthetics-app}})

## Synthetics Recorder [_synthetics_recorder]

System requirements:

* macOS - High Sierra and newer
* Windows - Windows 10 and newer
* Linux:

    * Ubuntu - 14.04 and newer
    * Fedora - 24 and newer
    * Debian - 8 and newer

## Output to Elasticsearch [_output_to_elasticsearch]

Synthetics must have a direct connection to {{es}}, whether running monitors from Elastic’s global managed testing infrastructure or from {{private-location}}s.

Do not configure any ingest pipelines or output via Logstash as this will prevent Synthetics from working properly and is not supported.

