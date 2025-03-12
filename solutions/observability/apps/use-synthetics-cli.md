---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/synthetics-command-reference.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-command-reference.html

navigation_title: "Use the CLI"
---

# Use the Synthetics CLI [synthetics-command-reference]



## `@elastic/synthetics` [elastic-synthetics-command]

Elastic uses the [@elastic/synthetics](https://www.npmjs.com/package/@elastic/synthetics) Node.js library to run synthetic browser tests and report the test results. The library also provides a CLI to help you scaffold, develop/run tests locally, and push tests to {{kib}}.

```sh
npx @elastic/synthetics [options] [files] [dir]
```

You will not need to use most command line flags. However, there are some you may find useful:

`--match <string>`
:   run tests with a name or tags that match the given glob pattern.

`--tags Array<string>`
:   run tests with the given tags that match the given glob pattern.

`--pattern <string>`
:   RegExp pattern to match journey files in the current working directory. Defaults to `/*.journey.(ts|js)$/`, which matches files ending with `.journey.ts` or `.journey.js`.

`--params <jsonstring>`
:   JSON object that defines any variables your tests require. Read more in [Work with params and secrets](../../../solutions/observability/apps/work-with-params-secrets.md).

    Params passed will be merged with params defined in your [`synthetics.config.js` file](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-params). Params defined via the CLI take precedence.


`--playwright-options <jsonstring>`
:   JSON object to pass in custom Playwright options for the agent. For more details on relevant Playwright options, refer to the [the configuration docs](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-playwright-options).

    Options passed will be merged with Playwright options defined in your [`synthetics.config.js` file](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-playwright-options). Options defined via the CLI take precedence.


`--screenshots <on|off|only-on-failure>`
:   Control whether or not to capture screenshots at the end of each step. Options include `'on'`, `'off'`, or `'only-on-failure'`.

    This can also be set in the configuration file using [`monitor.screenshot`](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-monitor). The value defined via the CLI will take precedence.


`-c, --config <string>`
:   Path to the configuration file. By default, test runner looks for a `synthetics.config.(js|ts)` file in the current directory. Synthetics configuration provides options to configure how your tests are run and pushed to Elastic. Allowed options are described in the [configuration file](../../../solutions/observability/apps/configure-synthetics-projects.md).

`--reporter <json|junit|buildkite-cli|default>`
:   One of `json`, `junit`, `buildkite-cli`, or `default`. Use the JUnit or Buildkite reporter to provide easily parsed output to CI systems.

`--inline`
:   Instead of reading from a file, `cat` inline scripted journeys and pipe them through `stdin`. For example, `cat path/to/file.js | npx @elastic/synthetics --inline`.

`--no-throttling`
:   Does not apply throttling.

    Throttling can also be disabled in the configuration file using [`monitor.throttling`](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-monitor). The value defined via the CLI will take precedence.


::::{note}
Network throttling for browser based monitors is disabled. See this [documention](https://github.com/elastic/synthetics/blob/main/docs/throttling.md) for more details.

::::


`--no-headless`
:   Runs with the browser in headful mode.

    This is the same as setting [Playwright’s `headless` option](https://playwright.dev/docs/api/class-testoptions#test-options-headless) to `false` by running `--playwright-options '{"headless": false}'`.


::::{note}
Headful mode should only be used locally to see the browser and interact with DOM elements directly for testing purposes. Do not attempt to run in headful mode when running through Elastic’s global managed testing infrastructure or {{private-location}}s as this is not supported.

::::


`-h, --help`
:   Shows help for the `npx @elastic/synthetics` command.

::::{note}
The `--pattern`, `--tags`, and `--match` flags for filtering are only supported when you run synthetic tests locally or push them to Elastic. Filtering is *not* supported in any other subcommands like `init` and `locations`.

::::


::::{note}
For debugging synthetic tests locally, you can set an environment variable, `DEBUG=synthetics npx @elastic/synthetics`, to capture Synthetics agent logs.

::::



## `@elastic/synthetics init` [elastic-synthetics-init-command]

Scaffold a new Synthetics project using Elastic Synthetics.

This will create a template Node.js project that includes the synthetics agent, required dependencies, a synthetics configuration file, and example browser and lightweight monitor files. These files can be edited and then pushed to Elastic to create monitors.

```sh
npx @elastic/synthetics init <name-of-project>
```

Read more about what’s included in a template Synthetics project in [Create a Synthetics project](../../../solutions/observability/apps/create-monitors-with-project-monitors.md).


## `@elastic/synthetics push` [elastic-synthetics-push-command]

Create monitors by using your local journeys. By default, running `push` command will use the `project` settings field from the `synthetics.config.ts` file, which is set up using the `init` command. However, you can override these settings using the CLI flags.

```sh
SYNTHETICS_API_KEY=<api-key> npx @elastic/synthetics push --url <kibana-url> --id <id|name>
```

::::{note}
The `push` command includes interactive prompts to prevent you from accidentally deleting or duplicating monitors. You will see a prompt when:

* You `push` a Synthetics project that used to contain one or more monitors but either no longer contains previously running monitors or has any monitors. Select `yes` to delete the monitors associated with the project ID being pushed.
* You `push` a Synthetics project that’s already been pushed using one Synthetics project ID and then try to `push` it using a *different* ID. Select `yes` to create duplicates of all monitors in the project. You can set `DEBUG=synthetics` environment variable to capture the deleted monitors.

::::


::::{note}
If the journey contains external NPM packages other than the `@elastic/synthetics`, those packages will be bundled along with the journey code when the `push` command is invoked. However there are some limitations when using external packages:

* Bundled journeys after compression should not be more than 1500 Kilobytes.
* Native node modules will not work as expected due to platform inconsistency.
* Uploading files in journey scripts(via locator.setInputFiles) is not supported.

::::


`--auth <string>`
:   API key used for [authentication](../../../deploy-manage/api-keys/elasticsearch-api-keys.md). You can also set the API key via the `SYNTHETICS_API_KEY` environment variable.

    If you are pushing to a [{{private-location}}](../../../solutions/observability/apps/create-monitors-in-synthetics-app.md), you must use an API key generated in 8.4 or higher.

    On {{stack}}, you must be logged into {{kib}} as a user with the privileges described in [Writer role](../../../solutions/observability/apps/writer-role.md) to create an API key.

    On {{obs-serverless}}, you must be logged in as a user with [Editor](../../../solutions/observability/apps/grant-users-access-to-secured-resources.md) access to create an API key.


`--id <string>`
:   A unique id associated with your project. It will be used for logically grouping monitors.

    If you used [`init` to create a project](../../../solutions/observability/apps/use-synthetics-cli.md#elastic-synthetics-init-command), this is the `<name-of-project>` you specified.

    This can also be set in the configuration file using [`project.id`](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-project). The value defined via the CLI will take precedence.


`--url <string>`
:   The URL for the deployment or Observability Serverless project to which you want to upload the monitors.

    This can also be set in the configuration file using [`project.url`](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-project). The value defined via the CLI will take precedence.

% Stateful only for --space

`--space <string>`
:   The identifier of the target [{{kib}} space](../../../deploy-manage/manage-spaces.md) for the pushed monitors. Spaces help you organize pushed monitors. Pushes to the "default" space if not specified.

    This can also be set in the configuration file using [`project.space`](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-project). The value defined via the CLI will take precedence.


`--schedule <number>`
:   The interval (in minutes) at which the monitor should run.

    This can also be set in the configuration file using [`monitor.schedule`](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-monitor). The value defined via the CLI will take precedence.


[`--locations Array<SyntheticsLocationsType>`](https://github.com/elastic/synthetics/blob/v1.3.0/src/locations/public-locations.ts#L28-L37)
:   Where to deploy the monitor. Monitors can be deployed in multiple locations so that you can detect differences in availability and response times across those locations.

    To list available locations, refer to [`@elastic/synthetics locations`](../../../solutions/observability/apps/use-synthetics-cli.md#elastic-synthetics-locations-command).

    This can also be set in the configuration file using [`monitor.locations` in the configuration file](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-monitor). The value defined via the CLI will take precedence.


`--private-locations Array<string>`
:   The [{{private-location}}s](../../../solutions/observability/apps/monitor-resources-on-private-networks.md) to which the monitors will be deployed. These {{private-location}}s refer to locations hosted and managed by you, whereas `locations` are hosted by Elastic. You can specify a {{private-location}} using the location’s name.

    To list available {{private-location}}s, refer to [`@elastic/synthetics locations`](../../../solutions/observability/apps/use-synthetics-cli.md#elastic-synthetics-locations-command).

    This can also be set in the configuration file using [`monitor.privateLocations` in the configuration file](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-monitor). The value defined via the CLI will take precedence.


`--fields <string>`
:   A list of key-value pairs that will be sent with each monitor event. The `fields` are appended to {{es}} documents as `labels`, and those labels are displayed in {{kib}} in the *Monitor details* panel in the [individual monitor’s *Overview* tab](../../../solutions/observability/apps/analyze-data-from-synthetic-monitors.md#synthetics-analyze-individual-monitors-overview).

    Example: `--fields '{ "foo": bar", "team": "synthetics" }'`

    This can also be set in the configuration file using [the `monitor.fields` option](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-monitor). The value defined via the CLI will take precedence.


`--yes`
:   The `push` command includes interactive prompts to prevent you from accidentally deleting or duplicating monitors. If running the CLI non-interactively, you can override these prompts using the `--yes` option. When the `--yes` option is passed to `push`:

    * If you `push` a Synthetics project that used to contain one or more monitors but no longer contains any monitors, all monitors associated with the Synthetics project ID being pushed will be deleted.
    * If you `push` a Synthetics project that’s already been pushed using one Synthetics project ID and then try to `push` it using a *different* ID, it will create duplicates of all monitors in the Synthetics project.



## Tag monitors [tagging-and-filtering]

Synthetics journeys can be tagged with one or more tags. Use tags to filter journeys when running tests locally or pushing them to Elastic.

To add tags to a single journey, add the `tags` parameter to the `journey` function or use the `monitor.use` method.

```js
import {journey, monitor} from "@elastic/synthetics";

journey({name: "example journey", tags: ["env:qa"] }, ({ page }) => {
  monitor.use({
    tags: ["env:qa"]
  })
  // Add steps here
});
```

For lightweight monitors, use the `tags` field in the yaml configuration file.

```yaml
name: example monitor
tags:
  - env:qa
```

To apply tags to all browser and lightweight monitors, configure using [the `monitor.tags`](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-monitor) field in the `synthetics.config.ts` file.


### Filter monitors [_filtering_monitors]

When running the `npx @elastic/synthetics push` command, you can filter the monitors that are pushed to {{kib}} using the following flags:

`--tags Array<string>`
:   Push monitors with the given tags that match the glob pattern.

`--match <string>`
:   Push monitors with a name or tags that match the glob pattern.

`--pattern <string>`
:   RegExp pattern to match the journey files in the current working directory. Defaults to `/*.journey.(ts|js)$/` for browser monitors and `/.(yml|yaml)$/` for lightweight monitors.

You can combine these techniques and push the monitors to different Kibana clusters/space based on the tags by using multiple configuration files.

```sh
npx @elastic/synthetics push --config synthetics.qa.config.ts --tags env:qa
npx @elastic/synthetics push --config synthetics.prod.config.ts --tags env:prod
```


## `@elastic/synthetics locations` [elastic-synthetics-locations-command]

List all available locations for running synthetics monitors.

```sh
npx @elastic/synthetics locations --url <host> --auth <api-key>
```

Run `npx @elastic/synthetics locations` with no flags to list all the available global locations managed by Elastic for running synthetics monitors.

To list both locations on Elastic’s global managed infrastructure and {{private-locations}}, include:

`--url <string>`
:   The URL for the {{kib}} deployment or Observability Serverless project from which to fetch all available public and {{private-location}}s.

`--auth <string>`
:   API key used for [authentication](../../../deploy-manage/api-keys/elasticsearch-api-keys.md).

::::{note}
If an administrator has disabled Elastic managed locations for the role you are assigned and you do *not* include `--url` and `--auth`, all global locations managed by Elastic will be listed. However, you will not be able to push to these locations with your API key and will see an error: *You don’t have permission to use Elastic managed global locations*. For more details, refer to the [troubleshooting docs](../../../troubleshoot/observability/troubleshooting-synthetics.md#synthetics-troubleshooting-public-locations-disabled).
::::


## `@elastic/synthetics totp <secret>` [elastic-synthetics-totp-command]

Generate a Time-based One-Time Password (TOTP) for multifactor authentication (MFA) in Synthetics.

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

```sh
npx @elastic/synthetics totp <secret>
npx @elastic/synthetics totp <secret> --issuer <string> --label <string>
```

:::

:::{tab-item} Serverless
:sync: serverless

```sh
npx @elastic/synthetics totp <secret> --issuer <issuer> --label <label>
```

:::

::::


`secret`
:   The encoded secret key used to generate the TOTP.

`--issuer <string>`
:   Name of the provider or service that is assocaited with the account.

`--label <string>`
:   Identifier for the account. Defaults to `SyntheticsTOTP`