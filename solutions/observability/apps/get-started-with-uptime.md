---
navigation_title: "Get started"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/uptime-get-started.html
applies_to:
  stack: all
---



# Get started with Uptime [uptime-get-started]


::::{important}
**This approach can only be used to create lightweight monitors.** To create *browser* monitors, use the [{{synthetics-app}}](get-started.md).
::::


{{heartbeat}} is a lightweight daemon that you install on a remote server to periodically check the status of your services and determine if they are available. It gathers performance data, formats it, and sends the data to the {{stack}}.

:::{image} ../../../images/observability-synthetics-get-started-heartbeat.png
:alt: Diagram showing which pieces of software are used to configure monitors
:::

::::{note}
The Elastic Synthetics integration is a method for creating synthetic monitors that is no longer recommended. **Do not use the Elastic Synthetics integration to set up new monitors.**

For details on how to migrate from Elastic Synthetics integration to {{project-monitors}} or the {{synthetics-app}}, refer to [Migrate from the Elastic Synthetics integration](migrate-from-elastic-synthetics-integration.md).

If you’ve used the Elastic Synthetics integration to create monitors in the past and need to reference documentation about the integration, go to the [8.3 documentation](https://www.elastic.co/guide/en/observability/8.3/uptime-set-up.html#uptime-set-up-choose-agent).

::::



## Pull the Docker image [uptime-set-up-docker]

Elastic provides Docker images that you can use to run monitors. Start by pulling the {{heartbeat}} Docker image.

Version 9.0.0-beta1 has not yet been released.


## Configure [uptime-set-up-config]

Next, create a `heartbeat.yml` configuration file.

The example below shows how to configure an `http` monitor, one of [three types of lightweight monitors](asciidocalypse://docs/beats/docs/reference/heartbeat/configuration-heartbeat-options.md#monitor-types).

```yaml
heartbeat.monitors:
- type: http
  id: service-status <1>
  name: Service Status
  service.name: my-apm-service-name
  hosts: ["http://localhost:80/service/status"]
  check.response.status: [200]
  schedule: '@every 5s'
```

1. Each `monitor` gets its own ID in the {{uptime-app}} and its own schedule entry. This allows tests to be run in parallel and analyzed separately.


Read more about configuration options in [Configure {{heartbeat}} monitors](asciidocalypse://docs/beats/docs/reference/heartbeat/configuration-heartbeat-options.md).

::::{warning}
**Do not use {{heartbeat}} to set up a *new* `browser` monitor.** Instead, use the [{{synthetics-app}}](get-started.md).

If you previously used {{heartbeat}} to set up **`browser`** monitor, you can find resources in the [8.4 {{heartbeat}} documentation](https://www.elastic.co/guide/en/beats/heartbeat/8.4/monitor-browser-options.html).

::::



## Connect to the {{stack}} [uptime-set-up-connect]

After configuring the monitor, run it in Docker and connect the monitor to the {{stack}}.

Version 9.0.0-beta1 has not yet been released.


## View in {{kib}} [uptime-set-up-kibana]

{{heartbeat}} is now sending synthetic monitoring data to the {{stack}}. Navigate to the {{uptime-app}} in {{kib}}, where you can see screenshots of each run, set up alerts in case of test failures, and more.

If a test does fail (shown as `down` in the {{uptime-app}}), you’ll be able to view the step script that failed, any errors, and a stack trace. For more information, refer to [Analyze](analyze.md).


## Manage monitors [uptime-manage]

After you’ve created a monitor, you’ll need to manage that monitor over time. This might include updating or permanently deleting an existing monitor.

To update a monitor’s configuration, update the relevant options in the {{heartbeat}} configuration file, and the changes will be reflected in the monitors.

To permanently delete a monitor, delete the monitor entry in the `heartbeat.yml` file.
