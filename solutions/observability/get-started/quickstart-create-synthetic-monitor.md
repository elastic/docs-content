---
description: Learn how to create a Synthetic Monitor to proactively test and monitor your applications by simulating user interactions.
applies_to:
  serverless:
products:
  - id: observability
  - id: cloud-serverless
---

# Quickstart: Create a Synthetic Monitor [create-synthetic-monitor]

Elastic [Synthetic monitoring](/solutions/observability/synthetics/index.md) is a comprehensive solution that allows organizations to proactively test and monitor applications by simulating user interactions, providing insights into performance metrics before real users encounter potential issues. This monitoring approach works by executing automated scripts that mimic typical user journeys and evaluating response times, error rates, and other critical performance indicators.

In this quickstart guide, you'll get more familiar with Elastic Observability as well as an overview on how to ingest, view, and get started with Synthetic monitoring.

:::::{stepper}

::::{step} Access your Elastic Cloud account

Go to [cloud.elastic.co](https://cloud.elastic.co/) and access your account or create a new one.

::::

::::{step} Create a new project

Create a new {{observability}} project. Make sure to select your preferred cloud region when you create your first project. Refer to [Create an Observability project](/solutions/observability/get-started.md) for more details. 

::::

::::{step} Go to Synthetics

Once your deployment is complete click **Applications** and select **Monitors** under **Synthetics**.

There are two ways to run synthetic monitors which will depend on if the website or app being tested are accessible from:

* Elastic's global managed testing infrastructure: With Elastic's global managed testing infrastructure, you can create and run monitors in multiple locations without having to manage your own infrastructure. Elastic takes care of software updates and capacity planning for you. This is perfect for testing websites or applications that are accessible from the public internet.  
* Private Locations: Private Locations allow you to run monitors from your own premises. To use Private Locations you must create a Private Location before continuing. For step-by-step instructions, refer to Monitor resources on private networks.

This guide shows how to leverage Elastic's global managed testing infrastructure.

:::{note}  
Projects let you define your infrastructure as code. With project monitors you organize your YAML configuration and JavaScript- or TypeScript-defined monitors on the filesystem, use Git for version control, and deploy via a CLI tool, usually executed on a CI/CD platform. Refer to [Create monitors with project monitors](https://www.elastic.co/guide/en/observability/current/synthetics-get-started-project.html) for more details.
:::

::::{step} Create a browser monitor

Create a single page browser monitor. Make sure to select a URL and the locations where monitors will be executed, then select **Create monitor**.

:::{image} /solutions/images/synthetics-create-browser-monitor.png
:alt: Create browser monitor
:::

Synthetics will be executing the test across all of those locations, automatically refreshing the screen.

:::{image} /solutions/images/Synthetic-Monitors.png
:alt: Browser monitor
:::

::::

::::{step} Turn on alerts

If there are any issues, you might want to turn on alerts. Select **Configure now** from the Alerts warning, or go to **Settings** and then **Alerting**. Select the default connector, which is already prepopulated when you deploy Elastic. After you select your default connector you can add your default email address to receive the alerts.

Go back to **Monitors** and select **Alerts and rules** then **Monitor status rule**. A dialog will appear where you can edit your alerts. You can also select alternate connector types, such as Slack, Microsoft Teams, and more. When you set up alerts and receive notifications, you’ll also receive a deep link directly into the Error details page. From here you can see:

* What step failed  
* Screenshot of the failed step  
* Screenshot of the last time that step was successful  
* The times of the failed step and last time step was successful to compare  
* Select Code executed, to see the code that was executed  
* Select Console to see what the browser is showing

:::{image} /solutions/images/Synthetic-Error_details.png
:alt: Error details
:::

::::

::::{step} Analyze your monitor data

Go to **Monitors** and select one of the monitors, you’ll see a dialog with a quick summary of the monitor. Select **Go to monitor** to see high level insights. Charts will start to render as more tests come through but you can quickly see the availability, the duration to execute tests, the timeline, and you can also drill into the waterfall chart. 

:::{image} /solutions/images/Monitor_drill_down_1.png
:alt: Monitor drill down
:::

To drill in, select the icon under **View test run**. From here you can see the waterfall chart, object weight, object count, and more.

:::{image} /solutions/images/Monitor_drill_down_2.png
:alt: Monitor drill down
:::

::::
:::::

## More resources

* [Explore observability demo gallery](http://docs.google.com/demo-gallery/?solutions=observability&features=null)  
* [Get started with monitoring your application performance (APM/tracking)](http://docs.google.com/getting-started/observability/monitor-your-application-performance)  
* [Get started with monitoring your hosts](http://docs.google.com/getting-started/observability/monitor-your-hosts)  
* [Get started with monitoring Kubernetes clusters](http://docs.google.com/getting-started/observability/monitor-kubernetes-clusters)  
* [Get started with optimizing workloads with universal profiling](http://docs.google.com/observability/universal-profiling)  
* [Create monitors for project monitors](https://www.elastic.co/guide/en/observability/current/synthetics-get-started-project.html)