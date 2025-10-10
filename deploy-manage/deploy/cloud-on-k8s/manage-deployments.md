---
navigation_title: Manage deployments
applies_to:
  deployment:
    eck: all
---
# Manage deployments in {{eck}}

This section provides detailed guidance on deploying, configuring, and managing {{es}} and {{kib}} within ECK. A **deployment** refers to an {{es}} cluster, optionally with one or more {{kib}} instances connected to it.

::::{tip}
This content focuses on {{es}} and {{kib}} deployments. To orchestrate other {{stack}} applications such as {{eck_resources_list_short}}, refer to the [Orchestrating other {{stack}} applications](./orchestrate-other-elastic-applications.md).
::::

## What You'll Learn

In this section, you'll learn how to perform the following tasks in ECK:

- [**Deploy an {{es}} cluster**](./elasticsearch-deployment-quickstart.md): Orchestrate an {{es}} cluster in Kubernetes.
- [**Deploy {{kib}} instances**](./kibana-instance-quickstart.md): Set up and connect {{kib}} to an existing {{es}} cluster.
- [**Manage deployments using {{stack}} Helm chart**](./managing-deployments-using-helm-chart.md): Use Helm to deploy clusters and other stack applications.
- [**Apply updates to your deployments**](./update-deployments.md): Modify existing deployments, scale clusters, and update configurations, while ensuring minimal disruption.
- [**Configure access to your deployments**](./accessing-services.md): Use and adapt Kubernetes services to your needs.
- [**Advanced configuration**](./configure-deployments.md): Explore available settings for {{es}} and {{kib}}, including storage, networking, security, and scaling options.

For a complete reference on configuration possibilities for {{es}} and {{kib}}, see:

- [](./elasticsearch-configuration.md)
- [](./kibana-configuration.md)

Other references for managing deployments:

* [**Upgrade the {{stack}} version**](../../upgrade/deployment-or-cluster.md): Upgrade orchestrated applications on ECK.
