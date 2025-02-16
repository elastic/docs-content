# Get started [synthetics-get-started]

To set up a synthetic monitor, you need to configure the monitor, run it, and send data back to {{es}}. After setup is complete, the data will be available in {{kib}} to view, analyze, and alert on.

$$$uptime-set-up-choose$$$
There are two ways to set up a synthetic monitor:

* {{project-monitors-cap}}
* The {{synthetics-app}}

Read more about each option below, and choose the approach that works best for you.


## {{project-monitors-cap}} [choose-projects]

With Elastic {{project-monitors-cap}}, you write tests in an external version-controlled project using YAML for lightweight monitors and JavaScript or TypeScript for browser monitors. Then, you use the `@elastic/synthetics` NPM library’s `push` command to create monitors in {{kib}}.

This approach works well if you want to create both browser monitors and lightweight monitors. It also allows you to configure and update monitors using a GitOps workflow.

Get started in [Use {{project-monitors-cap}}](../../../solutions/observability/apps/create-monitors-with-project-monitors.md).

:::{image} ../../../images/observability-synthetics-get-started-projects.png
:alt: synthetics get started projects
:::


## {{synthetics-app}} [choose-ui]

The {{synthetics-app}} is an application in {{kib}}. You can create monitors directly in the {{synthetics-app}} using the user interface.

This approach works well if you want to configure and update monitors using a UI in your browser.

Get started in [Use the {{synthetics-app}}](../../../solutions/observability/apps/create-monitors-in-synthetics-app.md).

:::{image} ../../../images/observability-synthetics-get-started-ui.png
:alt: Diagram showing which pieces of software are used to configure monitors
:::

::::{note}
The Elastic Synthetics integration is a method for creating synthetic monitors that is no longer recommended. **Do not use the Elastic Synthetics integration to set up new monitors.**

For details on how to migrate from Elastic Synthetics integration to {{project-monitors}} or the {{synthetics-app}}, refer to [Migrate from the Elastic Synthetics integration](../../../solutions/observability/apps/migrate-from-elastic-synthetics-integration.md).

If you’ve used the Elastic Synthetics integration to create monitors in the past and need to reference documentation about the integration, go to the [8.3 documentation](https://www.elastic.co/guide/en/observability/8.3/uptime-set-up.html#uptime-set-up-choose-agent).

::::




