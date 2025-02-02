---
navigation_title: "Use the Synthetics UI"
---

# Create monitors in the Synthetics UI [observability-synthetics-get-started-ui]


You can create synthetic monitors directly in the UI by opening an Observability project and navigating to **Synthetics**.

:::{image} ../../../images/serverless-synthetics-get-started-ui.png
:alt: Diagram showing which pieces of software are used to configure monitors
:::

This is one of [two approaches](../../../solutions/observability/apps/get-started.md) you can use to set up a synthetic monitor.


## Prerequisites [observability-synthetics-get-started-ui-prerequisites]

You must be signed in as a user with [Editor](../../../solutions/observability/apps/grant-users-access-to-secured-resources.md) access.

You should decide where you want to run the monitors before getting started. You can run monitors on one or both of the following:

* **Elastic’s global managed testing infrastructure**: With Elastic’s global managed testing infrastructure, you can create and run monitors in multiple locations without having to manage your own infrastructure. Elastic takes care of software updates and capacity planning for you.
* **{{private-location}}s**: {{private-location}}s allow you to run monitors from your own premises. To use {{private-location}}s you must create a {{private-location}} before continuing. For step-by-step instructions, refer to [Monitor resources on private networks](../../../solutions/observability/apps/monitor-resources-on-private-networks.md).

Executing synthetic tests on Elastic’s global managed testing infrastructure incurs an additional charge. Tests are charged under one of two new billing dimensions depending on the monitor type. For *browser monitor* usage, there is a fee per test run. For *lightweight monitor* usage, there is a fee per region in which you run any monitors regardless of the number of test runs. For more details, refer to the [{{obs-serverless}} pricing page](https://www.elastic.co/pricing/serverless-observability).


## Add a lightweight monitor [observability-synthetics-get-started-ui-add-a-lightweight-monitor]

To use the UI to add a lightweight monitor:

1. Go to **Synthetics** in your Observability project.
2. Click **Create monitor**.
3. Set the monitor type to **HTTP Ping**, **TCP Ping**, or **ICMP Ping**.
4. In *Locations*, select one or more locations.

    ::::{note}
    If you don’t see any locations listed, refer to the [troubleshooting guide](../../../troubleshoot/observability/troubleshooting-synthetics.md#synthetics-troubleshooting-no-locations) for guidance.

    ::::


    :::::{note}
    If you’ve [added a {{private-location}}](../../../solutions/observability/apps/monitor-resources-on-private-networks.md), you’ll see your the {{private-location}} in the list of *Locations*.

    :::{image} ../../../images/serverless-private-locations-monitor-locations.png
    :alt: Screenshot of Monitor locations options including a {private-location}
    :class: screenshot
    :::

    :::::

5. Set the *Frequency*, and configure the monitor as needed.
6. Click **Advanced options** to see more ways to configure your monitor.
7. (Optional) Click **Run test** to verify that the test is valid.
8. Click **Create monitor**.

    :::{image} ../../../images/serverless-synthetics-get-started-ui-lightweight.png
    :alt: Synthetics Create monitor UI
    :class: screenshot
    :::



## Add a browser monitor [observability-synthetics-get-started-ui-add-a-browser-monitor]

You can also create a browser monitor in the UI using an **Inline script**.

An inline script contains a single journey that you manage individually. Inline scripts can be quick to set up, but can also be more difficult to manage. Each browser monitor configured using an inline script can contain only *one* journey, which must be maintained directly in the UI.

If you depend on external packages, have your journeys next to your code repository, or want to embed and manage more than one journey from a single monitor configuration, use a [Synthetics project](../../../solutions/observability/apps/create-monitors-with-project-monitors.md) instead.

To use the UI to add a browser monitor:

1. Click **Create monitor**.
2. Set the monitor type to **Multistep**.
3. In *Locations*, select one or more locations.

    ::::{note}
    If you don’t see any locations listed, refer to the [troubleshooting guide](../../../troubleshoot/observability/troubleshooting-synthetics.md#synthetics-troubleshooting-no-locations) for guidance.

    ::::

4. Set the *Frequency*.
5. Add steps to the **Script editor** code block directly. The `journey` keyword isn’t required, and variables like `page` and `params` will be part of your script’s scope. You cannot `import` any dependencies when using inline browser monitors.

    :::{image} ../../../images/serverless-synthetics-ui-inline-script.png
    :alt: Configure a synthetic monitor using an inline script
    :class: screenshot
    :::

    ::::{note}
    Alternatively, you can use the **Script recorder** option. You can use the Elastic Synthetics Recorder to interact with a web page, export journey code that reflects all the actions you took, and upload the results in the UI. For more information, refer to [Use the Synthetics Recorder](../../../solutions/observability/apps/use-synthetics-recorder.md).

    ::::

6. Click **Advanced options** to see more ways to configure your monitor.

    * Use **Data options** to add context to the data coming from your monitors.
    * Use the **Synthetics agent options** to provide fine-tuned configuration for the synthetics agent. Read more about available options in [Use the Synthetics CLI](../../../solutions/observability/apps/use-synthetics-cli.md).

7. (Optional) Click **Run test** to verify that the test is valid.
8. Click **Create monitor**.


## View in your Observability project [observability-synthetics-get-started-ui-view-in-your-observability-project]

Navigate to **Synthetics** in your Observability project, where you can see screenshots of each run, set up alerts in case of test failures, and more.

If a test does fail (shown as `down` in the Synthetics UI), you’ll be able to view the step script that failed, any errors, and a stack trace. For more information, refer to [Analyze data from synthetic monitors](../../../solutions/observability/apps/analyze-data-from-synthetic-monitors.md#synthetics-analyze-journeys).

::::{note}
When a monitor is created or updated, the first run might not occur immediately, but the time it takes for the first run to occur will be less than the monitor’s configured frequency. For example, if you create a monitor and configure it to run every 10 minutes, the first run will occur within 10 minutes of being created. After the first run, the monitor will begin running regularly based on the configured frequency. You can run a manual test if you want to see the results more quickly.

::::



## Next steps [observability-synthetics-get-started-ui-next-steps]

Learn more about:

* [Writing user journeys](../../../solutions/observability/apps/write-synthetic-test.md) to use as inline scripts
* Using the [Synthetics Recorder](../../../solutions/observability/apps/use-synthetics-recorder.md)
* [Configuring lightweight monitors](../../../solutions/observability/apps/configure-lightweight-monitors.md)
