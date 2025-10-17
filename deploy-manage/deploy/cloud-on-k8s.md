---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-overview.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-advanced-topics.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-supported.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_learn_more_about_eck.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# {{eck}} [k8s-overview]

Built on the Kubernetes Operator pattern, {{eck}} (ECK) extends the basic Kubernetes orchestration capabilities to support the setup and management of {{eck_resources_list}} on Kubernetes.

## ECK overview

With {{eck}}, you can streamline critical operations, such as:

1. Managing and monitoring multiple clusters
2. Scaling cluster capacity and storage
3. Performing safe configuration changes through rolling upgrades
4. Securing clusters with TLS certificates
5. Setting up hot-warm-cold architectures with availability zone awareness

This section provides everything you need to install, configure, and manage {{stack}} applications with ECK, including:

- [](./cloud-on-k8s/deploy-an-orchestrator.md): ECK installation methods and configuration options. Deploy ECK on managed Kubernetes platforms like GKE, AKS, and EKS, on self-managed Kubernetes clusters, on OpenShift, and even in air-gapped environments.
- [](./cloud-on-k8s/manage-deployments.md): Handle {{es}} clusters and {{kib}} instances through ECK.
- [](./cloud-on-k8s/orchestrate-other-elastic-applications.md): Run {{eck_resources_list_short}} on Kubernetes.
- [](./cloud-on-k8s/tools-apis.md): A collection of tools and APIs available in ECK based environments.

Other sections of the documentation include the following important topics around ECK:

- [Logging and Monitoring](../monitor.md): Configure stack monitoring and logs forwarding with the help of ECK.
- [Remote Clusters](../remote-clusters.md): Configure remote clusters on ECK.
- [](../tools.md): Add snapshot repositories to your {{es}} clusters for automatic snapshots.
- [Security](../security.md): Secure communications, manage HTTP certificates, or add secure settings to your applications.
- [Users and Roles](../users-roles.md): Configure authentication and authorization mechanisms, built-in users, external providers, and more.
- [Autoscaling](../autoscaling.md): Learn how to use {{es}} autoscaling on ECK, or use Horizontal Pod Autoscaler functionality for stateless workloads.
- [Licensing](../license/manage-your-license-in-eck.md): Manage licenses on ECK.

::::{important}
ECK is an Elastic self-managed product offered in two licensing tiers: Basic and Enterprise. For more details refer to [Elastic subscriptions](https://www.elastic.co/subscriptions) and [](/deploy-manage/license/manage-your-license-in-eck.md) documentation.
::::

## Quickstart [eck-quickstart]

If you want to get started quickly, follow these guides to deploy ECK and set up an {{es}} cluster:

* [Install ECK using YAML manifests](./cloud-on-k8s/install-using-yaml-manifest-quickstart.md)
* [Deploy an {{es}} cluster](./cloud-on-k8s/elasticsearch-deployment-quickstart.md)
* [Deploy a {{kib}} instance](./cloud-on-k8s/kibana-instance-quickstart.md)

Afterwards, you can:

* Learn how to [update your deployment](./cloud-on-k8s/update-deployments.md)
* Check out [our recipes](./cloud-on-k8s/recipes.md) for multiple use cases
* Find further sample resources [in the project repository](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/samples)

## Supported versions [k8s-supported]

This section outlines the supported Kubernetes and {{stack}} versions for ECK. Check the full [Elastic support matrix](https://www.elastic.co/support/matrix#matrix_kubernetes) for more information.

### Kubernetes compatibility

ECK is compatible with the following Kubernetes distributions and related technologies:

::::{tab-set}

:::{tab-item} ECK 3.2
* Kubernetes 1.30-1.34
* OpenShift 4.15-4.19
* Google Kubernetes Engine (GKE), Azure Kubernetes Service (AKS), and Amazon Elastic Kubernetes Service (EKS)
* Helm: {{eck_helm_minimum_version}}+
:::

:::{tab-item} ECK 3.1
* Kubernetes 1.29-1.33
* OpenShift 4.15-4.19
* Google Kubernetes Engine (GKE), Azure Kubernetes Service (AKS), and Amazon Elastic Kubernetes Service (EKS)
* Helm: {{eck_helm_minimum_version}}+
:::

:::{tab-item} ECK 3.0
* Kubernetes 1.28-1.32
* OpenShift 4.14-4.18
* Google Kubernetes Engine (GKE), Azure Kubernetes Service (AKS), and Amazon Elastic Kubernetes Service (EKS)
* Helm: {{eck_helm_minimum_version}}+
:::

::::

ECK should work with all conformant **installers** listed in these [FAQs](https://github.com/cncf/k8s-conformance/blob/master/faq.md#what-is-a-distribution-hosted-platform-and-an-installer). Distributions include source patches and so may not work as-is with ECK.

Alpha, beta, and stable API versions follow the same [conventions used by Kubernetes](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning).

### {{stack}} compatibility [stack-compatibility]

ECK is compatible with the following {{stack}} applications:

* {{es}}, {{kib}}, APM Server: 7.17+, 8+, 9+
* Enterprise Search: 7.17+, 8+
* Beats: 7.17+, 8+, 9+
* Elastic Agent: 7.10+ (standalone), 7.17+ (Fleet), 8+, 9+
* Elastic Maps Server: 7.17+, 8+, 9+
* Logstash: 8.7+, 9+

{{stack}} application images for the OpenShift-certified {{es}} (ECK) Operator are only available from version 7.10 and later.

## Learn more about ECK [k8s_learn_more_about_eck]

* [Orchestrate {{es}} on Kubernetes](https://www.elastic.co/elasticsearch-kubernetes)
* [ECK post on the Elastic Blog](https://www.elastic.co/blog/introducing-elastic-cloud-on-kubernetes-the-elasticsearch-operator-and-beyond?elektra=products&storm=sub1)
* [Getting Started With {{eck}} (ECK)](https://www.youtube.com/watch?v=PIJmlYBIFXM)
* [Running the {{stack}} on Kubernetes with ECK](https://www.youtube.com/watch?v=Wf6E3vkvEFM)
