---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-configuration.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-configuration.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Configure a Synthetics project [observability-synthetics-configuration]

Synthetic tests support the configuration of dynamic parameters that can be used in Synthetics projects. In addition, the Synthetics agent, which is built on top of Playwright, supports configuring browser and context options that are available in Playwright-specific methods, for example, `ignoreHTTPSErrors`, `extraHTTPHeaders`, and `viewport`.

Create a `synthetics.config.js` or `synthetics.config.ts` file in the root of the Synthetics project and specify the options. For example:

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack
```ts
import type { SyntheticsConfig } from '@elastic/synthetics';

export default env => {
  const config: SyntheticsConfig = {
    params: {
      url: 'https://www.elastic.co',
    },
    playwrightOptions: {
      ignoreHTTPSErrors: false,
    },
    /**
     * Configure global monitor settings
     */
    monitor: {
      schedule: 10,
      locations: [ 'us_east' ],
    },
    /**
     * Project monitors settings
     */
    project: {
      id: 'my-project',
      url: 'https://abc123',
      space: 'custom-space',
    },
  };
  if (env !== 'development') {
    /**
     * Override configuration specific to environment
     * For example, config.params.url = ""
     */
  }
  return config;
};
```
:::

:::{tab-item} Serverless
:sync: serverless

```ts
import type { SyntheticsConfig } from '@elastic/synthetics';

export default env => {
  const config: SyntheticsConfig = {
    params: {
      url: 'https://www.elastic.co',
    },
    playwrightOptions: {
      ignoreHTTPSErrors: false,
    },
    /**
     * Configure global monitor settings
     */
    monitor: {
      schedule: 10,
      locations: [ 'us_east' ],
    },
    /**
     * Synthetic project monitors settings
     */
    project: {
      id: 'my-synthetics-project',
      url: 'https://abc123',
    },
  };
  if (env !== 'development') {
  /**
   * Override configuration specific to environment
   * For example, config.params.url = ""
   */
  }
  return config;
};
```
:::

::::

::::{note}
`env` in the example above is the environment you are pushing from *not* the environment where monitors will run. In other words, `env` corresponds to the configured `NODE_ENV`.

::::

The configuration file can either export an object, or a function that when called should return the generated configuration. To know more about configuring the tests based on environments, look at the [dynamic configuration](/solutions/observability/synthetics/work-with-params-secrets.md#synthetics-dynamic-configs) documentation.

## `params` [synthetics-configuration-params]

A JSON object that defines any variables your tests require. Read more in [Work with params and secrets](/solutions/observability/synthetics/work-with-params-secrets.md).

## `playwrightOptions` [synthetics-configuration-playwright-options]

For all available options, refer to the [Playwright documentation](https://playwright.dev/docs/test-configuration).

::::{note}
Do not attempt to run in headful mode (using `headless:false`) when running through Elastic’s global managed testing infrastructure or Private Locations as this is not supported.

::::

Below are details on a few Playwright options that are particularly relevant to Elastic Synthetics including TLS client authentication, timeouts, timezones, and device emulation.

### TLS client authentication [synthetics-configuration-playwright-options-client-certificates]

To enable TLS client authentication, set the [`clientCertificates`](https://playwright.dev/docs/api/class-testoptions#test-options-client-certificates) option in the configuration file:

::::{note}
Path-based options `{certPath, keyPath, pfxPath}` are only supported on Private Locations, defer to in-memory alternatives `{cert, key, pfx}` when running on locations hosted by Elastic.

::::

```js
playwrightOptions: {
  clientCertificates: [
    {
      origin: 'https://example.com',
      certPath: './cert.pem',
      keyPath: './key.pem',
      passphrase: 'mysecretpassword',
    },
    {
      origin: 'https://example.com',
      cert: Buffer.from("-----BEGIN CERTIFICATE-----\n..."),
      key: Buffer.from("-----BEGIN RSA PRIVATE KEY-----\n..."),
      passphrase: 'mysecretpassword',
    }
  ],
}
```

::::{tip}
When using Synthetics monitor UI, `cert`, `key` and `pfx` can simply be specified using a string literal:

```js
clientCertificates: [
  {
    cert: "-----BEGIN CERTIFICATE-----\n...",
    // Not cert: Buffer.from("-----BEGIN CERTIFICATE-----\n..."),
  }
],
```

::::

### Timeouts [synthetics-configuration-playwright-options-timeouts]

Playwright has two types of timeouts that are used in Elastic Synthetics: [action and navigation timeouts](https://playwright.dev/docs/test-timeouts#action-and-navigation-timeouts).

Elastic Synthetics uses a default action and navigation timeout of 50 seconds. You can override this default using [`actionTimeout`](https://playwright.dev/docs/api/class-testoptions#test-options-action-timeout) and [`navigationTimeout`](https://playwright.dev/docs/api/class-testoptions#test-options-navigation-timeout) in `playwrightOptions`.

### Timezones and locales [synthetics-configuration-playwright-options-timezones]

The Elastic global managed testing infrastructure does not currently set the timezone. For {{private-location}}s, the monitors will use the timezone of the host machine running the {{agent}}. This is not always desirable if you want to test how a web application behaves across different timezones. To specify what timezone to use when the monitor runs, you can use `playwrightOptions` on a per monitor or global basis.

To use a timezone and/or locale for all monitors in the Synthetics project, set [`locale` and/or `timezoneId`](https://playwright.dev/docs/emulation#locale%2D%2Dtimezone) in the configuration file:

```js
playwrightOptions: {
  locale: 'en-AU',
  timezoneId: 'Australia/Brisbane',
}
```

To use a timezone and/or locale for a *specific* monitor, add these options to a journey using [`monitor.use`](/solutions/observability/synthetics/configure-individual-browser-monitors.md).

### Device emulation [synthetics-config-device-emulation]

Users can emulate a mobile device using the configuration file. The example configuration below runs tests in "Pixel 5" emulation mode.

```js
import { SyntheticsConfig } from "@elastic/synthetics"
import { devices } from "playwright-chromium"

const config: SyntheticsConfig = {
  playwrightOptions: {
    ...devices['Pixel 5']
  }
}

export default config;
```

## `project` [synthetics-configuration-project]

Information about the Synthetics project.

`id` (`string`)
:   A unique id associated with your Synthetics project. It will be used for logically grouping monitors.

    If you used [`init` to create a Synthetics project](/solutions/observability/synthetics/cli.md#elastic-synthetics-init-command), this is the `<name-of-synthetics-project>` you specified.

`url` (`string`)
:   The URL for the Serverless Observability project or the {{kib}} URL for the deployment to which you want to upload the monitors.

space (`string`)
:   For {{kib}} deployments 9.0 or higher, the identifier of the target [{{kib}} space](/deploy-manage/manage-spaces.md) for the pushed monitors. Spaces help you organize pushed monitors. Pushes to the "default" space if not specified.

## `monitor` [synthetics-configuration-monitor]

Default values to be applied to *all* monitors when using the [`@elastic/synthetics` `push` command](/solutions/observability/synthetics/cli.md#elastic-synthetics-push-command).

`id` (`string`)
:   A unique identifier for this monitor.

$$$synthetics-configuration-monitor-name$$$ `name` (`string`)
:   A human readable name for the monitor.

$$$synthetics-configuration-monitor-tags$$$ `tags` (`Array<string>`)
:   A list of tags that will be sent with the monitor event. Tags are displayed in the Synthetics UI and allow you to search monitors by tag.

`schedule` (`number`)
:   The interval (in minutes) at which the monitor should run.

`enabled` (`boolean`)
:   Enable or disable the monitor from running without deleting and recreating it.

`locations` ([`Array<SyntheticsLocationsType>`](https://github.com/elastic/synthetics/blob/v1.3.0/src/locations/public-locations.ts#L28-L37))
:   Where to deploy the monitor. Monitors can be deployed in multiple locations so that you can detect differences in availability and response times across those locations.

    To list available locations you can:

    * Run the [`elastic-synthetics locations` command](/solutions/observability/synthetics/cli.md#elastic-synthetics-locations-command).
    * Find `Synthetics` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) and click **Create monitor**. Locations will be listed in *Locations*.

`privateLocations` (`Array<string>`)
:   The [{{private-location}}s](/solutions/observability/synthetics/monitor-resources-on-private-networks.md) to which the monitors will be deployed. These {{private-location}}s refer to locations hosted and managed by you, whereas `locations` are hosted by Elastic. You can specify a {{private-location}} using the location’s name.

    To list available {{private-location}}s you can:

    * Run the [`elastic-synthetics locations` command](/solutions/observability/synthetics/cli.md#elastic-synthetics-locations-command) with the URL for the Observability project or the {{kib}} URL for the deployment from which to fetch available locations.
    * Find `Synthetics` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) and click **Create monitor**. {{private-location}}s will be listed in *Locations*.

`throttling` (`boolean` | [`ThrottlingOptions`](https://github.com/elastic/synthetics/blob/v1.3.0/src/common_types.ts#L194-L198))
:   Control the monitor’s download speeds, upload speeds, and latency to simulate your application’s behavior on slower or laggier networks. Set to `false` to disable throttling altogether.

`screenshot` ([`ScreenshotOptions`](https://github.com/elastic/synthetics/blob/v1.3.0/src/common_types.ts#L192))
:   Control whether or not to capture screenshots. Options include `'on'`, `'off'`, or `'only-on-failure'`.

`alert.status.enabled` (`boolean`)
:   Enable or disable monitor status alerts. Read more about alerts in [Alerting](/solutions/observability/synthetics/configure-settings.md#synthetics-settings-alerting).

`retestOnFailure` (`boolean`)
:   Enable or disable retesting when a monitor fails. Default is `true`.

    By default, monitors are automatically retested if the monitor goes from "up" to "down". If the result of the retest is also "down", an error will be created, and if configured, an alert sent. Then the monitor will resume running according to the defined schedule.

    Using `retestOnFailure` can reduce noise related to transient problems.

`fields` (`object`)
:   A list of key-value pairs that will be sent with each monitor event. The `fields` are appended to {{es}} documents as `labels`, and those labels are displayed in {{kib}} in the *Monitor details* panel in the [individual monitor’s *Overview* tab](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-individual-monitors-overview).

    For example:

    ```js
    fields: {
      foo: 'bar',
      team: 'synthetics',
    }
    ```

For information on configuring monitors individually, refer to:

* [Configure individual browser monitors](/solutions/observability/synthetics/configure-individual-browser-monitors.md) for browser monitors
* [Configure lightweight monitors](/solutions/observability/synthetics/configure-lightweight-monitors.md) for lightweight monitors

## `proxy` [synthetics-configuration-proxy]

`uri` (`string`)
:   The Proxy URL to be used when connecting to the deployment or Observability Serverless project.

`token` (`string`)
:   (Optional) The authentication token to be used when connecting to the proxy URL. Based on auth header format `Basic Asaaas==`

`ca` (`string | Buffer`)
:   (Optional) Override the trusted CA certificates for the proxy connection.

`noVerify` (`boolean`)
:   (Optional) Disable TLS verification for the proxy connection.