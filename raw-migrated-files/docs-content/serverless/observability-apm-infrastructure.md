# Infrastructure [observability-apm-infrastructure]

::::{admonition} Applications UI Infrastructure is in beta
:class: important

The Applications UI Infrastructure functionality is in beta and is subject to change. The design and code is less mature than official generally available features and is being provided as-is with no warranties.

::::


The **Infrastructure** tab provides information about the containers, pods, and hosts that the selected service is linked to.

:::{image} ../../../images/serverless-infra.png
:alt: Example view of the Infrastructure tab in the Applications UI
:class: screenshot
:::

IT ops and software reliability engineers (SREs) can use this tab to quickly find a service’s underlying infrastructure resources when debugging a problem. Knowing what infrastructure is related to a service allows you to remediate issues by restarting, killing hanging instances, changing configuration, rolling back deployments, scaling up, scaling out, and so on.
