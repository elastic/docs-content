---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/environment-variable-capture.html
  - https://www.elastic.co/guide/en/serverless/current/security-environment-variable-capture.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Capture environment variables

You can configure an {{agent}} policy to capture up to five environment variables (`env vars`).

::::{note}
* Env var names must be no more than 63 characters, and env var values must be no more than 1023 characters. Values outside these limits are silently ignored.
* Env var names are case sensitive in Linux.

::::


To set up environment variable capture for an {{agent}} policy:

1. Find **Policies** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select an {{agent}} policy.
3. Click **Show advanced settings**.
4. Scroll down or search for `linux.advanced.capture_env_vars` or `mac.advanced.capture_env_vars`.
5. Enter the names of env vars you want to capture, separated by commas. For example: `PATH,USER`
6. Click **Save**.


## Find captured environment variables [find-cap-env-vars]

Captured environment variables are associated with process events, and appear in each event’s `process.env_vars` field.

To view environment variables in the **Events** table:

1. Click the **Events** tab on the **Hosts**, **Network**, or **Users** pages, then click **Fields** in the Events table.
2. Search for the `process.env_vars` field, select it, and click **Close**. A new column appears containing captured environment variable data.

:::{image} /solutions/images/security-env-var-capture-detail.png
:alt: The Events table with the "process.env_vars" column highlighted
:::
