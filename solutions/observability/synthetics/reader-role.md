---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-role-read.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Reader role [synthetics-role-read]

For users who need to view and create visualizations that access Synthetics data, provide read access. You can grant two types of read access:

* **General read access**: For most users, you can use [General read access](#synthetics-read-privileges-general), which grants read access to all {{kib}} apps and requires little configuration.
* **Limited read access**: If you want to limit read access to the {{synthetics-app}} only, you can use [Limited read access](#synthetics-read-privileges-limited), which requires additional configuration.

## General read access [synthetics-read-privileges-general]

For users who only need to view results in {{kib}}, use the `viewer` [built-in role](elasticsearch://reference/elasticsearch/roles.md).

## Limited read access [synthetics-read-privileges-limited]

If you want to limit read access to the {{synthetics-app}} only, do *not* use the `viewer` [built-in role](elasticsearch://reference/elasticsearch/roles.md).

Instead, you can create a reader role, called something like `synthetics_reader_limited`, and grant the following privileges:

| Type | Privilege | Purpose |
| --- | --- | --- |
| [Index](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) | `synthetics-*`: `read` | Read-only access to synthetics indices. |
| [Index](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) | `.alerts-observability.uptime.alerts-*`: `read` | Read-only access to synthetics alert indices. |
| [Observability {{kib}} privileges](/solutions/observability/get-started/observability-kibana-privileges.md) | `Synthetics and Uptime`: `read` | Access to the {{synthetics-app}} in {{kib}}. |

### Allow running tests and managing alert rules [synthetics-read-sub-feature-privileges]
```{applies_to}
stack: ga 9.4+
serverless: ga
```

On its own, the `Synthetics and Uptime`: `read` privilege doesn't allow users to run tests or change alert rules. To grant either capability without allowing users to create, edit, or delete monitors:

1. Expand **Synthetics and Uptime** in the list of [Observability {{kib}} privileges](/solutions/observability/get-started/observability-kibana-privileges.md#synthetics-and-uptime-sub-feature-privileges).
2. Turn on **Customize sub-feature privileges**.
3. Select the privileges to add to the role:

    * **Can run tests manually**: trigger an on-demand run of an existing monitor using the **Run test manually** action. Grant this to operators who need to launch an ad-hoc test but must not manage monitors.
    * **Can manage rules**: create, update, delete, enable, disable, and run Synthetics and Uptime alert rules, including the default status and TLS rules. Grant this when the people responsible for alerting aren't the people who configure monitors, for example a site reliability engineer who tunes rules. Monitors, settings, global parameters, and private locations stay read-only.

Both privileges are opt-in, so you grant them separately even when **Synthetics and Uptime** is set to **All**. For the complete list of privileges in this group, refer to [Synthetics and Uptime sub-feature privileges](/solutions/observability/get-started/observability-kibana-privileges.md#synthetics-and-uptime-sub-feature-privileges).

You can't customize built-in roles. To add either privilege for a user who has [general read access](#synthetics-read-privileges-general) through the `viewer` role, assign that user an additional role that grants `Synthetics and Uptime`: `read` with the sub-feature privilege turned on.
