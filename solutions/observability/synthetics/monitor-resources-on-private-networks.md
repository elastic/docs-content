---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-private-location.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-private-location.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Monitor resources on private networks [synthetics-private-location]

To monitor resources on private networks you can either:

* Allow Elastic’s global managed infrastructure to access your private endpoints.
* Use {{agent}} to create a {{private-location}}.

{{private-location}}s using {{agent}} require only outbound connections from your network, while allowing Elastic’s global managed infrastructure to access a private endpoint requires inbound access, therefore posing an additional risk that you must consider.

## Allow access to your private network [monitor-via-access-control]

To give Elastic’s global managed infrastructure access to a private endpoint, use IP address filtering, HTTP authentication, or both.

To grant access using IP, use [this list of egress IPs](https://manifest.synthetics.elastic-cloud.com/v1/ip-ranges.json). The addresses and locations on this list might change, so automating updates to filtering rules is recommended. IP filtering alone will allow all users of Elastic’s global managed infrastructure access to your endpoints. If this is a concern, consider adding additional protection through user/password authentication with a proxy like nginx.

## Monitor using a private agent [monitor-via-private-agent]

{{private-location}}s allow you to run monitors from your own premises. Before running a monitor on a {{private-location}}, you’ll need to:

* [Set up {{fleet-server}} and {{agent}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-fleet-agent).
* [Connect {{fleet}} to the {{stack}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-connect) and enroll an {{agent}} in {{fleet}}.
* [Add a {{private-location}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-add) in the Synthetics UI.

A {{private-location}} is classic or scalable depending on how many {{agents}} share its agent policy:

* **Classic**: The agent policy runs on a single {{agent}}, and that agent runs every monitor assigned to the location.
* {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` **Scalable**: With an [Enterprise subscription]({{subscriptions}}) or an active trial, enroll multiple {{agents}} on the same agent policy. {{kib}} automatically distributes each monitor to exactly one agent, with failover when an agent becomes unhealthy. You don't need to turn on anything extra when you add the {{private-location}}. Refer to [Scale a {{private-location}} across multiple {{agents}}](#synthetics-private-location-scalable) for more information.

::::{important}
{{private-location}}s running through {{agent}} must have a direct connection to {{es}}. Do not configure any ingest pipelines, or output using Logstash as this will prevent Synthetics from working properly and [is not supported](/solutions/observability/synthetics/support-matrix.md).

::::

## Set up {{fleet-server}} and {{agent}} [synthetics-private-location-fleet-agent]

Start by setting up {{fleet-server}} and {{agent}}:

* **Set up {{fleet-server}}**: If you are using {{ecloud}}, {{fleet-server}} will already be provided and you can skip this step. To learn more, refer to [Set up {{fleet-server}}](/reference/fleet/fleet-server.md).
* **Create an agent policy**: For more information on agent policies and creating them, refer to [{{agent}} policy](/reference/fleet/agent-policy.md#create-a-policy).

::::{important}
The {{agent}} must be enrolled in {{fleet}}. {{private-location}}s cannot be set up using standalone {{agents}}.
::::

When you create the agent policy:

* Decide how many {{agents}} run the policy:
    * Run a classic {{private-location}} on a single {{agent}}. Classic {{private-location}}s do not distribute tests across {{agents}}, so running the same policy on more than one {{agent}} can produce duplicate or missing tests. To add capacity on one {{agent}}, refer to [Scaling {{private-location}}s](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-scaling).
    * {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` To run tests on multiple {{agents}} that share one agent policy, use a [scalable {{private-location}}](#synthetics-private-location-scalable).
* {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Create the agent policy in the same {{kib}} space as the {{private-location}}. Cross-space agent policies are not supported. To run monitors in more than one space, create a separate agent policy in each space.

## Connect to the {{stack}} or your Observability Serverless project [synthetics-private-location-connect]

After setting up {{fleet}}, you’ll connect {{fleet}} to the {{stack}} or your Observability Serverless project and enroll an {{agent}} in {{fleet}}.

Elastic provides Docker images that you can use to run {{fleet}} and an {{agent}} more easily. Additional installation methods can be found on the [{{agent}} installation guide](/reference/fleet/install-elastic-agents.md). 
::::{important}
For running browser monitors on {{private-location}}s, you *must* use one of the `elastic-agent-complete` Docker image variants in a containerized environment. The standard {{agent}} variant only supports TCP, ICMP, and HTTP monitors.

::::

To pull the Docker image run:

::::{tab-set}
:group: docker
:::{tab-item} elastic-agent-complete
:sync: specific

```sh subs=true
# Supports all monitor types: TCP, ICMP, HTTP and Browser
docker pull docker.elastic.co/elastic-agent/elastic-agent-complete:{{version.stack}}
```

:::

:::{tab-item} elastic-agent
:sync: latest

```shell subs=true
# Supports TCP, ICMP and HTTP monitors
docker pull docker.elastic.co/elastic-agent/elastic-agent:{{version.stack}}
```

:::

::::

You can download and install a specific version of the {{stack}} by replacing `{{version.stack}}` with the version number you want. For example, you can replace `{{version.stack}}` with {{version.stack.base}}.

Then enroll and run an {{agent}}. You’ll need an enrollment token and the URL of the {{fleet-server}}. You can use the default enrollment token for your policy or create new policies and [enrollment tokens](/reference/fleet/fleet-enrollment-tokens.md) as needed.

For more information on running {{agent}} with Docker, refer to [Run {{agent}} in a container](/reference/fleet/elastic-agent-container.md).

::::{tab-set}
:group: docker
:::{tab-item} elastic-agent-complete
:sync: specific

```shell subs=true
docker run \
  --env FLEET_ENROLL=1 \
  --env FLEET_URL={fleet_server_host_url} \
  --env FLEET_ENROLLMENT_TOKEN={enrollment_token} \
  --cap-add=NET_RAW \
  --cap-add=SETUID \
  --rm docker.elastic.co/elastic-agent/elastic-agent-complete:{{version.stack}}
```

The `elastic-agent-complete` container, when running as Synthetics Private Locations, requires additional capabilities to operate correctly. Ensure `NET_RAW` and `SETUID` are enabled on the container.

:::

:::{tab-item} elastic-agent
:sync: latest

```shell subs=true
docker run \
  --env FLEET_ENROLL=1 \
  --env FLEET_URL={fleet_server_host_url} \
  --env FLEET_ENROLLMENT_TOKEN={enrollment_token} \
  --cap-add=NET_RAW \
  --cap-add=SETUID \
  --rm docker.elastic.co/elastic-agent/elastic-agent:{{version.stack}}
```

The `elastic-agent` container, when running as Synthetics Private Locations, requires additional capabilities to operate correctly. Ensure `NET_RAW` and `SETUID` are enabled on the container.

:::

::::

::::{note}
You may need to set other environment variables. Learn how in [{{agent}} environment variables guide](/reference/fleet/agent-environment-variables.md).

::::

## Add a {{private-location}} [synthetics-private-location-add]

When the {{agent}} is running you can add a new {{private-location}} in the UI:

1. Find `Synthetics` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Go to **Settings**.
1. Go to the **{{private-location}}s** tab.
1. Click **Create location**.
1. Give your new location a unique _Location name_.
1. Select the _Agent policy_ you created above. 
    
    {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Only agent policies that exist in the **current space** are available for selection.
1. (Optional) In _Tags_ select [tags](/explore-analyze/find-and-organize/tags.md) to assign to this location.
1. (Optional) In _Spaces_ specify the [spaces](/deploy-manage/manage-spaces.md) where this location will be available.
1. Click **Save**.

::::{note}
:applies_to: stack: ga 9.4+
If you upgraded from a version that allowed cross-space agent policy selection, any private location that references an agent policy from a different space will show **Policy not found in the current space** in the UI. To resolve this, reassign the private location to an agent policy in the same space, or create a new agent policy in the current space and re-enroll the {{agent}}.
::::

Using custom CAs for synthetics browser tests in private locations is not currently possible without a workaround. To learn more, refer to the GitHub issue [elastic/synthetics#717](https://github.com/elastic/synthetics/issues/717).

## Monitor integration health [synthetics-private-location-health]

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga`

Synthetics automatically detects when private location monitors have broken {{fleet}} integrations and surfaces health status in the UI with actionable recovery options. This can happen if an agent policy or {{fleet}} package policy is deleted after a monitor is configured, or if the referenced private location no longer exists.

### Failure types [synthetics-private-location-health-failure-types]

Each monitor is evaluated per location. The following failure types can occur, listed in priority order — only the first matching issue per location is reported, since it is the root cause:

| Status | Cause | Recovery |
|--------|-------|----------|
| `missing_location` | The monitor references a private location that no longer exists. | Manual |
| `missing_agent_policy` | The agent policy associated with the private location was deleted. | Manual |
| `missing_package_policy` | The {{fleet}} package policy for this monitor/location pair is missing. | Automatic (Reset) |

### Health status in the UI [synthetics-private-location-health-ui]

Health status surfaces in three places:

- **Monitor list**: An orange warning icon appears next to unhealthy monitors. Hover over the icon to see per-location details on why the monitor is affected.
- **Monitor details page**: A warning callout lists the affected locations. A **Reset monitor** button is shown when the failure type is `missing_package_policy`, which recreates the missing Fleet resources.
- **Private Locations settings**: Each location shows a badge with the count of unhealthy monitors. Clicking the badge opens a popover listing the affected monitors and a **Reset monitors** button that bulk-resets all recoverable monitors at that location.

### Reset behavior [synthetics-private-location-health-reset]

Only monitors with a `missing_package_policy` status can be auto-reset. The **Reset** action recreates the missing Fleet package policy, restoring the monitor to a healthy state.

Monitors with `missing_agent_policy` or `missing_location` statuses are excluded from auto-reset because the underlying infrastructure must be restored before Fleet resources can be recreated. When you initiate a reset, the confirmation dialog lists which monitors will be reset and which will be skipped and why.

To resolve failures that require manual intervention:

- **`missing_agent_policy`**: Recreate the agent policy and re-enroll an {{agent}}, then update the affected private location under **Settings > {{private-location}}s** to reference the new agent policy.
- **`missing_location`**: [Re-create the private location](#synthetics-private-location-add) or edit the affected monitors to remove or replace the deleted location.

## Scale a {{private-location}} across multiple {{agents}} [synthetics-private-location-scalable]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

A scalable {{private-location}} runs its monitors on a pool of {{agents}} that share one agent policy. Each monitor runs on one agent in the pool. When an agent becomes unhealthy, its monitors move to the healthy agents. When you add an agent, some monitors move to it.

Enroll a second {{agent}} on the same agent policy when one {{agent}} can't run all the monitors in the location, or when monitors must keep running if an agent fails. Keep a single {{agent}} (a classic {{private-location}}) when it has enough capacity and you don't need failover.

### Requirements [synthetics-private-location-scalable-requirements]

* An [Enterprise subscription]({{subscriptions}}) or an active trial. Without one, multiple {{agents}} on the same agent policy each run every monitor in the location, producing duplicate results. If your subscription level drops below Enterprise, Synthetics clears the agent assignments on its next rebalancing pass and the same duplicate behavior returns until you upgrade again. To avoid duplicate results in the meantime, [remove all but one agent](#synthetics-private-location-scalable-disable).
* {{agents}} enrolled in {{fleet}} on the same agent policy. Failover requires at least two agents. The agent policy must be in the same {{kib}} space as the {{private-location}}.
* For browser monitors, every agent in the pool must use an `elastic-agent-complete` Docker image. Refer to [Connect to the {{stack}}](#synthetics-private-location-connect) for more information.
* Because a monitor can move to any agent in the pool, configure every agent the same way, including network access to monitored hosts, environment variables that your monitors read, and the host timezone.
* Each agent needs the CPU and RAM described in [Scaling {{private-location}}s](#synthetics-private-location-scaling). Browser and lightweight concurrency limits apply to each agent separately.

Optionally, if you want to view memory and CPU usage for each agent in the Synthetics UI, add the System integration to the agent policy.

### Set up a scalable {{private-location}} [synthetics-private-location-scalable-setup]

To set up a scalable {{private-location}}:

1. [Create an agent policy](#synthetics-private-location-fleet-agent) in the same {{kib}} space as the {{private-location}}.
1. [Enroll two or more {{agents}}](#synthetics-private-location-connect) on that agent policy.
1. [Add a {{private-location}}](#synthetics-private-location-add) that uses the agent policy. With an Enterprise subscription or an active trial, {{kib}} automatically distributes monitors across all enrolled agents.

On the **{{private-location}}s** tab, a scalable location shows a **Scalable** badge with the number of enrolled agents. Expand the location's row to view the monitors, health, and resource usage of each agent. Refer to [{{private-location}}s settings](/solutions/observability/synthetics/configure-settings.md#synthetics-settings-private-locations) for more information.

To add agents to an existing location, enroll additional {{agents}} on its agent policy. {{kib}} automatically redistributes monitors to include the new agents.

### Remove agents [synthetics-private-location-scalable-disable]

To reduce a scalable location to a single agent, unenroll all but one {{agent}} from its agent policy. {{kib}} reassigns the remaining monitors to the surviving agent when the removed agents are detected as unhealthy. With one agent left, the location becomes a classic {{private-location}}: the remaining agent runs every monitor assigned to the location.

You can't move an agent's monitors to other agents before you unenroll it. When you unenroll an agent, its monitors move only after it's detected as unhealthy, and they might miss some scheduled runs in the meantime.

### How monitors are assigned to agents [synthetics-private-location-scalable-assignment]

Synthetics assigns each monitor to one agent in the pool. The assignment balances the estimated memory cost of the monitors across agents: a browser monitor counts roughly as much as 50 lightweight monitors, and agents with more total RAM receive a larger share. Because assignment is weighted by memory cost rather than monitor count, the number of monitors per agent can look uneven even when memory is balanced. Current CPU and memory usage appear in the Synthetics UI but aren't used for assignments.

About once a minute, Synthetics checks the health of every agent in the pool and adjusts assignments:

* **Failover**: When an agent stops checking in to {{fleet}} and stops sending results, Synthetics marks it as unhealthy after about 90 seconds and moves its monitors to healthy agents, usually within 2–3 minutes of the last check-in. During that move, a monitor can briefly run on two agents, which produces duplicate results.
* **Recovery and new agents**: After a recovered or newly enrolled agent has been healthy for 3 minutes, Synthetics moves only as many monitors to it as needed to balance the pool.
* **No healthy agents**: If no agent in the pool is healthy, monitors keep their assignments and don't run until an agent recovers.

To stop these adjustments for every scalable {{private-location}}, turn off **Rebalance private location shards** in [**Settings → Advanced**](/solutions/observability/synthetics/configure-settings.md#synthetics-settings-advanced-rebalancing).

::::{warning}
Turning off **Rebalance private location shards** removes the agent assignment from every monitor in every scalable {{private-location}}. Each monitor then runs on every agent enrolled on its location's agent policy, which duplicates test runs. When you turn the switch back on, Synthetics reassigns the monitors right away.
::::

## Scaling {{private-location}}s [synthetics-private-location-scaling]

By default, each {{agent}} in a {{private-location}} allows two simultaneous browser tests and an unlimited number of lightweight checks. If more than two browser tests are scheduled to run at the same time on one agent, some of them are delayed. You can change these limits using the environment variables `SYNTHETICS_LIMIT_{{TYPE}}`, where `{{TYPE}}` is one of `BROWSER`, `HTTP`, `TCP`, and `ICMP`, for the container running the {{agent}} Docker image.

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` In a scalable {{private-location}}, these limits and the CPU and RAM requirements apply to each agent. To add capacity by adding agents instead of resources, refer to [Scale a {{private-location}} across multiple {{agents}}](#synthetics-private-location-scalable).

### CPU and RAM requirements

It is critical to allocate enough memory and CPU capacity to handle configured limits. Resource requirements will vary depending on simultaneous workload and monitor complexity:

**For browser monitors**: Start by allocating at least 2 GiB of memory and two cores _per browser instance_ to ensure consistent performance and avoid out-of-memory errors. Then adjust as needed.
**For tcp, http, icmp**: Much less memory is needed, start by allocating at least 512MiB of memory and two cores _globally_. While this will be enough to run many lightweight monitors, it is recommended to track the resource usage and adjust accordingly.

Example: For a private location expected to run 2 concurrent browser monitors and 100 HTTP checks, the recommended allocation is 2 * (2 GiB + 2 vCPU) + (512 MiB + 2 vCPU) => 4,5 GiB + 6 vCPU.

### Known limitations on vertical scaling

- A single private location will not scale beyond 10,000 monitors. Exceeding this number will result in agent degradation and inconsistent execution, regardless of the resources allocated. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` In a scalable {{private-location}}, this limit applies per location, not per agent — adding more agents does not raise it.

- Many Synthetics monitors, or monitors with complex configurations, can cause the check-in payload to exceed the default 1 MiB `checkin_limit.max_body_byte_size` limit on {{fleet-server}}. When this happens, check-ins are rejected and agents appear offline or unhealthy in the Fleet UI even though monitors are executing successfully. To resolve this, increase the `server.limits.checkin_limit.max_body_byte_size` setting on your self-managed Fleet Server. Refer to [Advanced {{fleet-server}} options](/reference/fleet/fleet-server-scalability.md#fleet-server-configuration) for configuration details and an example.

If you're facing one of these scenarios, it is likely that the private location has grown too large and needs to be split into smaller locations, each allotted a portion of the original location monitors.

## Next steps [synthetics-private-location-next]

Now you can add monitors to your {{private-location}} in [the Synthetics UI](/solutions/observability/synthetics/create-monitors-ui.md) or using the [Elastic Synthetics library’s `push` method](/solutions/observability/synthetics/create-monitors-with-projects.md).