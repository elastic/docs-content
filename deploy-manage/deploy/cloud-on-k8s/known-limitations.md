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

As of {{stack}} version 7.14.0 and ECK version 2.10.0 it is also possible to run {{agent}} and {{fleet}} as a non-root user. See [Storing local state in host path volume](configuration-examples-standalone.md#k8s_storing_local_state_in_host_path_volume) for instructions.


## {{agent}} running in the same namespace as the {{stack}}. [k8s_agent_running_in_the_same_namespace_as_the_stack]

Until ECK version 2.11.0, {{agent}} and {{fleet-server}} were required to run within the same Namespace as {{es}}.

As of ECK version 2.11.0, {{agent}}, {{fleet-server}} and {{es}} can all be deployed in different Namespaces.


## Running {{endpoint-sec}} integration [k8s_running_endpoint_sec_integration]

Running {{endpoint-sec}} [integration](/solutions/security/configure-elastic-defend/install-elastic-defend.md) is not yet supported in containerized environments, like {{k8s}}. This is not an ECK limitation, but the limitation of the integration itself. Note that you can use ECK to deploy {{es}}, {{kib}} and {{fleet-server}}, and add {{endpoint-sec}} integration to your policies if {{agents}} running those policies are deployed in non-containerized environments.


## {{fleet-server}} initialization fails on minikube when CNI is disabled [k8s_fleet_server_initialization_fails_on_minikube_when_cni_is_disabled]

When deployed with ECK, the {{fleet-server}} Pod makes an HTTP call to itself during {{fleet}} initialization using its Service. Since a [Pod cannot reach itself through its Service on minikube](https://github.com/kubernetes/minikube/issues/1568) when CNI is disabled, the call hangs until the connection times out and the Pod enters a crash loop.

Solution: enable CNI when starting minikube: `minikube start --cni=true`.


## Storing local state in host path volume [k8s_storing_local_state_in_host_path_volume_2]

{{agent}} managed by ECK stores local state in a host path volume by default. This ensures that {{integrations}} run by the agent can continue their work without duplicating work that has already been done after the Pod has been recreated for example because of a Pod configuration change. Multiple replicas of an agent, for example {{fleet}} Servers, can not be deployed on the same underlying {{k8s}} node as they would try to use the same host path. Consider the following options for managing local state storage:

* If local state storage in `hostPath` volumes is not desired this can be turned off by configuring an `emptyDir` volume instead.
* {applies_to}`stack: ga 8.16` If local state storage is still desired but running the Agent container as root is not allowed, then you can give the Agent container the `CHOWN` and `SETPCAP` capabilities. At startup, {{agent}} changes the owner of its state directory to its own user and group.
* If you use an {{agent}} version before 8.16 or cannot grant additional capabilities to the Agent container, you can use a `DaemonSet` to adjust the permissions of the Agent local state on each node before {{agent}} starts. This `DaemonSet` must run as root (`runAsUser: 0`) and might also require `privileged: true`. Also note the {{kib}} changes required to trust the {{es}} CA when running in fleet mode.

Full configuration examples exist in  [Running as a non-root user](configuration-fleet.md#k8s-elastic-agent-running-as-a-non-root-user).


## Rolling updates and multiple replicas with host path volumes [k8s_agent_hostpath_rolling_updates]

Two {{agent}} Pods on the same {{k8s}} node cannot use the same host path at the same time. The second Pod stops with the error `failed to get app lock: another elastic-agent is already running`. This happens in two cases:

* You deploy {{agent}} as a `Deployment` with more than one replica, and {{k8s}} schedules two replicas on the same node.
* You update a `Deployment` that has one replica, for example to change resources. By default, a `Deployment` uses the `RollingUpdate` strategy. The strategy starts the new Pod before it stops the old Pod. If both Pods run on the same node, the new Pod fails until the old Pod stops.

To avoid the error, use one of these options:

1. Deploy {{agent}} as a `DaemonSet`. A `DaemonSet` runs one Pod on each node.
2. For a `Deployment` with one replica, set the update strategy to `Recreate` so that {{k8s}} stops the old Pod before starting the new one. The {{agent}} is not available during the update.

    ```yaml
    apiVersion: agent.k8s.elastic.co/v1alpha1
    kind: Agent
    metadata:
      name: elastic-agent
    spec:
      deployment:
        replicas: 1
        strategy:
          type: Recreate
    ...
    ```

3. For a `Deployment` with more than one replica, add a `podAntiAffinity` rule to prevent two replicas from running on the same node. Make sure that the cluster has more available nodes than replicas. Otherwise, a Pod stays in the `Pending` state.

    ```yaml
    apiVersion: agent.k8s.elastic.co/v1alpha1
    kind: Agent
    metadata:
      name: elastic-agent
    spec:
      deployment:
        replicas: 2
        podTemplate:
          spec:
            affinity:
              podAntiAffinity:
                requiredDuringSchedulingIgnoredDuringExecution:
                - labelSelector:
                    matchLabels:
                      agent.k8s.elastic.co/name: elastic-agent <1>
                  topologyKey: kubernetes.io/hostname
    ...
    ```

    1. Use the name of the {{agent}} resource.

4. Use an `emptyDir` volume instead of the host path volume. {{agent}} then does not keep its local state when a Pod restarts. This option is not recommended. Refer to [Storing local state in host path volume](#k8s_storing_local_state_in_host_path_volume_2).


