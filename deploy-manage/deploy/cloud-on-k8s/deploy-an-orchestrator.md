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

If you're looking to deploy {{es}}, {{kib}}, or other Elastic applications using ECK, refer to [](./manage-deployments.md).

::::{tip}
For a quickstart experience covering the ECK installation, and an {{es}} cluster with a {{kib}} instance, refer to [](../cloud-on-k8s.md#eck-quickstart)
::::