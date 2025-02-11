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

* [Set up {{fleet-server}} and {{agent}}](../../../solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-fleet-agent).
* [Connect {{fleet}} to the {{stack}}](../../../solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-connect) and enroll an {{agent}} in {{fleet}}.
* [Add a {{private-location}}](../../../solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-add) in the {{synthetics-app}}.

::::{important}
{{private-location}}s running through {{agent}} must have a direct connection to {{es}}. Do not configure any ingest pipelines, or output via Logstash as this will prevent Synthetics from working properly and is not [supported](../../../solutions/observability/apps/synthetics-support-matrix.md).

::::



## Set up {{fleet-server}} and {{agent}} [synthetics-private-location-fleet-agent]

Start by setting up {{fleet-server}} and {{agent}}:

* **Set up {{fleet-server}}**: If you are using {{ecloud}}, {{fleet-server}} will already be provided and you can skip this step. To learn more, refer to [Set up {{fleet-server}}](https://www.elastic.co/guide/en/fleet/current/fleet-server.html).
* **Create an agent policy**: For more information on agent policies and creating them, refer to [{{agent}} policy](https://www.elastic.co/guide/en/fleet/current/agent-policy.html#create-a-policy).

::::{important}
A {{private-location}} should be set up against an agent policy that runs on a single {{agent}}. The {{agent}} must be **enrolled in Fleet** ({{private-location}}s cannot be set up using **standalone** {{agents}}). Do *not* run the same agent policy on multiple agents being used for {{private-location}}s, as you may end up with duplicate or missing tests. {{private-location}}s do not currently load balance tests across multiple {{agents}}. See [Scaling {{private-location}}s](../../../solutions/observability/apps/monitor-resources-on-private-networks.md#synthetics-private-location-scaling) for information on increasing the capacity within a {{private-location}}.

By default {{private-location}}s are configured to allow two simultaneous browser tests and an unlimited number of lightweight checks. As a result, if more than two browser tests are assigned to a particular {{private-location}}, there may be a delay to run them.

::::



## Connect to the {{stack}} [synthetics-private-location-connect]

After setting up {{fleet}}, you’ll connect {{fleet}} to the {{stack}} and enroll an {{agent}} in {{fleet}}.

$$$synthetics-private-location-docker$$$
Elastic provides Docker images that you can use to run {{fleet}} and an {{agent}} more easily. For monitors running on {{private-location}}s, you *must* use the `elastic-agent-complete` Docker image to create a self-hosted {{agent}} node. The standard {{ecloud}} or self-hosted {{agent}} will not work.

::::{important}
The `elastic-agent-complete` Docker image is the only way to have all available options that you see in the {{ecloud}}.

::::


Version 9.0.0-beta1 has not yet been released.

Then enroll and run an {{agent}}. You’ll need an enrollment token and the URL of the {{fleet-server}}. You can use the default enrollment token for your policy or create new policies and [enrollment tokens](https://www.elastic.co/guide/en/fleet/current/fleet-enrollment-tokens.html) as needed.

For more information on running {{agent}} with Docker, refer to [Run {{agent}} in a container](https://www.elastic.co/guide/en/fleet/current/elastic-agent-container.html).

Version 9.0.0-beta1 has not yet been released.

::::{important}
The `elastic-agent-complete` Docker image requires additional capabilities to operate correctly. Ensure `NET_RAW` and `SETUID` are enabled on the container.

::::


::::{note}
You may need to set other environment variables. Learn how in [{{agent}} environment variables guide](https://www.elastic.co/guide/en/fleet/current/agent-environment-variables.html).

::::



## Add a {{private-location}} [synthetics-private-location-add]

When the {{agent}} is running you can add a new {{private-location}} in {{kib}}:

1. Find `Synthetics` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Settings**.
3. Click **{{private-location}}s**.
4. Click **Add location**.
5. Give your new location a unique *Location name* and select the *Agent policy* you created above.
6. Click **Save**.

::::{important}
It is not currently possible to use custom CAs for synthetics browser tests in private locations without following a workaround. To learn more about the workaround, refer to the following GitHub issue: [elastic/synthetics#717](https://github.com/elastic/synthetics/issues/717).
::::



## Scaling {{private-location}}s [synthetics-private-location-scaling]

By default {{private-location}}s are configured to allow two simultaneous browser tests, and an unlimited number of lightweight checks. These limits can be set via the environment variables `SYNTHETICS_LIMIT_{{TYPE}}`, where `{{TYPE}}` is one of `BROWSER`, `HTTP`, `TCP`, and `ICMP` for the container running the {{agent}} docker image.

It is critical to allocate enough memory and CPU capacity to handle configured limits. Start by allocating at least 2 GiB of memory and two cores per browser instance to ensure consistent performance and avoid out-of-memory errors. Then adjust as needed. Resource requirements will vary depending on workload. Much less memory is needed for lightweight monitors. Start by allocating at least 512MiB of memory and two cores for lightweight checks. Then increase allocated memory and CPU based on observed usage patterns.

These limits are for simultaneous tests, not total tests. For example, if 60 browser tests were scheduled to run once per hour and each took 1 minute to run, that would fully occupy one execution slot. However, it is a good practice to set up execution slots with extra capacity. A good starting point would be to over-allocate by a factor of 5. In the previous example that would mean allocating 5 slots.


## Next steps [synthetics-private-location-next]

Now you can add monitors to your {{private-location}} in [the {{synthetics-app}}](../../../solutions/observability/apps/create-monitors-in-synthetics-app.md) or using the [Elastic Synthetics library’s `push` method](../../../solutions/observability/apps/create-monitors-with-project-monitors.md).
