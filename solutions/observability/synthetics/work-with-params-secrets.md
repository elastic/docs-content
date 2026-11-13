---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-params-secrets.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-params-secrets.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Work with params and secrets [observability-synthetics-params-secrets]

Params allow you to use dynamically defined values in your synthetic monitors. For example, you may want to test a production website with a particular demo account whose password is only known to the team managing the synthetic monitors.

For more information about security-sensitive use cases, refer to [Working with secrets and sensitive values](/solutions/observability/synthetics/work-with-params-secrets.md#synthetics-secrets-sensitive).

## Define params [synthetics-params-secrets-define]

You can declare param values any of the following ways:

* In the *Global parameters* tab of the [Synthetics Settings page in an Observability project](/solutions/observability/synthetics/configure-settings.md#synthetics-settings-global-parameters).
* Declaring a default value for the parameter in a [configuration file](/solutions/observability/synthetics/work-with-params-secrets.md#synthetics-dynamic-configs).
* Passing the `--params` [CLI argument](/solutions/observability/synthetics/work-with-params-secrets.md#synthetics-cli-params).

::::{note}
If you are creating and managing synthetic monitors using a [Synthetics project](/solutions/observability/synthetics/create-monitors-with-projects.md), you can also use regular environment variables via the standard node `process.env` global object.

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

:::{image} /solutions/images/observability-synthetics-params-secrets-kibana-define.png
:alt: Global parameters tab on the Synthetics Settings page
:screenshot:
:::

### Allow users to view global parameter values

```{applies_to}
stack: ga 9.1
serverless: ga
```

By default, custom user roles do not have access to global parameter values. Administrators can grant read access to global parameters by adding the Synthetics **Can read global parameter values** {{kib}} [sub-feature privilege](/solutions/observability/get-started/observability-kibana-privileges.md#synthetics-and-uptime-sub-feature-privileges) to a role. When added, users can view a global parameter value using the [**Get parameters** API]({{kib-apis}}operation/operation-get-parameters) or by selecting the {icon}`eye` icon.

To add the **Can read global parameter values** {{kib}} privilege to a role:

1. Go to the **Roles** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Edit an existing role or select **Create role**.
1. From the **Kibana** section, click **Assign to space**.
1. Expand `Synthetics and Uptime` in the list of [Observability {{kib}} privileges](/solutions/observability/get-started/observability-kibana-privileges.md).
2. Turn on **Customize sub-feature privileges**.
3. Turn on **Can read global parameter values**.
4. Click **Assign role**.

Refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for more on creating custom roles.

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

To set parameters when running [`npx @elastic/synthetics` on the command line](/solutions/observability/synthetics/cli.md), use the `--params` or `-p` flag. The provided map is merged over any existing variables defined in the `synthetics.config.{js,ts}` file.

For example, to override the `my_url` parameter, you would run:

```sh
npx @elastic/synthetics . --params '{"my_url": "http://localhost:8080"}'
```

## Use params [synthetics-params-secrets-use]

You can use params in both lightweight and browser monitors created in either a Synthetics project or the Synthetics UI.

### In a Synthetics project [synthetics-params-secrets-use-project]

For lightweight monitors in a Synthetics project, wrap the name of the param in `"${}"` (for example, `"${my_url}"`).

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

:::{image} /solutions/images/serverless-synthetics-params-secrets-kibana-use-lightweight.png
:alt: Use a param in a lightweight monitor created in the Synthetics UI
:screenshot:
:::

To use a param in a browser monitor that is created in the Synthetics UI, add `params.` before the name of the param (for example, `params.my_url`).

:::{image} /solutions/images/serverless-synthetics-params-secrets-kibana-use-browser.png
:alt: Use a param in a lightweight monitor created in the Synthetics UI
:screenshot:
:::

## Working with secrets and sensitive values [synthetics-secrets-sensitive]

Your synthetics scripts might require the use of passwords or other sensitive secrets that are not known until runtime.

::::{warning}
{applies_to}`serverless: ga`{applies_to}`stack: ga 9.1` Params are viewable by administrators and users with the **Can read global parameter values** {{kib}} privilege. Also, synthetics scripts have no limitations on accessing these values, and a malicious script author could write a synthetics journey that exfiltrates `params` and other data at runtime. Do **not** use truly sensitive passwords (for example, an admin password or a real credit card) in **any** synthetics tools. Instead, set up limited demo accounts, or fake credit cards with limited functionality. If you want to limit access to parameters, ensure that users who are not supposed to access those values do not have the **Can read global parameter values** {{kib}} privilege, and that any scripts that use those values do not leak them in network requests or screenshots.
::::

### Reference secrets from HashiCorp Vault [synthetics-secrets-vault]
```{applies_to}
stack: preview 9.6+
serverless: unavailable
```

Use HashiCorp Vault to keep secret values out of the monitor configuration stored in {{kib}}. A param or supported monitor field holds a reference to the secret. The {{agent}} running the monitor looks the value up in Vault when the monitor runs and caches it for five minutes, so {{kib}} never stores the secret value. {{kib}} does store each connection's credential as an encrypted saved object, and delivers it to the agent as a {{fleet}} secret.

This feature requires:

* A [{{private-location}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md) running {{agent}} 9.6 or later.
* Synthetics integration version 1.13.0 or later. To update an earlier version, refer to [Upgrade an integration](/reference/fleet/upgrade-integration.md).
* [{{fleet}} secret storage](/reference/fleet/agent-policy.md#agent-policy-secret-values) enabled.

A monitor that references a secret directly and runs on an Elastic managed location is rejected when you save it. This check doesn't cover params. If a param holds a reference, make sure the monitors that use it run only on private locations.

#### Add a Vault connection [synthetics-secrets-vault-connection]

Each connection holds the credential that reads secrets from one Vault account. You can add several per {{kib}} space.

To add, edit, test, or delete connections, you need the **Can manage** privilege under **Secret provider connections**. This privilege is included in **All** for **Synthetics and Uptime**. Refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for role configuration.

:::{warning}
Anyone who can edit monitors or global parameters in the space can reference any secret the connection's credential can read. Give each connection a dedicated, read-only credential scoped to the paths your monitors need. Monitor scripts can expose resolved values in logs, network requests, or screenshots.
:::

1. Go to **Synthetics** → **Settings** → **Global parameters**, then find **HashiCorp Vault connections**.
2. Click **Add connection** and fill in the fields:

    | Field | Description |
    | --- | --- |
    | **Name** | The name you reference the connection by, such as `prod`. You can't change it after you save the connection. |
    | **Vault address** | The address of your Vault server, such as `https://vault.example.com:8200`. It must use `https`, unless the host is a loopback address such as `localhost` or `127.0.0.1`. It can't include credentials, a query string, or a fragment, and it can't be a link-local address such as `169.254.169.254`. If `xpack.synthetics.secretConnections.allowedHosts` limits which hosts {{kib}} can contact, the host must be on that list. |
    | **Auth method** | Can be a **Token**, or an AppRole with a **Role ID** and **Secret ID**. |
    | **KV v2 mount** | Optional. It's the KV v2 secrets engine mount that holds the secrets this connection reads. Defaults to `secret`. |
    | **Allowed monitor hosts** | Decides which monitor targets might receive secrets from this connection. Leave it empty to allow any host. |
    | **Skip TLS verification (dev only)** | Turns off certificate validation. Use it only against a development Vault server. |

3. Click **Test connection** to check that {{kib}} can reach and authenticate with Vault, then click **Save connection**.

Test connection runs from {{kib}}. A monitor looks secrets up from the {{private-location}}'s network instead, so confirm that the agents can also reach the address. A loopback address can't be tested from {{kib}} at all, because it refers to whichever host is making the request.

To change a connection later, click **Edit**. You can edit a connection even if params and monitors are already using it. You can also enter a new credential to rotate it.

You can leave the secret field blank to keep the stored credential unless you:

* Change **Vault address**, **Auth method**, or **Skip TLS verification (dev only)**.
* Add hosts to an existing **Allowed monitor hosts** list or remove the restriction.

These changes require you to re-enter the credential. Adding a restriction to an unrestricted connection or narrowing an existing list doesn't require re-entry.

If you add or narrow **Allowed monitor hosts**, the form lists the monitors that the restriction would stop before you save.

To remove a connection, click **Delete**. However, this fails while any param or monitor still names it, so point them at another connection first.

#### Reference a secret [synthetics-secrets-vault-reference]

Reference a secret by connection name, path, and field:

```text
vault://<connection>@<secret-path>#<field>
```

The connection name is required. For example, a param or a monitor's request header can hold:

```text
Bearer vault://prod@myapp/credentials#password
```

Use only letters, digits, `.`, `_`, and `-`, plus `/` to separate segments of the path. Percent-encoded characters aren't accepted. {{kib}} rejects a reference that is malformed, names a connection that doesn't exist, or leaves the connection name out.

References work in params and in these monitor fields: **Username**, **Password**, **Request headers**, **Request body**, **Request payload** (TCP monitors), **Parameters** (browser monitors), and the TLS **Client certificate**, **Client key**, and **Client key passphrase**. {{kib}} rejects a reference in any other field, such as the URL, when you save the monitor. References don't work in browser monitor scripts. Pass a secret into a script through a param instead.

After saving the monitor, run it from its {{private-location}} and confirm that the request using the secret succeeds. This verifies access from the agent's network, which **Test connection** doesn't check.

#### Limit which hosts receive a secret [synthetics-secrets-vault-allowed-hosts]

**Allowed monitor hosts** restricts a connection so its secrets only reach the targets you list. Enter up to 100 host names or IP addresses without a scheme, port, path, or wildcard, using the punycode form for international names.

When the list isn't empty, the connection becomes much narrower:

* Only HTTP, TCP, and ICMP monitors can use it, and every target and proxy the monitor uses must be on the list.
* Browser monitors can't use it at all.
* Monitors that follow redirects or use Kerberos can't use it either.

A monitor that the restriction excludes reports down, and the secret isn't sent.

#### Configure {{kib}} settings [synthetics-secrets-vault-settings]

Set these in `kibana.yml`:

`xpack.synthetics.secretConnections.enabled`
:   Turns Vault connections and secret references on or off. Defaults to `true`. When it's `false`, the **HashiCorp Vault connections** panel is hidden and a monitor that contains a reference is rejected when you save it.

`xpack.synthetics.secretConnections.allowedHosts`
:   The Vault host names {{kib}} can contact when you save or test a connection. Defaults to `['*']`, which allows any host. Host names must match exactly, and the only wildcard supported is the literal `*`. A connection whose host isn't on the list can't be saved or tested, and monitors that reference a connection saved before the list was tightened fail until its host is added again. Accepts up to 1000 entries.

#### Known limitations [synthetics-secrets-vault-limitations]

* The {{agent}} resolves references before each monitor run, reusing secret values cached for five minutes. After an agent receives a saved connection update, it fetches fresh values on the next run that uses that connection.
* {{kib}} doesn't detect references inside base64-encoded Kerberos and NTLM fields, so a secret referenced there is never looked up.
* Deleting or changing a connection doesn't revoke its credential in Vault. The running agent process can retain connection credentials and configuration, and an offline {{agent}} doesn't receive updates until it reconnects. This is separate from the five-minute cache for retrieved secret values. To withdraw access, revoke the credential in Vault and rotate any secrets it retrieved.

### Use environment variables in Synthetics Projects

If you are managing monitors with a Synthetics project, you can use environment variables in your `synthetics.config.ts` or `synthetics.config.js` file.

The example below uses `process.env.MY_URL` to reference a variable named `MY_URL` defined in the environment and assigns its value to a param. That param can then be used in both lightweight and browser monitors that are managed in the Synthetics project:

```js
export default {
  params: {
    my_url: process.env.MY_URL
  }
};
```

### Use environment variables with Private Locations

If you are using Kibana-managed monitors and running them on a Private Location, you can inject environment variables directly into the agent's runtime environment.
This method allows you to keep sensitive values out of the {{kib}} UI. Instead, it stores those values on the infrastructure hosting the {{agent}}.

::::{warning}
These variables are accessible to all monitors running on this specific Private Location.

::::

#### 1. Pass variables to the Private Location
When starting your Private Location ({{agent}}) using Docker, use the `--env` flag to pass your variables.



```bash
docker run \
  --env FLEET_ENROLL=1 \
  --env FLEET_URL={fleet_server_host_url} \
  --env FLEET_ENROLLMENT_TOKEN={enrollment_token} \
  --env MY_URL={secret_value} \
  --cap-add=NET_RAW \
  --cap-add=SETUID \
  -d --restart=unless-stopped \
  docker.elastic.co/elastic-agent/elastic-agent-complete:X.X.X
```

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` On a [scalable {{private-location}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-scalable), each monitor runs on one {{agent}} and can move to another agent that shares the location's agent policy. Start every agent with the same `--env` variables. If an agent is missing a variable, the monitor fails when it runs there.

#### 2. Reference variables in the inline script
In the Synthetics **Monitors** editor in {{kib}}, you can now access these variables using `process.env`.

```js
step('navigate to secure url', async () => {
  // The script reads the environment variable from the private location elastic agent container
  await page.goto(process.env.MY_URL);
});
```
