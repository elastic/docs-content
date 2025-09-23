---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-migrate-from-integration.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Migrate from the Elastic Synthetics integration [synthetics-migrate-from-integration]

The Elastic Synthetics integration is a method for creating synthetic monitors that is no longer recommended.

You should *not* use the Elastic Synthetics integration to set up new monitors and should make a plan to migrate existing monitors to use either **{{project-monitors-cap}}** or the **{{synthetics-app}}**:

* With Elastic **{{project-monitors-cap}}**, you write tests in an external version-controlled project and use a CLI tool to push monitors to the {{stack}}.
* The **{{synthetics-app}}** is an application in {{kib}} that you can use to configure and create monitors using a user interface.

## Compare approaches [synthetics-migrate-integration-compare]

Below is a comparison of how you used the {{agent}} integration to create monitors and how you’ll use the {{synthetics-app}} or projects to create monitors:

**Supported monitors**:

* **{{agent}} integration**: Supported both lightweight and browser monitors
* **Projects or the {{synthetics-app}}**: Supports both lightweight and browser monitors

**Where monitors run ([read more](#synthetics-migrate-integration-location))**:

* **{{agent}} integration**: You had to run monitors on your infrastructure
* **Projects or the {{synthetics-app}}**: You can run monitors on both:

    * Your infrastructure using [{{private-location}}s](/solutions/observability/synthetics/monitor-resources-on-private-networks.md)
    * Elastic’s global managed infrastructure

**Where you configure monitors**:

* **{{agent}} integration**: You could configure monitors using:

    * A user interface in {{kib}} (all monitor types)
    * Code in an external, version-controlled project (browser monitors *only*)

* **Projects or the {{synthetics-app}}**: You can configure monitors using:

    * A user interface in {{kib}} (all lightweight monitors, browser monitors via inline script only)
    * Code in an external, version-controlled project (all monitor types)

**How to use projects ([read more](#synthetics-migrate-integration-projects))**:

* **{{agent}} integration**:

    1. Created a project that uses `@elastic/synthetics`.
    2. Wrote journeys in JavaScript or TypeScript files.
    3. Zipped the entire project.
    4. Configured and created the monitor in the Integrations UI by adding a ZIP URL that pointed to the location of the project.

* **Projects or the {{synthetics-app}}**:

    1. Create a project that uses `@elastic/synthetics`.
    2. Configure lightweight monitors in YAML files.
    3. Write journeys in JavaScript or TypeScript files and configure individual monitors in your journey code using `monitor.use` or configure all monitors using the `synthetics.config.ts` file.
    4. Use the `elastic/synthetics push` command to create monitors.

Find more details in [Use {{project-monitors-cap}}](/solutions/observability/synthetics/create-monitors-with-projects.md).

**How to use the UI ([read more](#synthetics-migrate-integration-ui))**:

* **{{agent}} integration**:

    1. Went to the **Integrations** page in {{kib}}.
    2. Searched for and added the **Elastic Synthetics** integration.
    3. Configured the monitor.
    4. Created the monitor.

* **Projects or the {{synthetics-app}}**:

    1. Go to **Synthetics** in {{kib}}.
    2. Go to **Management**.
    3. Click **Create monitor**.
    4. Configure the monitor.
    5. Create the monitor.

Find more details in [Use the {{synthetics-app}}](/solutions/observability/synthetics/create-monitors-ui.md).

## Where monitors run [synthetics-migrate-integration-location]

If you want to continue hosting on your infrastructure, you will need to create a {{private-location}} before creating monitors. If you have already have an {{agent}} running using `elastic-agent-complete`, you can [add it as a new {{private-location}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-add) in the {{synthetics-app}}. To create a new {{private-location}} from scratch, follow all instructions in [Monitor resources on private networks](/solutions/observability/synthetics/monitor-resources-on-private-networks.md).

Alternatively, you can start hosting on Elastic’s global managed infrastructure. With Elastic’s global managed testing infrastructure, you can create and run monitors in multiple locations without having to manage your own infrastructure. Elastic takes care of software updates and capacity planning for you.

Executing synthetic tests on Elastic’s global managed testing infrastructure incurs an additional charge. Tests are charged under one of two new billing dimensions depending on the monitor type. For *browser monitor* usage, there is a fee per test run. For *lightweight monitor* usage, there is a fee per region in which you run any monitors regardless of the number of test runs. For more details, refer to [full details and current pricing](https://www.elastic.co/pricing).

## How to use projects [synthetics-migrate-integration-projects]

If you already have an external project you were adding via a ZIP URL you can use the same project, but you will have to make some changes.

First, upgrade the existing project to use the latest version of `@elastic/synthetics`:

1. Run `npm install -g @elastic/synthetics@latest` to install the latest version of the CLI.
2. Upgrade your existing project to use new project settings:

    1. Run `npm @elastic/synthetics init <path-to-existing-project>`.
    2. Respond to all prompts provided by the CLI.

        ::::{note}
        To ensure that your project will work with the latest version of Elastic Synthetics, the CLI will create a new configuration file on `init`, but you will see a prompt asking if you would like to continue before overwriting an existing configuration file.

        ::::

3. Review updated files and directories, including:

    1. `journeys/` will contain sample journey code. Move existing journey files into this directory.
    2. `synthetics.config.ts` will contain updated default settings needed for the upgraded project.
    3. `package.json` will contain updated NPM settings for your project.

        ::::{note}
        If there is already a `package.json` file in the directory when you run `init`, the synthetics agent will *not* create a new `package.json` file. Instead it will modify the existing `package.json` file to:

        * Add `@elastic/synthetics` library to the dependencies if it’s not already present.
        * Add a `test` and `push` script if they are not already present.

        ::::

    4. `.github/` will contain sample workflow files to use with GitHub Actions.

Then, you can further configure monitors as needed. In the upgraded project, you’ll use code (instead of the Integrations UI) to define settings like the name of the monitor and the frequency at which it will run. There are two ways you can configure monitors using code:

* For individual monitors, use `monitor.use` directly in the journey code. Read more in [Configure individual monitors](/solutions/observability/synthetics/configure-individual-browser-monitors.md).
* To configure all monitors at once, use the synthetics configuration file. Read more in [Configure projects](/solutions/observability/synthetics/configure-projects.md).

Finally, you’ll create monitors using `push` instead of by adding a ZIP URL in the Integrations UI. This will require an API token. Read more in [`@elastic/synthetics push`](/solutions/observability/synthetics/cli.md#elastic-synthetics-push-command).

Optionally, you can also add lightweight monitors to the project in YAML files. Read more about adding lightweight monitors to projects in [Configure lightweight monitors](/solutions/observability/synthetics/configure-lightweight-monitors.md).

For more information on getting started with projects, refer to [Use {{project-monitors-cap}}](/solutions/observability/synthetics/create-monitors-with-projects.md).

## How to use the UI [synthetics-migrate-integration-ui]

If you created monitors solely via the Elastic Synthetics integration UI, you can recreate monitors in the {{synthetics-app}}.

The configuration options in the {{synthetics-app}} look very similar to the Elastic Synthetics integration UI with a few exceptions. In the {{synthetics-app}}:

1. You will select one or more locations for each monitor.
2. You cannot use a ZIP URL for browser monitors. Use projects instead.
3. You can test the configuration (including the journey for browser monitors) using **Run test** before creating the monitor.

For more information on getting started with the {{synthetics-app}}, refer to [Use the {{synthetics-app}}](/solutions/observability/synthetics/create-monitors-ui.md).

