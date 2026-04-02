---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-allocator-affinity.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Configure allocator affinity [ece-configuring-allocator-affinity]

One of the benefits of the ECE platform is its robust deployment instance distribution logic that maximizes the utilization of the underlying resources you deploy the {{stack}} on. In ECE 2.4 and later, you can customize how {{stack}} deployments get distributed across the available set of allocators in your ECE installation, which is known as *allocator affinity*.


## Before you begin [ece_before_you_begin_6] 

Configuring allocator affinity is an optional post-installation task that changes the behavior of {{ece}}. If you do not explicitly set an affinity strategy, all instances use the [`fill-anti-affinity`](#fill-anti-affinity) strategy by default.

To follow these steps, you must be familiar with using the ECE RESTful API. The API examples in this topic use HTTPS, which requires that you have a [TLS certificate already installed](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md). For testing purposes only, you can specify the `-k` option to turn off certificate verification, as shown in our examples, or use HTTP over port 12400 until you get your TLS certificate sorted out.


## Affinity strategies [ece_affinity_strategies] 

The following distribution strategies to configure allocator affinity are available:

$$$fill-anti-affinity$$$`fill-anti-affinity` (default)
:   Prefers to create instances of the same deployment on separate allocators, if available. This strategy tries to fill an already used allocator in a given zone before moving on to the next one, but it will prioritize separating instances of the same deployment onto different allocators. The strategy strikes a good balance between utilization and fault tolerance, as it minimizes the impact on any given deployment in case of a host failure. This strategy is the default for ECE 2.3 and later.

`fill`
:   Similar to the previous strategy, optimizes for maximum utilization of already used allocators before expanding to new, unused ones. Because this strategy makes sure that existing resources are fully utilized before requiring new ones to be provisioned, it is especially useful when running ECE on cloud environments where you typically pay only for provisioned capacity. With this strategy, new {{es}} nodes and {{kib}} instances for a deployment are created on the least empty allocator in a given zone, even if multiple instances end up on the same allocator, making sure to fill it first before moving on to the next allocator in that zone. The trade-off is that you potentially give up host-level high availability (HA) if an allocator gets filled with multiple instances from the same deployment. This strategy was the default for ECE 2.2 and earlier.

`distribute`
:   This strategy optimizes for distributing the deployment instances as evenly as possible across all available resources in a given availability zone, creating new deployment instances on the least used allocators. This stategy is useful in scenarios where the hardware resources are already provisioned, typically in on-premise datacenters, and you want to use as much of them as possible. Available in ECE 2.4 and later.

`distribute-anti-affinity`
:   Similar to the previous strategy, with one change: this strategy prefers to create instances of the same deployment on separate allocators in a specific zone, if available, in order to minimize the impact of an allocator failure on any given deployment. Available in ECE 2.4 and later.


## Steps [ece_steps_3] 

To check how allocator affinity is currently configured:

```sh
curl -X GET -u admin:PASSWORD -k https://$COORDINATOR_HOST:12443/api/v1/platform/configuration/store/constructor
{
  "errors": [{
    "code": "platform.config.store.not_found",
    "message": "Config option [constructor] could not be found"
  }]
}
```

If a configuration option cannot be found, the default `fill-anti-affinity` strategy is being used.

To set allocator affinity to the `distribute-anti-affinity` strategy:

```sh
curl -X POST -u admin:PASSWORD -k https://$COORDINATOR_HOST:12443/api/v1/platform/configuration/store/constructor -H 'Content-Type: application/json' -d '{ "value": "{ \"allocator_prioritization\": \"distribute-anti-affinity\" }" }'
{
  "changed": false,
  "name": "constructor",
  "value": "{ \"allocator_prioritization\": \"distribute-anti-affinity\" }"
}
```

To update allocator affinity to the `distribute` strategy:

```sh
curl -X PUT -u admin:PASSWORD -k https://$COORDINATOR_HOST:12443/api/v1/platform/configuration/store/constructor -H 'Content-Type: application/json' -d '{ "value": "{ \"allocator_prioritization\": \"distribute\" }" }'
{
  "changed": true,
  "name": "constructor",
  "value": "{ \"allocator_prioritization\": \"distribute\" }"
}
```

To change allocator affinity back to the default behavior:

```sh
curl -X DELETE -u admin:PASSWORD -k https://$COORDINATOR_HOST:12443/api/v1/platform/configuration/store/constructor
{

}
```

