---
navigation_title: "Synthetics"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-troubleshooting.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-troubleshooting.html
---

# Troubleshoot Synthetics [synthetics-troubleshooting]



## Local debugging [synthetics-troubleshooting-local-debugging]

For debugging synthetic tests locally, you can set an environment variable, `DEBUG=synthetics`, to capture Synthetics agent logs when using the [Synthetics CLI](/solutions/observability/apps/use-synthetics-cli.md).


## Common issues [synthetics-troubleshooting-common-issues]


### Monitors stopped running after upgrading to 8.8.0 or above [synthetics-troubleshooting-missing-api-key]
```yaml {applies_to}
stack: all
```

Synthetic monitors will stop running if you have gone through this workflow:

1. Enabled Monitor Management (in the {{uptime-app}}) prior to 8.6.0.
2. Created a synthetic monitor that is configured to run on Elastic’s global managed infrastructure.
3. Upgraded to 8.8.0 or above.

This happens because the permissions granted by clicking **Enable Monitor Management** in versions prior to 8.6.0 are not sufficient in versions 8.8.0 and above.

To fix this, a user with [admin permissions](/solutions/observability/apps/setup-role.md) needs to visit the {{synthetics-app}} in {{kib}}. In 8.8.0 and above, the equivalent of "enabling monitor management" happens automatically in the background when a user with [admin permissions](/solutions/observability/apps/setup-role.md) visits the {{synthetics-app}}.

If a user *without* [admin permissions](/solutions/observability/apps/setup-role.md) visits the {{synthetics-app}} before an admin has visited it, the user will see a note that says "Only administrators can enable this feature". That note will persist until an admin user visits the {{synthetics-app}}.


### No results from a monitor configured to run on a {{private-location}} [synthetics-troubleshooting-no-agent-running]

If you have created a {{private-location}} and configured a monitor to run on that {{private-location}}, but don’t see any results for that monitor in the {{synthetics-app}}, make sure there is an agent configured to run against the agent policy.

::::{note}
If you attempt to assign an agent policy to a {{private-location}} *before* configuring an agent to run against the agent policy, you will see a note in the {{synthetics-app}} UI that the selected agent policy has no agents.

::::


When creating a {{private-location}}, you have to:

::::{tab-set}

:::{tab-item} {{serverless-short}}
1. [Set up {{agent}}](/solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-fleet-agent).
2. [Connect {{fleet}} to your Observability project](/solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-connect) and enroll an {{agent}} in {{fleet}}.
3. [Add a {{private-location}}](/solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-add) in the Synthetics UI.
:::

:::{tab-item} {{stack}}
1. [Set up {{fleet-server}} and {{agent}}](/solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-fleet-agent).
2. [Connect {{fleet}} to the {{stack}}](/solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-connect) and enroll an {{agent}} in {{fleet}}.
3. [Add a {{private-location}}](/solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-add) in the {{synthetics-app}}.
:::

::::

If you do not complete the second item, no agents will be configured to run against the agent policy, and any monitors configured to run on that {{private-location}} won’t be able to run so there will be no results in the {{synthetics-app}}.

To fix this, make sure there is an agent configured to run against the agent policy.


### No results from a monitor [synthetics-troubleshooting-no-direct-es-connection]

If you have configured a monitor but don’t see any results for that monitor in the {{synthetics-app}}, whether running them from Elastic’s global managed testing infrastructure or from {{private-location}}s, ensure Synthetics has a direct connection to {{es}}.

Do not configure any ingest pipelines or output via Logstash as this will prevent Synthetics from working properly and is not [supported](/solutions/observability/apps/synthetics-support-matrix.md).


### Browser monitor configured to run on a {{private-location}} not running to schedule [synthetics-troubleshooting-missing-browser-schedules]

If you have browser monitors configured to run on a {{private-location}} but notice one or more of them are not running as scheduled, this could be because:

* The time it takes for your monitor to run is longer than the frequency you have set
* There may be too many monitors trying to run concurrently, causing some of them to skip their scheduled run

You may also see a message in the logs such as `2 tasks have missed their schedule deadlines by more than 1 second in the last 15s`. These will be visible from inside the Agent diagnostic ZIP file, and the numbers and time periods may be different in your logs.

Start by identifying the cause of the issue. First, check if the time it takes the monitor to run is less than the scheduled frequency:

1. Go to the {{synthetics-app}}.
2. Click the monitor, then click **Go to monitor**.
3. Go to the [Overview tab](/solutions/observability/apps/analyze-data-from-synthetic-monitors.md#synthetics-analyze-individual-monitors-overview) to see the *Avg. duration*. You can also view the duration for individual runs in the [History tab](/solutions/observability/apps/analyze-data-from-synthetic-monitors.md#synthetics-analyze-individual-monitors-history).
4. Compare the duration to the scheduled frequency. If the duration is *greater than* the scheduled frequency, for example if the monitor that takes 90 seconds to run and its scheduled frequency is 1 minute, the next scheduled run will not occur because the current one is still running so you may see results for every other scheduled run.

    To fix this, you can either:

    * Change the frequency so the monitor runs less often.
    * Refactor the monitor so it can run in a shorter amount of time.


If the duration is *less than* the scheduled frequency or the suggestion above does not fix the issue, then there may be too many browser monitors attempting to run on the {{private-location}}. Due to the additional hardware overhead of running browser monitors, we limit each {{private-location}} to only run two browser monitors at the same time. Depending on how many browser monitors you have configured to run on the {{private-location}} and their schedule, the {{private-location}} may not be able to run them all because it would require more than two browser tests to be running simultaneously.

To fix this issue, you can either:

* Increase the number of concurrent browser monitors allowed (as described in [Scaling Private Locations](/solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-scaling)), paying attention to the scaling and hardware requirements documented.
* Create multiple {{private-location}}s and spread your browser monitors across them more evenly (effectively horizontally scaling your {{private-location}}s).


### No locations are available [synthetics-troubleshooting-no-locations]

When using {{ecloud}}, if there are no options available in the *Locations* dropdown when you try to create a monitor in the {{synthetics-app}} *or* if no locations are listed when using the [`location` command](/solutions/observability/apps/use-synthetics-cli.md#elastic-synthetics-locations-command), it might be because you do not have permission to use Elastic managed locations *and* there are no [Private Locations](/solutions/observability/apps/monitor-resources-on-private-networks.md#monitor-via-private-agent) available yet.

There are a few ways to fix this:

::::{tab-set}

:::{tab-item} {{serverless-short}}
* If you have [Editor](/solutions/observability/apps/grant-users-access-to-secured-resources.md) access, you can [create a new Private Location](/solutions/observability/apps/monitor-resources-on-private-networks.md#monitor-via-private-agent). Then try creating the monitor again.
* If you do *not* have the right privileges to create a Private Location, you can ask an [Admin](/solutions/observability/apps/grant-users-access-to-secured-resources.md) to create a Private Location or give you the necessary privileges so you can [create a new Private Location](/solutions/observability/apps/monitor-resources-on-private-networks.md#monitor-via-private-agent). Then try creating the monitor again.

:::

:::{tab-item} {{stack}}
* If you have [write access](/solutions/observability/apps/writer-role.md) including the privileges for [creating new Private Locations](/solutions/observability/apps/writer-role.md#synthetics-role-write-private-locations), you can [create a new Private Location](/solutions/observability/apps/monitor-resources-on-private-networks.md#monitor-via-private-agent). Then try creating the monitor again.
* If you do *not* have the right privileges to create a Private Location, you can ask someone with the [necessary privileges](/solutions/observability/apps/writer-role.md#synthetics-role-write-private-locations) to create a Private Location or ask an administrator with a [setup role](/solutions/observability/apps/setup-role.md) to give you the necessary privileges and [create a new Private Location](/solutions/observability/apps/monitor-resources-on-private-networks.md#monitor-via-private-agent). Then try creating the monitor again.
* If you want to create a monitor to run on Elastic’s global managed infrastructure, ask an administrator with a [setup role](/solutions/observability/apps/setup-role.md) to update [`Synthetics and Uptime` sub-feature privileges](/solutions/observability/apps/writer-role.md#disable-managed-locations) for the role you’re currently assigned. Then try creating the monitor again.
:::

::::

### You do not have permission to use Elastic managed locations [synthetics-troubleshooting-public-locations-disabled]
```yaml {applies_to}
stack: all
```

If you try to create or edit a monitor hosted on Elastic’s global managed infrastructure but see a note that you do not have permission to use Elastic managed locations, an administrator has restricted the use of public locations.

To fix this you can either:

* Ask an administrator with a [setup role](/solutions/observability/apps/setup-role.md) to update [`Synthetics and Uptime` sub-feature privileges](/solutions/observability/apps/writer-role.md#disable-managed-locations) for the role you’re currently assigned or assign you a role that allows using Elastic’s global managed infrastructure.
* Use a [Private Location](/solutions/observability/apps/monitor-resources-on-private-networks.md#monitor-via-private-agent).


## Get help [synthetics-troubleshooting-get-help]


### Elastic Support [synthetics-troubleshooting-support]

We offer a support experience unlike any other. Our team of professionals *speak human and code* and love making your day. [Learn more about subscriptions](https://www.elastic.co/subscriptions).


### Discussion forum [synthetics-troubleshooting-discussion]

For other questions and feature requests, visit our [discussion forum](https://discuss.elastic.co//c/observability/synthetics/75).
