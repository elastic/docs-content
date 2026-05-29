---
navigation_title: Kerberos Authentication
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

# Kerberos Authentication for browser monitors [synthetics-kerberos]

Kerberos Auhtentication enables monitoring on Single Sign-On (SSO) protected sites, usually behind Microsoft Active Directory.

:::{admonition} Requirements
* Kerberos Authentication works for **Private Locations only**. It will not work from Elastic's managed global locations.
* Credentials must be made available to the agent process beforehand. A keytab for the service account plus a `kinit`'d ticket cache (`KRB5CCNAME`). Keep it fresh with a cron job or `systemd` timer (e.g. `kinit -R` every few hours, `kinit -kt` on failure).
* `/etc/krb5.conf` must be configured for your realm.
* The SPN (e.g. `HTTP/intranet.corp.local@CORP.LOCAL`) must be registered against the service account that fronts the protected URL.
:::
:::: 

## Configuring Kerberos authentication [configuring_kerberos]

Browser monitors already have first-class support for SSO Kerberos authentication, simply specify the protected domains under `playwrightOptions.args`:

```ts
playwrightOptions: {
  args: [
    '--auth-server-allowlist=*.corp.local,corp.local',
    '--auth-negotiate-delegate-allowlist=*.corp.local',
  ],
}
```

The hostname must match an entry in `--auth-server-allowlist`. The matcher is hostname-only and supports shell-style wildcards — `*.corp.local` will NOT match the bare `corp.local`.