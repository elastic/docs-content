---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-infrastructure.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-infrastructure.html
---

# Infrastructure [observability-apm-infrastructure]

::::{important}

The Applications UI Infrastructure functionality is in beta and is subject to change. The design and code is less mature than official generally available features and is being provided as-is with no warranties.

::::


The **Infrastructure** tab provides information about the containers, pods, and hosts that the selected service is linked to.

* **Pods**: Uses the `kubernetes.pod.name` from the [APM metrics data streams](../../../solutions/observability/apps/metrics.md).
* **Containers**: Uses the `container.id` from the [APM metrics data streams](../../../solutions/observability/apps/metrics.md).
* **Hosts**: If the application is containerized—​if the APM metrics documents include `container.id`-- the `host.name` is used from the infrastructure data streams (filtered by `container.id`). If not, `host.hostname` is used from the APM metrics data streams.


:::{image} ../../../images/serverless-infra.png
:alt: Example view of the Infrastructure tab in the Applications UI
:class: screenshot
:::

IT ops and software reliability engineers (SREs) can use this tab to quickly find a service’s underlying infrastructure resources when debugging a problem. Knowing what infrastructure is related to a service allows you to remediate issues by restarting, killing hanging instances, changing configuration, rolling back deployments, scaling up, scaling out, and so on.

::::{tip}
**Why is the infrastructure tab empty?**

If there is no data in the Application UI’s infrastructure tab for a selected service, you can read more about why this happens and how to fix it in the [troubleshooting docs](../../../troubleshoot/observability/apm/common-problems.md#troubleshooting-apm-infra-data).

::::