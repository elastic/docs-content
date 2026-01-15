# Orchestrate other Elastic applications

This section explains how to deploy and configure various {{stack}} applications within {{eck}} (ECK).

::::{tip}
This content applies to {{eck_resources_list_short}} applications. To orchestrate an {{es}} cluster or {{kib}}, refer to [](./manage-deployments.md).
::::

The following guides provide specific instructions for deploying and configuring each application on ECK:
* [APM Server](apm-server.md)
* [Standalone Elastic Agent](standalone-elastic-agent.md)
* [{{fleet}}-managed {{agent}}](fleet-managed-elastic-agent.md)
* [Elastic Maps Server](elastic-maps-server.md)
* [Beats](beats.md)
* [{{ls}}](logstash.md)
* ```{applies_to} deployment: eck: ga 3.3``` [{{package-registry}}](package-registry.md)

::::{note}
Enterprise Search is not available in {{stack}} versions 9.0 and later. To deploy or manage Enterprise Search in earlier versions, refer to the [previous ECK documentation](https://www.elastic.co/guide/en/cloud-on-k8s/2.16/k8s-enterprise-search.html).
::::

When orchestrating any of these applications, also consider the following topics:

* [{{stack}} Helm Chart](managing-deployments-using-helm-chart.md)
* [Recipes](recipes.md)
* [Secure the {{stack}}](../../security.md)
* [Access {{stack}} services](accessing-services.md)
* [Customize Pods](customize-pods.md)
* [Manage compute resources](manage-compute-resources.md)
* [Autoscaling stateless applications](../../autoscaling/autoscaling-in-eck.md#k8s-stateless-autoscaling)
* [{{stack}} configuration policies](elastic-stack-configuration-policies.md)
* [Upgrade the {{stack}} version](../../upgrade/deployment-or-cluster.md)
* [Connect to external Elastic resources](connect-to-external-elastic-resources.md)