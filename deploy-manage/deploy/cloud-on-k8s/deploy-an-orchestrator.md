---
applies:
  eck: all
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-quickstart.html
---

% Similar to ECE section, write an introduction about the installation methods and include links to the other sections (AIR GAPPED and Configure).
% The page has been provided as it already provides a good introduction.

# Deploy an orchestrator [k8s-quickstart]

With Elastic Cloud on Kubernetes (ECK) you can extend the basic Kubernetes orchestration capabilities to easily deploy, secure, upgrade your {{es}} cluster, along with other Elastic applications.

This section provides step-by-step guidance on:

- [**Installing the ECK Operator**](./install.md) → Learn different installation methods, including Helm and YAML manifests.
- [**Deploying in air-gapped environments**](./air-gapped-install.md) → Follow best practices for installing and operating ECK in restricted networks.
- [**Configuring ECK**](./configure.md) → Understand the available configuration options to optimize your ECK deployment.

::::{tip}
If you're looking to deploy {{es}}, {{kib}}, or other Elastic applications using ECK, refer to [](./manage-deployments.md).
::::

## Looking for a quickstart?

If you want to get started quickly, follow these guides to deploy ECK and set up an {{es}} cluster:

* [Install ECK using the YAML manifests](install-using-yaml-manifest-quickstart.md)
* [Deploy an {{es}} cluster](elasticsearch-deployment-quickstart.md)
* [Deploy a {{kib}} instance](kibana-instance-quickstart.md)
* [Update your deployment](update-deployments.md)

Afterwards, you can find further sample resources [in the project repository](https://github.com/elastic/cloud-on-k8s/tree/2.16/config/samples) or by checking out [our recipes](recipes.md).