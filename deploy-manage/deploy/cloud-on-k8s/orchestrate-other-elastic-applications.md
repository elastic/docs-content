# Orchestrate other Elastic applications

This section explains how to deploy and configure various Elastic Stack applications within Elastic Cloud on Kubernetes (ECK).

::::{tip}
This content applies to APM Server, Beats, Elastic Agent, Elastic Maps Server, and Logstash applications. To orchestrate an {{es}} cluster or {{kib}}, refer to [](./manage-deployments.md).
::::

The following guides provide specific instructions for deploying and configuring each application on ECK:
* [APM Server](apm-server.md)
* [Standalone Elastic Agent](standalone-elastic-agent.md)
* [{{fleet}}-managed {{agent}}](fleet-managed-elastic-agent.md)
* [Elastic Maps Server](elastic-maps-server.md)
* [Beats](beats.md)
* [{{ls}}](logstash.md)

When orchestrating any of these applications, also consider the following topics:

* [Elastic Stack Helm Chart](managing-deployments-using-helm-chart.md)
* [Recipes](recipes.md)
* [Secure the Elastic Stack](../../security.md)
* [Access Elastic Stack services](accessing-services.md)
* [Customize Pods](customize-pods.md)
* [Manage compute resources](manage-compute-resources.md)
* [Autoscaling stateless applications](../../autoscaling/autoscaling-stateless-applications-on-eck.md)
* [Elastic Stack configuration policies](elastic-stack-configuration-policies.md)
* [Upgrade the Elastic Stack version](../../upgrade/deployment-or-cluster.md)
* [Connect to external Elastic resources](connect-to-external-elastic-resources.md)