---
navigation_title: Kerberos for browser monitors
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-kerberos.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-kerberos.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Kerberos authentication for browser monitors [synthetics-kerberos]

Kerberos authentication enables monitoring on single sign-on (SSO) protected sites, usually behind Microsoft Active Directory.

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` HTTP monitors reach Kerberos-protected endpoints a different way. Rather than the Chromium settings described here, they take a `kerberos` block in the monitor configuration. Like browser monitors, they only run from {{private-location}}s. For the fields that block takes, refer to the [HTTP options](/solutions/observability/synthetics/configure-lightweight-monitors.md#synthetics-lightweight-http).

:::{admonition} Requirements
* Kerberos authentication works for **Private Locations only**. It does not work from Elastic's managed global locations.
* Provide the agent process with a keytab for the service account and a `kinit` 'd ticket cache (KRB5CCNAME). Use a cron job or systemd timer to renew the ticket regularly (for example, `kinit -R` every few hours, or `kinit -kt` on failure).
* Configure `/etc/krb5.conf` for your realm.
* Register the SPN (for example, `HTTP/intranet.corp.local@CORP.LOCAL`) on the service account that fronts the protected URL.
:::

## Configuring Kerberos authentication [configuring_kerberos]

Browser monitors support for SSO Kerberos authentication natively. Specify the protected domains under `playwrightOptions.args`:

```ts
playwrightOptions: {
  args: [
    '--auth-server-allowlist=*.corp.local,corp.local',
    '--auth-negotiate-delegate-allowlist=*.corp.local',
  ],
}
```

The hostname must match an entry in `--auth-server-allowlist`. Matching is hostname-only and supports shell-style wildcards — `*.corp.local` will not match the bare `corp.local`.