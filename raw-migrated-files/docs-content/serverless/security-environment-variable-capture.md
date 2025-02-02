# Capture environment variables [security-environment-variable-capture]

You can configure an {{agent}} policy to capture up to five environment variables (`env vars`).

::::{note}
* Env var names must be no more than 63 characters, and env var values must be no more than 1023 characters. Values outside these limits are silently ignored.
* Env var names are case sensitive.

::::


To set up environment variable capture for an {{agent}} policy:

1. Find **Policies** in the navigation menu or use the global search field.
2. Select an {{agent}} policy.
3. Click **Show advanced settings**.
4. Scroll down or search for `linux.advanced.capture_env_vars`, or `mac.advanced.capture_env_vars`.
5. Enter the names of env vars you want to capture, separated by commas. For example: `PATH,USER`
6. Click **Save**.


## Find captured environment variables [find-cap-env-vars]

Captured environment variables are associated with process events, and appear in each event’s `process.env_vars` field.

To view environment variables in the **Events** table:

1. Click the **Events** tab on the **Hosts***, ***Network***, or ***Users** pages, then click **Fields** in the Events table.
2. Search for the `process.env_vars` field, select it, and click **Close**. A new column appears containing captured environment variable data.

:::{image} ../../../images/serverless--cloud-native-security-env-var-capture-detail.png
:alt: The Events table with the "process.env_vars" column highlighted
:class: screenshot
:::
