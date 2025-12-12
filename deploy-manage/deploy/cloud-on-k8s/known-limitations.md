---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elastic-agent-fleet-known-limitations.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Known limitations [k8s-elastic-agent-fleet-known-limitations]

## Running as root (ECK < 2.10.0 and Agent < 7.14.0) [k8s_running_as_root_eck_2_10_0_and_agent_7_14_0]

Until version 7.14.0 and ECK version 2.10.0, {{agent}} and {{fleet-server}} were required to run as root.

As of {{stack}} version 7.14.0 and ECK version 2.10.0 it is also possible to run {{agent}} and {{fleet}} as a non-root user, and with {{agent}} version 8.16.0 running as a non-root user is further simplified. See [Storing local state in host path volume](configuration-examples-standalone.md#k8s_storing_local_state_in_host_path_volume) for instructions.


## {{agent}} running in the same namespace as the {{stack}}. [k8s_agent_running_in_the_same_namespace_as_the_stack]

Until ECK version 2.11.0, {{agent}} and {{fleet-server}} were required to run within the same Namespace as {{es}}.

As of ECK version 2.11.0, {{agent}}, {{fleet-server}} and {{es}} can all be deployed in different Namespaces.


## Running {{endpoint-sec}} integration [k8s_running_endpoint_sec_integration]

Running {{endpoint-sec}} [integration](/solutions/security/configure-elastic-defend/install-elastic-defend.md) is not yet supported in containerized environments, like {{k8s}}. This is not an ECK limitation, but the limitation of the integration itself. Note that you can use ECK to deploy {{es}}, {{kib}} and {{fleet-server}}, and add {{endpoint-sec}} integration to your policies if {{agents}} running those policies are deployed in non-containerized environments.


## {{fleet-server}} initialization fails on minikube when CNI is disabled [k8s_fleet_server_initialization_fails_on_minikube_when_cni_is_disabled]

When deployed with ECK, the {{fleet-server}} Pod makes an HTTP call to itself during {{fleet}} initialization using its Service. Since a [Pod cannot reach itself through its Service on minikube](https://github.com/kubernetes/minikube/issues/1568) when CNI is disabled, the call hangs until the connection times out and the Pod enters a crash loop.

Solution: enable CNI when starting minikube: `minikube start --cni=true`.


## Storing local state in host path volume [k8s_storing_local_state_in_host_path_volume_2]

{{agent}} managed by ECK stores local state in a host path volume by default. This ensures that {{integrations}} run by the agent can continue their work without duplicating work that has already been done after the Pod has been recreated for example because of a Pod configuration change. Multiple replicas of an agent, for example {{fleet}} Servers, can not be deployed on the same underlying {{k8s}} node as they would try to use the same host path. There are 1 or 2 options for managing this feature depending on the version of Elastic Agent:

::::{tab-set}

:::{tab-item} {{agent}} 8.16 and higher

1. If local state storage in `hostPath` volumes is not desired this can be turned off by configuring an `emptyDir` volume instead.
2. If local state storage is still desired but running the Agent container as root is not allowed, then you can run a `DaemonSet` that adjusts the permissions for the Agent local state on each Node prior to running {{agent}}. Note that this `DaemonSet` must be `runAsUser: 0` and possibly `privileged: true`. Also note the {{kib}} changes required to trust the {{es}} CA when running in fleet mode.

Full configuration examples exist in  [Running as a non-root user](configuration-fleet.md#k8s-elastic-agent-running-as-a-non-root-user).

:::

:::{tab-item} {{agent}} 8.15 and before 

1. If local state storage in `hostPath` volumes is not desired this can be turned off by configuring an `emptyDir` volume instead.

:::

::::