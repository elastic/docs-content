---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/synthetics-params-secrets.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-params-secrets.html
---

# Work with params and secrets [observability-synthetics-params-secrets]

Params allow you to use dynamically defined values in your synthetic monitors. For example, you may want to test a production website with a particular demo account whose password is only known to the team managing the synthetic monitors.

For more information about security-sensitive use cases, refer to [Working with secrets and sensitive values](../../../solutions/observability/apps/work-with-params-secrets.md#synthetics-secrets-sensitive).


## Define params [synthetics-params-secrets-define]

Param values can be declared by any of the following methods:

* In the *Global parameters* tab of the [Synthetics Settings page in an Observability project](../../../solutions/observability/apps/configure-synthetics-settings.md#synthetics-settings-global-parameters).
* Declaring a default value for the parameter in a [configuration file](../../../solutions/observability/apps/work-with-params-secrets.md#synthetics-dynamic-configs).
* Passing the `--params` [CLI argument](../../../solutions/observability/apps/work-with-params-secrets.md#synthetics-cli-params).

::::{note}
If you are creating and managing synthetic monitors using a [Synthetics project](../../../solutions/observability/apps/create-monitors-with-project-monitors.md), you can also use regular environment variables via the standard node `process.env` global object.

::::


The values in the configuration file are read in the following order:

1. **Global parameters in an Observability project**: The *Global parameters* set using the UI are read first.
2. **Configuration file**: Then the *Global parameters* are merged with any parameters defined in a configuration file. If a parameter is defined in both the Observability UI **and** a Synthetics project configuration file, the value in the configuration file will be used.
3. **CLI**: Then the parameters defined in the configuration are merged with any parameters passed to the CLI `--params` argument. If a parameter is defined in a Synthetics project configuration file **and** using the CLI argument, the value defined using the CLI will be used. When running a script using the CLI, *Global parameters* defined in {{kib}} or the Observability Serverless project have no impact on the test because it won’t have access to {{kib}} or the Observability project.


### Global parameters in your Observability project [observability-synthetics-params-secrets-global-parameters-in-your-observability-project]

From any page in the Synthetics UI:

1. Go to **Settings**.
2. Go to the **Global parameters** tab.
3. Define parameters.

:::{image} ../../../images/observability-synthetics-params-secrets-kibana-define.png
:alt: Global parameters tab on the Synthetics Settings page
:class: screenshot
:::


### Synthetics project config file [synthetics-dynamic-configs]

Use a `synthetics.config.js` or `synthetics.config.ts` file to define variables required by your tests. This file should be placed in the root of your Synthetics project.

```js
export default (env) => {
  let my_url = "http://localhost:8080";
  if (env === "production") {
    my_url = "https://elastic.github.io/synthetics-demo/"
  }
  return {
    params: {
      my_url,
    },
  };
};
```

The example above uses the `env` variable, which corresponds to the value of the `NODE_ENV` environment variable.


### CLI argument [synthetics-cli-params]

To set parameters when running [`npx @elastic/synthetics` on the command line](../../../solutions/observability/apps/use-synthetics-cli.md), use the `--params` or `-p` flag. The provided map is merged over any existing variables defined in the `synthetics.config.{js,ts}` file.

For example, to override the `my_url` parameter, you would run:

```sh
npx @elastic/synthetics . --params '{"my_url": "http://localhost:8080"}'
```


## Use params [synthetics-params-secrets-use]

You can use params in both lightweight and browser monitors created in either a Synthetics project or the Synthetics UI.


### In a Synthetics project [synthetics-params-secrets-use-project]

For lightweight monitors in a Synthetics project, wrap the name of the param in `${}` (for example, `${my_url}`).

```yaml
- type: http
  name: Todos Lightweight
  id: todos-lightweight
  urls: ["${my_url}"]
  schedule: '@every 1m'
```

In browser monitors, parameters can be referenced via the `params` property available within the argument to a `journey`, `before`, `beforeAll`, `after`, or `afterAll` callback function.

Add `params.` before the name of the param (for example, `params.my_url`):

```js
beforeAll(({params}) => {
  console.log(`Visiting ${params.my_url}`)
})

journey("My Journey", ({ page, params }) => {
  step('launch app', async () => {
    await page.goto(params.my_url)   <1>
  })
})
```

1. If you are using TypeScript, replace `params.my_url` with `params.my_url as string`.



### In the UI [synthetics-params-secrets-use-ui]

To use a param in a lightweight monitor that is created in the Synthetics UI, wrap the name of the param in `${}` (for example, `${my_url}`).

:::{image} ../../../images/serverless-synthetics-params-secrets-kibana-use-lightweight.png
:alt: Use a param in a lightweight monitor created in the Synthetics UI
:class: screenshot
:::

To use a param in a browser monitor that is created in the Synthetics UI, add `params.` before the name of the param (for example, `params.my_url`).

:::{image} ../../../images/observability-synthetics-params-secrets-kibana-use-lightweight.png
:alt: Use a param in a lightweight monitor created in the Synthetics UI
:class: screenshot
:::


## Working with secrets and sensitive values [synthetics-secrets-sensitive]

Your synthetics scripts may require the use of passwords or other sensitive secrets that are not known until runtime.

::::{warning}
Params are viewable in plain-text by administrators and other users with `all` privileges for the Synthetics app. Also note that synthetics scripts have no limitations on accessing these values, and a malicious script author could write a synthetics journey that exfiltrates `params` and other data at runtime. Do **not** use truly sensitive passwords (for example, an admin password or a real credit card) in **any** synthetics tools. Instead, set up limited demo accounts, or fake credit cards with limited functionality. If you want to limit access to parameters, ensure that users who are not supposed to access those values do not have `all` privileges for the Synthetics app, and that any scripts that use those values do not leak them in network requests or screenshots.

::::


If you are managing monitors with a Synthetics project, you can use environment variables in your `synthetics.config.ts` or `synthetics.config.js` file.

The example below uses `process.env.MY_URL` to reference a variable named `MY_URL` defined in the environment and assigns its value to a param. That param can then be used in both lightweight and browser monitors that are managed in the Synthetics project:

```js
export default {
  params: {
    my_url: process.env.MY_URL
  }
};
```