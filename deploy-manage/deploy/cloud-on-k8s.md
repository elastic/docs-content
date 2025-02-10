---
applies:
  eck: all
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-overview.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-advanced-topics.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-supported.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_learn_more_about_eck.html
---

# Elastic Cloud on Kubernetes [k8s-overview]

::::{important}
ECK is an Elastic self-managed product offered in two licensing tiers: Basic and Enterprise. For more details refer to [Elastic subscriptions](https://www.elastic.co/subscriptions) and [](/deploy-manage/license/manage-your-license-in-eck.md) documentation.
::::

Built on the Kubernetes Operator pattern, Elastic Cloud on Kubernetes (ECK) extends the basic Kubernetes orchestration capabilities to support the setup and management of Elasticsearch, Kibana, APM Server, Enterprise Search, Beats, Elastic Agent, Elastic Maps Server, and Logstash on Kubernetes.

With Elastic Cloud on Kubernetes you can streamline critical operations, such as:

1. Managing and monitoring multiple clusters
2. Scaling cluster capacity and storage
3. Performing safe configuration changes through rolling upgrades
4. Securing clusters with TLS certificates
5. Setting up hot-warm-cold architectures with availability zone awareness

This section provides everything you need to install, configure, and manage Elastic Stack applications with ECK, including:

- [](./cloud-on-k8s/deploy-an-orchestrator.md): ECK installation methods and configuration details.
- [](./cloud-on-k8s/manage-deployments.md): Install and configure {{es}} clusters and {{kib}} instances through ECK.
- [](./cloud-on-k8s/orchestrate-other-elastic-applications.md): Install and configure APM Server, Enterprise Search, Beats, Elastic Agent, Elastic Maps Server, and Logstash on Kubernetes.
- [](./cloud-on-k8s/tools-apis.md): Collection of tools and APIs available in ECK based environments.

## Looking for a quickstart? [eck-quickstart]

If you want to get started quickly, follow these guides to deploy ECK and set up an {{es}} cluster:

* [Install ECK using the YAML manifests](./cloud-on-k8s/install-using-yaml-manifest-quickstart.md)
* [Deploy an {{es}} cluster](./cloud-on-k8s/elasticsearch-deployment-quickstart.md)
* [Deploy a {{kib}} instance](./cloud-on-k8s/kibana-instance-quickstart.md)
* [Update your deployment](./cloud-on-k8s/update-deployments.md)

Afterwards, you can find further sample resources [in the project repository](https://github.com/elastic/cloud-on-k8s/tree/2.16/config/samples) or by checking out [our recipes](./cloud-on-k8s/recipes.md).

## Supported versions [k8s-supported]

ECK is compatible with:

* Kubernetes 1.28-1.32
* OpenShift 4.12-4.17
* Google Kubernetes Engine (GKE), Azure Kubernetes Service (AKS), and Amazon Elastic Kubernetes Service (EKS)
* Helm: 3.2.0+
* Elasticsearch, Kibana, APM Server: 6.8+, 7.1+, 8+
* Enterprise Search: 7.7+, 8+
* Beats: 7.0+, 8+
* Elastic Agent: 7.10+ (standalone), 7.14+ (Fleet), 8+
* Elastic Maps Server: 7.11+, 8+
* Logstash: 8.7+

ECK should work with all conformant installers as listed in these [FAQs](https://github.com/cncf/k8s-conformance/blob/master/faq.md#what-is-a-distribution-hosted-platform-and-an-installer). Distributions include source patches and so may not work as-is with ECK.

Alpha, beta, and stable API versions follow the same [conventions used by Kubernetes](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning).

Elastic Stack application images for the OpenShift-certified Elasticsearch (ECK) Operator are only available from version 7.10 and later.

Check the full [Elastic support matrix](https://www.elastic.co/support/matrix#matrix_kubernetes) for more information.

## Common tasks

* [Deploy and configure ECK](./cloud-on-k8s/deploy-an-orchestrator.md)
* [Manage {{es}} and {{kib}} deployments](./cloud-on-k8s/manage-deployments.md)
* [Orchestrate other Elastic Stack applications](./cloud-on-k8s/orchestrate-other-elastic-applications.md)

% to consider in either deploy or manage deployment sections
% this was a "redirect only" in the excel
## Advanced topics [k8s-advanced-topics]

* [*Deploy ECK on OpenShift*](/deploy-manage/deploy/cloud-on-k8s/deploy-eck-on-openshift.md)
* [*Deploy ECK on GKE Autopilot*](/deploy-manage/deploy/cloud-on-k8s/deploy-eck-on-gke-autopilot.md)
* [*Create custom images*](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md)
* [*Service meshes*](/deploy-manage/deploy/cloud-on-k8s/service-meshes.md)
* [*Traffic Splitting*](/deploy-manage/deploy/cloud-on-k8s/requests-routing-to-elasticsearch-nodes.md)
* [*Network policies*](/deploy-manage/deploy/cloud-on-k8s/network-policies.md)
* [*Webhook namespace selectors*](/deploy-manage/deploy/cloud-on-k8s/webhook-namespace-selectors.md)
* [*Stack Monitoring*](/deploy-manage/monitor/stack-monitoring/eck-stack-monitoring.md)
* [*Deploy a FIPS compatible version of ECK*](/deploy-manage/deploy/cloud-on-k8s/deploy-fips-compatible-version-of-eck.md)

% TBD: discuss if these make sense here
## Learn more about ECK [k8s_learn_more_about_eck]

* [Orchestrate Elasticsearch on Kubernetes](https://www.elastic.co/elasticsearch-kubernetes)
* [ECK post on the Elastic Blog](https://www.elastic.co/blog/introducing-elastic-cloud-on-kubernetes-the-elasticsearch-operator-and-beyond?elektra=products&storm=sub1)
* [Getting Started With Elastic Cloud on Kubernetes (ECK)](https://www.youtube.com/watch?v=PIJmlYBIFXM)
* [Running the Elastic Stack on Kubernetes with ECK](https://www.youtube.com/watch?v=Wf6E3vkvEFM)

% TBD: discuss where to put this "ask for help info"

## Ask for help [k8s-ask-for-help]

If you are an existing Elastic customer with an active support contract, you can create a case in the [Elastic Support Portal](https://support.elastic.co/). Kindly attach an [ECK diagnostic](/troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md) when opening your case.

Alternatively, or if you do not have a support contract, and if you are unable to find a solution to your problem with the information provided in these documents, ask for help:

* [ECK Discuss forums](https://discuss.elastic.co/c/eck) to ask any question
* [Github issues](https://github.com/elastic/cloud-on-k8s/issues) for bugs and feature requests
