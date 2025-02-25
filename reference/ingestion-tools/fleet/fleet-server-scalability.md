---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-server-scalability.html
---

# Fleet Server scalability [fleet-server-scalability]

This page summarizes the resource and {{fleet-server}} configuration requirements needed to scale your deployment of {{agent}}s. To scale {{fleet-server}}, you need to modify settings in your deployment and the {{fleet-server}} agent policy.

::::{tip}
Refer to the [Scaling recommendations](#agent-policy-scaling-recommendations) section for specific recommendations about using {{fleet-server}} at scale.
::::


First modify your {{fleet}} deployment settings in {{ecloud}}:

1. Log in to {{ecloud}} and go to your deployment.
2. Under **Deployments > *deployment name***, click **Edit**.
3. Under {{integrations-server}}:

    * Modify the compute resources available to the server to accommodate a higher scale of {{agent}}s
    * Modify the availability zones to satisfy fault tolerance requirements

    For recommended settings, refer to [Scaling recommendations ({{ecloud}})](#scaling-recommendations).

    :::{image} images/fleet-server-hosted-container.png
    :alt: {{fleet-server}} hosted agent
    :class: screenshot
    :::


Next modify the {{fleet-server}} configuration by editing the agent policy:

1. In {{fleet}}, open the **Agent policies** tab. Click the name of the **{{ecloud}} agent policy** to edit the policy.
2. Open the **Actions** menu next to the {{fleet-server}} integration and click **Edit integration**.

    :::{image} images/elastic-cloud-agent-policy.png
    :alt: {{ecloud}} policy
    :class: screenshot
    :::

3. Under {{fleet-server}}, modify **Max Connections** and other [advanced settings](#fleet-server-configuration) as described in [Scaling recommendations ({{ecloud}})](#scaling-recommendations).

    :::{image} images/fleet-server-configuration.png
    :alt: {{fleet-server}} configuration
    :class: screenshot
    :::



## Advanced {{fleet-server}} options [fleet-server-configuration]

The following advanced settings are available to fine tune your {{fleet-server}} deployment.

`cache`
:   `num_counters`
:   Size of the hash table. Best practice is to have this set to 10 times the max connections.

`max_cost`
:   Total size of the cache.


`server.timeouts`
:   `checkin_timestamp`
:   How often {{fleet-server}} updates the "last activity" field for each agent. Defaults to `30s`. In a large-scale deployment, increasing this setting may improve performance. If this setting is higher than `2m`, most agents will be shown as "offline" in the Fleet UI. For a typical setup, it’s recommended that you set this value to less than `2m`.

`checkin_long_poll`
:   How long {{fleet-server}} allows a long poll request from an agent before timing out. Defaults to `5m`. In a large-scale deployment, increasing this setting may improve performance.


`server.limits`
:   `policy_throttle`
:   How often a new policy is rolled out to the agents.


Deprecated: Use the `action_limit` settings instead.

`action_limit.interval`
:   How quickly {{fleet-server}} dispatches pending actions to the agents.

`action_limit.burst`
:   Burst of actions that may be dispatched before falling back to the rate limit defined by `interval`.

`checkin_limit.max`
:   Maximum number of agents that can call the checkin API concurrently.

`checkin_limit.interval`
:   How fast the agents can check in to the {{fleet-server}}.

`checkin_limit.burst`
:   Burst of check-ins allowed before falling back to the rate defined by `interval`.

`checkin_limit.max_body_byte_size`
:   Maximum size in bytes of the checkin API request body.

`artifact_limit.max`
:   Maximum number of agents that can call the artifact API concurrently. It allows the user to avoid overloading the {{fleet-server}} from artifact API calls.

`artifact_limit.interval`
:   How often artifacts are rolled out. Default of `100ms` allows 10 artifacts to be rolled out per second.

`artifact_limit.burst`
:   Number of transactions allowed for a burst, controlling oversubscription on outbound buffer.

`artifact_limit.max_body_byte_size`
:   Maximum size in bytes of the artficact API request body.

`ack_limit.max`
:   Maximum number of agents that can call the ack API concurrently. It allows the user to avoid overloading the {{fleet-server}} from Ack API calls.

`ack_limit.interval`
:   How often an acknowledgment (ACK) is sent. Default value of `10ms` enables 100 ACKs per second to be sent.

`ack_limit.burst`
:   Burst of ACKs to accommodate (default of 20) before falling back to the rate defined in `interval`.

`ack_limit.max_body_byte_size`
:   Maximum size in bytes of the ack API request body.

`enroll_limit.max`
:   Maximum number of agents that can call the enroll API concurrently. This setting allows the user to avoid overloading the {{fleet-server}} from Enrollment API calls.

`enroll_limit.interval`
:   Interval between processing enrollment request. Enrollment is both CPU and RAM intensive, so the number of enrollment requests needs to be limited for overall system health. Default value of `100ms` allows 10 enrollments per second.

`enroll_limit.burst`
:   Burst of enrollments to accept before falling back to the rate defined by `interval`.

`enroll_limit.max_body_byte_size`
:   Maximum size in bytes of the enroll API request body.

`status_limit.max`
:   Maximum number of agents that can call the status API concurrently. This setting allows the user to avoid overloading the Fleet Server from status API calls.

`status_limit.interval`
:   How frequently agents can submit status requests to the Fleet Server.

`status_limit.burst`
:   Burst of status requests to accomodate before falling back to the rate defined by interval.

`status_limit.max_body_byte_size`
:   Maximum size in bytes of the status API request body.

`upload_start_limit.max`
:   Maximum number of agents that can call the uploadStart API concurrently. This setting allows the user to avoid overloading the Fleet Server from uploadStart API calls.

`upload_start_limit.interval`
:   How frequently agents can submit file start upload requests to the Fleet Server.

`upload_start_limit.burst`
:   Burst of file start upload requests to accomodate before falling back to the rate defined by interval.

`upload_start_limit.max_body_byte_size`
:   Maximum size in bytes of the uploadStart API request body.

`upload_end_limit.max`
:   Maximum number of agents that can call the uploadEnd API concurrently. This setting allows the user to avoid overloading the Fleet Server from uploadEnd API calls.

`upload_end_limit.interval`
:   How frequently agents can submit file end upload requests to the Fleet Server.

`upload_end_limit.burst`
:   Burst of file end upload requests to accomodate before falling back to the rate defined by interval.

`upload_end_limit.max_body_byte_size`
:   Maximum size in bytes of the uploadEnd API request body.

`upload_chunk_limit.max`
:   Maximum number of agents that can call the uploadChunk API concurrently. This setting allows the user to avoid overloading the Fleet Server from uploadChunk API calls.

`upload_chunk_limit.interval`
:   How frequently agents can submit file chunk upload requests to the Fleet Server.

`upload_chunk_limit.burst`
:   Burst of file chunk upload requests to accomodate before falling back to the rate defined by interval.

`upload_chunk_limit.max_body_byte_size`
:   Maximum size in bytes of the uploadChunk API request body.


## Scaling recommendations ({{ecloud}}) [scaling-recommendations]

The following tables provide the minimum resource requirements and scaling guidelines based on the number of agents required by your deployment. It should be noted that these compute resource can be spread across multiple availability zones (for example: a 32GB RAM requirement can be satisfed with 16GB of RAM in 2 different zones).

* [Resource requirements by number of agents](#resource-requirements-by-number-agents)


### Resource requirements by number of agents [resource-requirements-by-number-agents]

|     |     |     |     |
| --- | --- | --- | --- |
| Number of Agents | {{fleet-server}} Memory | {{fleet-server}} vCPU | {{es}} Hot Tier |
| 2,000 | 2GB | up to 8 vCPU | 32GB  RAM  &#124; 8 vCPU |
| 5,000 | 4GB | up to 8 vCPU | 32GB  RAM  &#124; 8 vCPU |
| 10,000 | 8GB | up to 8 vCPU | 128GB RAM  &#124; 32 vCPU |
| 15,000 | 8GB | up to 8 vCPU | 256GB RAM  &#124; 64 vCPU |
| 25,000 | 8GB | up to 8 vCPU | 256GB RAM  &#124; 64 vCPU |
| 50,000 | 8GB | up to 8 vCPU | 384GB RAM  &#124; 96 vCPU |
| 75,000 | 8GB | up to 8 vCPU | 384GB RAM  &#124; 96 vCPU |
| 100,000 | 16GB | 16 vCPU | 512GB RAM  &#124; 128 vCPU |

A series of scale performance tests are regularly executed in order to verify the above requirements and the ability for {{fleet}} to manage the advertised scale of {{agent}}s. These tests go through a set of acceptance criteria. The criteria mimics a typical platform operator workflow. The test cases are performing agent installations, version upgrades, policy modifications, and adding/removing integrations, tags, and policies. Acceptance criteria is passed when the {{agent}}s reach a `Healthy` state after any of these operations.


## Scaling recommendations [agent-policy-scaling-recommendations]

**{{agent}} policies**

A single instance of {{fleet}} supports a maximum of 1000 {{agent}} policies. If more policies are configured, UI performance might be impacted. The maximum number of policies is not affected by the number of spaces in which the policies are used.

If you are using {{agent}} with [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), the maximum supported number of {{agent}} policies is 500.

**{{agents}}**

When you use {{fleet}} to manage a large volume (10k or more) of {{agents}}, the check-in from each of the multiple agents triggers an {{es}} authentication request. To help reduce the possibility of cache eviction and to speed up propagation of {{agent}} policy changes and actions, we recommend setting the [API key cache size](elasticsearch://docs/reference/elasticsearch/configuration-reference/security-settings.md#api-key-service-settings) in your {{es}} configuration to 2x the maximum number of agents.

For example, with 25,000 running {{agents}} you could set the cache value to `50000`:

```yaml
xpack.security.authc.api_key.cache.max_keys: 50000
```
