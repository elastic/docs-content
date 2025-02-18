---
applies:
  eck: all
---
# Manage deployments

This section provides detailed guidance on deploying, configuring, and managing Elasticsearch and Kibana within ECK. A **deployment** refers to an {{es}} cluster, optionally with one or more {{kib}} instances connected to it.

::::{tip}
This content focuses on Elasticsearch and Kibana deployments. To orchestrate other Elastic Stack applications such as APM Server, Beats, Elastic Agent, Elastic Maps Server, and Logstash, refer to the [Orchestrating other Elastic Stack applications](./orchestrate-other-elastic-applications.md).
::::

## What You'll Learn

In this section, you'll learn how to perform the following tasks in ECK:

- [**Deploy an Elasticsearch cluster**](./elasticsearch-deployment-quickstart.md): Orchestrate an {{es}} cluster in Kubernetes.
- [**Deploy Kibana instances**](./kibana-instance-quickstart.md): Set up and connect Kibana to an existing Elasticsearch cluster.
- [**Manage deployments using Elastic Stack Helm chart**](./managing-deployments-using-helm-chart.md): Use Helm to deploy clusters and other stack applications.
- [**Apply updates to your deployments**](./update-deployments.md): Modify existing deployments, scale clusters, and update configurations, while ensuring minimal disruption.
- [**Configure access to your deployments**](./accessing-services.md): Use and adapt Kubernetes services to your needs.
- [**Advanced configuration**](./configure-deployments.md): Explore available settings for Elasticsearch and Kibana, including storage, networking, security, and scaling options.

For a complete reference on configuration possibilities for {{es}} and {{kib}}, see:

- [](./elasticsearch-configuration.md)
- [](./kibana-configuration.md)

Other references for managing deployments:

* [**Upgrade the Elastic Stack version**](../../upgrade/deployment-or-cluster.md): Upgrade orchestrated applications on ECK.
