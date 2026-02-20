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

## Running as root [k8s_running_as_root_eck_2_10_0_and_agent_7_14_0]

Until {{stack}} version 7.14.0 and ECK version 2.10.0, {{agent}} and {{fleet-server}} were required to run as root.

As of {{stack}} version 7.14.0 and ECK version 2.10.0, it is possible to run {{agent}} and {{fleet}} as a non-root user. With {{agent}} version 8.16.0, running as a non-root user is further simplified because the Agent automatically manages ownership of its volume mounts (except on OpenShift/SELinux-enabled clusters). Refer to [Running as a non-root user](configuration-fleet.md#k8s-elastic-agent-running-as-a-non-root-user) for instructions.


## {{agent}} running in the same namespace as the {{stack}}. [k8s_agent_running_in_the_same_namespace_as_the_stack]

Until ECK version 2.11.0, {{agent}} and {{fleet-server}} were required to run within the same Namespace as {{es}}.

As of ECK version 2.11.0, {{agent}}, {{fleet-server}} and {{es}} can all be deployed in different Namespaces.


## Running {{endpoint-sec}} integration [k8s_running_endpoint_sec_integration]

Running {{endpoint-sec}} [integration](/solutions/security/configure-elastic-defend/install-elastic-defend.md) is not yet supported in containerized environments, like {{k8s}}. This is not an ECK limitation, but the limitation of the integration itself. Note that you can use ECK to deploy {{es}}, {{kib}} and {{fleet-server}}, and add {{endpoint-sec}} integration to your policies if {{agents}} running those policies are deployed in non-containerized environments.


## {{fleet-server}} initialization fails on minikube when CNI is disabled [k8s_fleet_server_initialization_fails_on_minikube_when_cni_is_disabled]

When deployed with ECK, the {{fleet-server}} Pod makes an HTTP call to itself during {{fleet}} initialization using its Service. Since a [Pod cannot reach itself through its Service on minikube](https://github.com/kubernetes/minikube/issues/1568) when CNI is disabled, the call hangs until the connection times out and the Pod enters a crash loop.

Solution: enable CNI when starting minikube: `minikube start --cni=true`.


## Storing local state in host path volume [k8s_storing_local_state_in_host_path_volume_2]

::::{include} _snippets/storing-local-state-host-path-volume.md