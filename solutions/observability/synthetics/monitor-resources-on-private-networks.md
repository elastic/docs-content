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

{{private-location}}s via Elastic Agent require only outbound connections from your network, while allowing Elastic’s global managed infrastructure to access a private endpoint requires inbound access, thus posing an additional risk that users must assess.

## Allow access to your private network [monitor-via-access-control]

To give Elastic’s global managed infrastructure access to a private endpoint, use IP address filtering, HTTP authentication, or both.

To grant access via IP, use [this list of egress IPs](https://manifest.synthetics.elastic-cloud.com/v1/ip-ranges.json). The addresses and locations on this list may change, so automating updates to filtering rules is recommended. IP filtering alone will allow all users of Elastic’s global managed infrastructure access to your endpoints, if this is a concern consider adding additional protection via user/password authentication via a proxy like nginx.

## Monitor via a private agent [monitor-via-private-agent]

{{private-location}}s allow you to run monitors from your own premises. Before running a monitor on a {{private-location}}, you’ll need to:

* [Set up {{fleet-server}} and {{agent}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-fleet-agent).
* [Connect {{fleet}} to the {{stack}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-connect) and enroll an {{agent}} in {{fleet}}.
* [Add a {{private-location}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-add) in the Synthetics UI.

::::{important}
{{private-location}}s running through {{agent}} must have a direct connection to {{es}}. Do not configure any ingest pipelines, or output via Logstash as this will prevent Synthetics from working properly and is not [supported](/solutions/observability/synthetics/support-matrix.md).

::::

## Set up {{fleet-server}} and {{agent}} [synthetics-private-location-fleet-agent]

Start by setting up {{fleet-server}} and {{agent}}:

* **Set up {{fleet-server}}**: If you are using {{ecloud}}, {{fleet-server}} will already be provided and you can skip this step. To learn more, refer to [Set up {{fleet-server}}](/reference/fleet/fleet-server.md).
* **Create an agent policy**: For more information on agent policies and creating them, refer to [{{agent}} policy](/reference/fleet/agent-policy.md#create-a-policy).

::::{important}
A {{private-location}} should be set up against an agent policy that runs on a single {{agent}}. The {{agent}} must be **enrolled in Fleet** ({{private-location}}s cannot be set up using **standalone** {{agents}}). Do *not* run the same agent policy on multiple agents being used for {{private-location}}s, as you may end up with duplicate or missing tests. {{private-location}}s do not currently load balance tests across multiple {{agents}}. See [Scaling {{private-location}}s](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-scaling) for information on increasing the capacity within a {{private-location}}.

By default {{private-location}}s are configured to allow two simultaneous browser tests and an unlimited number of lightweight checks. As a result, if more than two browser tests are assigned to a particular {{private-location}}, there may be a delay to run them.

::::

## Connect to the {{stack}} or your Observability Serverless project [synthetics-private-location-connect]

After setting up {{fleet}}, you’ll connect {{fleet}} to the {{stack}} or your Observability Serverless project and enroll an {{agent}} in {{fleet}}.

Elastic provides Docker images that you can use to run {{fleet}} and an {{agent}} more easily, additional installation methods can be found on the [{{agent}} installation guide](/reference/fleet/install-elastic-agents.md). 
::::{important}
For running browser monitors on {{private-location}}s, you *must* use one of the `elastic-agent-complete` Docker image variants in a containerized environment, as it includes the required dependencies. The standard {{agent}} variant only supports TCP, ICMP and HTTP monitors.

::::

To pull the Docker image run:

::::{tab-set}
:group: docker
:::{tab-item} `elastic-agent-complete`
:sync: specific

```sh subs=true
# Supports all monitor types: TCP, ICMP, HTTP and Browser
docker pull docker.elastic.co/elastic-agent/elastic-agent-complete:{{version.stack}}
```

:::

:::{tab-item} `elastic-agent`
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
:::{tab-item} `elastic-agent-complete`
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

::::{important}
The `elastic-agent-complete` container, when running as Synthetics Private Locations, requires additional capabilities to operate correctly. Ensure `NET_RAW` and `SETUID` are enabled on the container.

::::

:::

:::{tab-item} `elastic-agent`
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

::::{important}
The `elastic-agent` container, when running as Synthetics Private Locations, requires additional capabilities to operate correctly. Ensure `NET_RAW` and `SETUID` are enabled on the container.

::::

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
1. (Optional) In _Tags_ select [tags](/explore-analyze/find-and-organize/tags.md) to assign to this location.
1. (Optional) In _Spaces_ specify the [spaces](/deploy-manage/manage-spaces.md) where this location will be available.
1. Click **Save**.

::::{important}
It is not currently possible to use custom CAs for synthetics browser tests in private locations without following a workaround. To learn more about the workaround, refer to the following GitHub issue: [elastic/synthetics#717](https://github.com/elastic/synthetics/issues/717).
::::

## Scaling {{private-location}}s [synthetics-private-location-scaling]

By default {{private-location}}s are configured to allow two simultaneous browser tests, and an unlimited number of lightweight checks. These limits can be set via the environment variables `SYNTHETICS_LIMIT_{{TYPE}}`, where `{{TYPE}}` is one of `BROWSER`, `HTTP`, `TCP`, and `ICMP` for the container running the {{agent}} docker image.

### CPU and RAM requirements

It is critical to allocate enough memory and CPU capacity to handle configured limits. Resource requirements will vary depending on simultaneous workload and monitor complexity:

**For browser monitors**: Start by allocating at least 2 GiB of memory and two cores _per browser instance_ to ensure consistent performance and avoid out-of-memory errors. Then adjust as needed.
**For tcp, http, icmp**: Much less memory is needed, start by allocating at least 512MiB of memory and two cores _globally_. While this will be enough to run a large number of lightweight monitors, it is recommended to track the resource usage and adjust accordingly.

Example: For a private location expected to run 2 concurrent browser monitors and 100 HTTP checks, the recommended allocation is 2 * (2 GiB + 2 vCPU) + (512 MiB + 2 vCPU) => 4,5 GiB + 6 vCPU.

### Known limitations on vertical scaling

- A single private location will not scale beyond 10,000 monitors. Exceeding this number will result in agent degradation and inconsistent execution, regardless of the resources allocated.
- Complex monitor configuration can disproportionately increase the private location policy size, leading to agent communication errors and degradation even if the limit mentioned above hasn't been reached.

If you're facing one of these scenarios, it is likely that the private location has grown too large and needs to be split into smaller locations, each alloted a portion of the original location monitors.

## Next steps [synthetics-private-location-next]

Now you can add monitors to your {{private-location}} in [the Synthetics UI](/solutions/observability/synthetics/create-monitors-ui.md) or using the [Elastic Synthetics library’s `push` method](/solutions/observability/synthetics/create-monitors-with-projects.md).