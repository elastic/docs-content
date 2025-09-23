---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-manage-monitors.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-manage-monitors.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Manage monitors [synthetics-manage-monitors]

After you’ve [created a synthetic monitor](/solutions/observability/synthetics/get-started.md), you’ll need to manage that monitor over time. This might include updating or permanently deleting an existing monitor.

If you’re using {{project-monitors}}, you should also set up a workflow that uses [best practices for managing monitors effectively](/solutions/observability/synthetics/manage-monitors.md#synthetics-projects-best-practices) in a production environment.

## Update a monitor [manage-monitors-config]

You can update a monitor’s configuration, for example, changing the interval at which the monitor runs a test.

You can also update the journey used in a browser monitor. For example, if you update the UI used in your application, you may want to update your journey’s selectors and assertions.

:::::::{tab-set}

::::::{tab-item} Project monitors
If you [set up the monitor using a Synthetic project](/solutions/observability/synthetics/create-monitors-with-projects.md), you’ll update the monitor in the Synthetic project source and then `push` changes.

For lightweight monitors, make changes to the YAML file.

For browser monitors, you can update the configuration of one or more monitors:

* To update the configuration of an individual monitor, edit the journey directly in the JavaScript or TypeScript files, specifically the options in `monitor.use`.
* To update the configuration of *all* monitors in a Synthetic project, edit the [global synthetics configuration file](/solutions/observability/synthetics/configure-projects.md#synthetics-configuration-monitor).

To update the journey that a browser monitor runs, edit the journey code directly and [test the updated journey locally](/solutions/observability/synthetics/write-synthetic-test.md#synthetics-test-locally) to make sure it’s valid.

After making changes to the monitors, run the [`push` command](/solutions/observability/synthetics/cli.md#elastic-synthetics-push-command) to replace the existing monitors with new monitors using the updated configuration or journey code.

::::{note}
Updates are linked to a monitor’s `id`. To update a monitor you must keep its `id` the same.
::::
::::::

::::::{tab-item} Synthetics UI
If you [set up the monitor using the Synthetics UI](/solutions/observability/synthetics/create-monitors-ui.md), you can update the monitor configuration of both lightweight and browser monitors in the {{synthetics-app}}:

1. Go to **Management**.
2. Click the pencil icon next to the monitor you want to edit.
3. Update the *Monitor settings* as needed.

    1. To update the journey used in a browser monitor, edit *Inline script*.
    2. Make sure to click **Run test** to validate the new journey before updating the monitor.

4. Click **Update monitor**.
::::::

:::::::

## Delete a monitor [manage-monitors-delete]

Eventually you might want to delete a monitor altogether. For example, if the user journey you were validating no longer exists.

:::::::{tab-set}

::::::{tab-item} Project monitors
If you [set up the monitor using a Synthetics project](/solutions/observability/synthetics/create-monitors-with-projects.md), you’ll delete the monitor from the project source and push changes.

For lightweight monitors, delete the monitor from the YAML file.

For browser monitors, delete the full journey from the JavaScript or TypeScript file.

Then, run the [`push` command](/solutions/observability/synthetics/cli.md#elastic-synthetics-push-command). The monitor associated with that journey that existed will be deleted.
::::::

::::::{tab-item} Synthetics UI
If you [set up the monitor using the Synthetics UI](/solutions/observability/synthetics/create-monitors-ui.md), you can delete a lightweight or browser monitor in the Synthetics UI:

1. Go to **Management**.
2. Click the trash can icon next to the monitor you want to delete.
::::::

:::::::
Alternatively, you can temporarily disable a monitor by updating the monitor’s configuration in your journey’s code or in the Synthetics UI using the *Enabled* toggle.

## Implement best practices for Synthetics projects [synthetics-projects-best-practices]

::::{important}
This is only relevant to monitors created using projects.
::::

After you’ve [set up a project](/solutions/observability/synthetics/create-monitors-with-projects.md), there are some best practices you can implement to manage the Synthetics project effectively.

### Use version control [synthetics-version-control]

First, it’s recommended that you version control all files in Git. If your Synthetics project is not already in a version controlled directory add it and push it to your Git host.

### Set up recommended workflow [synthetics-workflow]

While it can be convenient to run the `push` command directly from your workstation, especially when setting up a new Synthetics project, it is not recommended for production environments.

Instead, we recommended that you:

1. Develop and test changes locally.
2. Create a pull request for all config changes.
3. Have your CI service automatically verify the PR by running `npx @elastic/synthetics .`

    Elastic’s synthetics runner can output results in a few different formats, including JSON and JUnit (the standard format supported by most CI platforms).

    If any of your journeys fail, it will yield a non-zero exit code, which most CI systems pick up as a failure by default.

4. Have a human approve the pull request.
5. Merge the pull request.
6. Have your CI service automatically deploy the change by running `npx @elastic/synthetics push` after changes are merged.

The exact implementation details will depend on the CI system and Git host you use. You can reference the sample GitHub configuration file that is included in the `.github` directory when you create a new Synthetics project.