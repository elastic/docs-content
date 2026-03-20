---
navigation_title: On Elastic Cloud on Kubernetes
applies_to:
  deployment:
    eck: ga
products:
  - id: cloud-kubernetes
---

# Remote clusters on {{eck}} [k8s-remote-clusters]

::::{include} _snippets/eck_rcs_intro.md
::::

::::{include} _snippets/terminology.md
::::

When using remote cluster connections with ECK, the setup process varies depending on how both the local and remote clusters are deployed:

* When both clusters are managed by the same operator, ECK can automate certificate and API-key management, connection configuration, and reconciliation.
* When external clusters are involved, ECK provides limited automation, and additional manual configuration is required on both the local and remote clusters.

## Prerequisites

To use CCS or CCR, your {{es}} clusters must meet the following criteria:

* The local and remote clusters must run on compatible versions of {{es}}. Review the version compatibility table.
  
  :::{include} _snippets/remote-cluster-certificate-compatibility.md
  :::

* Network connectivity between the clusters. Review the [connection modes](./connection-modes.md) and the [security models](./security-models.md) to understand the connectivity requirements for your specific setup. Remote cluster connections can operate through Kubernetes services, load balancers, reverse proxies, or other intermediaries, as long as the local cluster can reach the remote cluster’s endpoint.

* The remote clusters feature on ECK requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../license/manage-your-license-in-eck.md) for more details about managing licenses.

## Set up remote clusters with {{eck}} [eck-rcs-setup]

Use one of the following guides depending on how the local and remote clusters are deployed.

Connect from ECK-managed clusters:

  - [Connect to {{es}} clusters in the same ECK environment](./eck-remote-clusters.md)
  - [Connect to a different ECK environment](./eck-remote-clusters-to-other-eck.md)
  - [Connect to external clusters or deployments](./eck-remote-clusters-to-external.md)

Connect to ECK-managed clusters from other deployment types:

  - [](./ec-enable-ccs-for-eck.md)
  - [](./ece-enable-ccs-for-eck.md)
  - [Connect self-managed {{es}} clusters to ECK](./self-remote-cluster-eck.md)
