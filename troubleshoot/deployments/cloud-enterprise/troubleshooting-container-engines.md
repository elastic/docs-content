---
navigation_title: "Container engines"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-troubleshooting-containers.html
---

# Troubleshoot container engines [ece-troubleshooting-containers]

This article describes how to troubleshoot container engine services in Elastic Cloud Enterprise. We refer to [Docker](https://www.docker.com/) by default, as it’s the most common container engine, but these steps are also valid for [Podman](https://podman.io/). You can simply replace `docker` in the commands  with `podman` as needed.

::::{important}
Do not restart the Docker daemon unless directly prescribed by Elastic Support upon reviewing an [{{ece}} diagnostic](run-ece-diagnostics-tool.md), as historically Docker can leave residual orphan processes. We also advise against running any variation of Docker’s `prune` to avoid accidental data loss.
::::



## Use supported configuration [ece-troubleshooting-containers-supported]

Make sure to use a combination of [Linux operating systems](../../../deploy-manage/deploy/cloud-enterprise/configure-operating-system.md) and container engine version that is supported, following our official [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise). Using unsupported combinations can cause a plethora of either intermediate or potentially permanent issues with you {{ece}} environment, such as failures to create [system deployments](../../../deploy-manage/deploy/cloud-enterprise/system-deployments-configuration.md), to upgrade workload deployments, proxy timeouts, data loss, and more.


## Troubleshoot unhealthy containers [ece-troubleshooting-containers-unhealthy]

While troubleshooting the stability of an {{ece}} host, you may encounter `unhealthy` Docker containers as reported by [`ps`](https://docs.docker.com/reference/cli/docker/container/ls).

System containers reporting unhealthy is infrequent and usually only occurs after an unexpected occurance or issues while performing operating system maintenance. If operating system maintenance does need performed, kindly pivot to our [perform host maintenance guide](../../../deploy-manage/maintenance/ece/perform-ece-hosts-maintenance.md).


### Restart deployment instances [ece-troubleshooting-containers-unhealthy-instances]

If the `unhealthy` Docker container is a Deployment’s instance, name formatting `fac-{{cluster_id}}-instance-{{node_id}}`, we recommend restarting the instance from the {{ece}} UI via [its pause and resume mechanism](../../../deploy-manage/maintenance/ece/deployments-maintenance.md) rather than via Docker.

If the `unhealthy` status returns, we recommend investigating via [our troubleshooting bootlooping guide](../../monitoring/node-bootlooping.md).

This should indicate an issue with the {{es}} configuration rather than any Docker-level problem. An isolated exception effecting [air-gapped environments](../../../deploy-manage/deploy/cloud-enterprise/air-gapped-install.md) is if the expected Docker [`image`](https://docs.docker.com/reference/cli/docker/image/ls/) does not yet exist on the Allocator in which case its logs would report `Unable to pull image`.


### Restart service containers [ece-troubleshooting-containers-unhealthy-restart]

While troubleshooting `unhealthy` {{ece}} system containers (name prefix `frc-`), *some* may be restarted while others should not.

{{ece}}'s [runners](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-get-runners) will automatically create or restart missing system containers. If you’re attempting to permanently remove a system container by removing its role from the host, you’d instead [update runner roles](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-set-runner-roles). If eligible system containers return to an `unhealthy` status after restart, we recommend reviewing their start-up Docker [`logs`](https://docs.docker.com/reference/cli/docker/container/logs/).

It is safe to restart the following via Docker [`stop`](https://docs.docker.com/reference/cli/docker/container/stop/) followed by Docker [`rm`](https://docs.docker.com/reference/cli/docker/container/rm/) on:

* `frc-allocator-metricbeats-allocator-metricbeat`
* `frc-allocators-allocator`
* `frc-beats-runners-beats-runner`
* `frc-constructors-constructor`
* `frc-proxies-proxyv2`
* `frc-proxies-route-server`

It is safe to restart the following via Docker [`restart`](https://docs.docker.com/reference/cli/docker/container/restart/):

* `frc-client-forwarders-client-forwarder`
* `frc-directors-director`
* `frc-services-forwarders-services-forwarder`

It is **not** safe to restart the following without explicit steps from Elastic Support upon reviewing an [{{ece}} diagnostic](run-ece-diagnostics-tool.md):

* any container name prefixing `fac-`
* `frc-runners-runner`
* `frc-zookeeper-servers-zookeeper`

For unhealthy Zookeeper, instead see [verify Zookeeper sync status](verify-zookeeper-sync-status.md) and [resolving Zookeeper quorum](rebuilding-broken-zookeeper-quorum.md).

For any {{ece}} system container not listed, kindly reach out to [Elastic Support](ask-for-help.md) for advisement.
