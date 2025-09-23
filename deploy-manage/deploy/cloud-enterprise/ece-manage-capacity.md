---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-manage-capacity.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Manage your allocators capacity [ece-manage-capacity]

In {{ece}} (ECE), every host is a runner. Depending on the size of your platform, runners can have [one or more roles](ece-roles.md): Coordinator, director, proxy, and allocator. While planning the capacity of your ECE installation, you have to properly size the capacity for all roles. However, the allocator role deserves particular attention, as it hosts the {{es}}, {{kib}}, and APM nodes, and the relevant services.

This section focuses on the allocator role, and explains how to plan its capacity in terms of memory, CPU, `processors` setting, and storage.

* [Memory](#ece-alloc-memory)
* [CPU quotas](#ece-alloc-cpu)
* [Processors setting](#ece-alloc-processors-setting)
* [Storage](#ece-alloc-storage)


## Memory [ece-alloc-memory]

You should plan your deployment size based on the amount of data you ingest. Memory is the main scaling unit for a deployment. Other units, like CPU and disks, are proportional to the memory size. The memory available for an allocator is called *capacity*.

During installation, the allocator capacity defaults to 85% of the host physical memory, as the rest is reserved for ECE system services.

::::{note}
ECE does not support hot-adding of resources to a running node.  When increasing CPU/memory allocated to a ECE node, a restart is needed to utilize the additional resources.
::::


To adjust the allocator capacity prior to ECE 3.5.0, you must reinstall ECE on the host with a new value assigned to the `--capacity` parameter. Starting with ECE 3.5.0, you can update the allocator capacity using the [allocator settings ECE API](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-set-allocator-settings). After making this change, you must restart the allocator service for it to take effect.

```sh
curl -X PUT \
  http(s)://<ece_admin_url:port>/api/v1/platform/infrastructure/allocators/<allocator_id>/settings \
  -H “Authorization: ApiKey $ECE_API_KEY” \ <1>
  -H 'Content-Type: application/json' \
  -d '{"capacity":<Capacity_Value_in_MB>}'
```
1. For information on how to use API keys for authentication, refer to [Access the API from the command line](cloud://reference/cloud-enterprise/ece-api-command-line.md).

::::{important}
When running ECE on Podman, CPU quotas for existing instances cannot be disabled or updated. As a result, changing an allocator’s capacity won’t affect the CPU quotas of already running containers.
::::

After applying the change, log in to the allocator host you updated and restart the allocator service:

```sh
docker restart frc-allocators-allocator
```

### Examples [ece_examples]

Here are some examples to make Elastic deployments and ECE system services run smoothly on your host:

* If the runner has more than one role (allocator, coordinator, director, or proxy), you should reserve 28GB of host memory. For example, on a host with 256GB of RAM, 228GB is suitable for deployment use.
* If the runner has only the Allocator role, you should reserve 12GB of host memory. For example, on a host with 256GB of RAM, 244GB is suitable for deployment use.

Note that the recommended reservations above are not guaranteed upper limits, if you measure actual memory usage you may see numbers 0-2GB higher or lower.

These fluctuations should not be a concern in practice. To get actual limits that could be used in alerts, you could add 4GB to the recommended values above.


## CPU quotas [ece-alloc-cpu]

ECE uses CPU quotas to assign shares of the allocator host to the instances that are running on it. To calculate the CPU quota, use the following formula:

`CPU quota = DeploymentRAM / HostCapacity`

::::{important}
In ECE versions prior to 3.5.0, the CPU quota is always calculated using the memory specified at installation time, even if you later update the host capacity using the API.
::::

### Examples [ece_examples_2]

Consider a 32GB deployment hosted on a 128GB allocator.

If you use the default system service reservation, the CPU quota is 29%:

* CPU quota = 32 / (128 * 0.85) = 29%

If you use 12GB Allocator system service reservation, the CPU quota is 28%:

* CPU quota = 32 / (128 - 12) = 28%

Those percentages represent the upper limit of the % of the total CPU resources available in a given 100ms period.


## Processors setting [ece-alloc-processors-setting]

In addition to the [CPU quotas](#ece-alloc-cpu), the `processors` setting also plays a relevant role.

The allocated `processors` setting originates from {{es}} and is responsible for calculating your [thread pools](elasticsearch://reference/elasticsearch/configuration-reference/thread-pool-settings.md#node.processors). While the CPU quota defines the percentage of the total CPU resources of an allocator that are assigned to an instance, the allocated `processors` define how the thread pools are calculated in {{es}}, and therefore how many concurrent search and indexing requests an instance can process. In other words, the CPU ratio defines how fast a single task can be completed, while the `processors` setting defines how many different tasks can be completed at the same time.

We rely on {{es}} and the `-XX:ActiveProcessorCount` JVM setting to automatically detect the allocated `processors`.

In earlier versions of ECE and {{es}}, the [{{es}} processors](elasticsearch://reference/elasticsearch/configuration-reference/thread-pool-settings.md#node.processors) setting was used to configure the allocated `processors` according to the following formula:

`Math.min(16,Math.max(2,(16*instanceCapacity*1.0/1024/64).toInt))`

The following table gives an overview of the allocated `processors` that are used to calculate the {{es}} [thread pools](elasticsearch://reference/elasticsearch/configuration-reference/thread-pool-settings.md) based on the preceding formula:

| instance size | vCPU |
| --- | --- |
| 1024 | 2 |
| 2048 | 2 |
| 4096 | 2 |
| 8192 | 2 |
| 16384 | 4 |
| 32768 | 8 |

This table also provides a rough indication of what the auto-detected value could be on newer versions of ECE and {{es}}.


## Storage [ece-alloc-storage]

ECE has specific [hardware prerequisites](ece-hardware-prereq.md) for storage. Disk space is consumed by system logs, container overhead, and deployment data.

The main factor for selecting a disk quota is the deployment data, that is, data from your {{es}}, {{kib}}, and APM nodes. The biggest portion of data is consumed by the {{es}} nodes.

::::{note}
ECE uses [XFS](ece-software-prereq.md#ece-xfs) to enforce specific disk space quotas to control the disk consumption for the deployment nodes running on your allocator.
::::


::::{important}
You must use XFS and have quotas enabled on all allocators, otherwise disk usage won’t display correctly.
::::


To calculate the disk quota, use the following formula:

`Diskquota = ICmultiplier * Deployment RAM`

`ICmultiplier` is the disk multiplier of the instance configuration that you defined in your ECE environment.

The default multiplier for `data.default` is 32, which is used for hot nodes. The default multiplier for `data.highstorage` is 64, which is used for warm and cold nodes. The FS multiplier for `data.frozen` is 80, which is used for frozen nodes.

You can change the value of the disk multiplier at different levels:

* At the ECE level, check [Edit instance configurations](ece-configuring-ece-instance-configurations-edit.md).
* At the instance level, [log into the Cloud UI](log-into-cloud-ui.md) and proceed as follows:

    1. From your deployment overview page, find the instance you want and open the instance menu.
    2. Select **Override disk quota**.
    3. Adjust the disk quota to your needs.


::::{important}
The override only persists during the lifecycle of the instance container. If a new container is created, for example during a `grow_and_shrink` plan or a vacate operation, the quota is reset to its default. To increase the storage ratio in a persistent way, [edit the instance configurations](ece-configuring-ece-instance-configurations-edit.md).
::::


