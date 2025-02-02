# Get started [observability-synthetics-get-started]

To set up a synthetic monitor, you need to configure the monitor, run it, and send data back to Elastic. After setup is complete, the data will be available in your Observability project to view, analyze, and alert on.

There are two ways to set up a synthetic monitor:

* Synthetics project
* The Synthetics UI

Read more about each option below, and choose the approach that works best for you.


## Synthetics project [observability-synthetics-get-started-synthetics-project]

With a Synthetics project, you write tests in an external version-controlled Node.js project using YAML for lightweight monitors and JavaScript or TypeScript for browser monitors. Then, you use the `@elastic/synthetics` NPM library’s `push` command to create monitors in your Observability project.

This approach works well if you want to create both browser monitors and lightweight monitors. It also allows you to configure and update monitors using a GitOps workflow.

Get started in [Create monitors in a Synthetics project](../../../solutions/observability/apps/create-monitors-with-project-monitors.md).

:::{image} ../../../images/serverless-synthetics-get-started-projects.png
:alt: Diagram showing which pieces of software are used to configure monitors
:::


## Synthetics UI [observability-synthetics-get-started-synthetics-ui]

You can create monitors directly in the user interface. This approach works well if you want to create and manage your monitors in the browser.

Get started in [Create monitors in the Synthetics UI](../../../solutions/observability/apps/create-monitors-in-synthetics-app.md).

:::{image} ../../../images/serverless-synthetics-get-started-ui.png
:alt: Diagram showing which pieces of software are used to configure monitors
:::



