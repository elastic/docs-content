---
navigation_title: Manage deployments
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-stack-getting-started.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-deployments.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-monitoring-deployments.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

% document scope: This doc focuses on everything that can be achieved from the deployment UI
% TBD: include a link to a doc to manage deployments through ECE API. Same for Deploy an orchestrator section (ECE API links are still pending because we still haven't published the reference docs)

# Manage deployments in {{ece}} [ece-stack-getting-started]

{{ece}} allows you to manage one or more instances of the {{stack}} through **deployments**.


A *deployment* helps you manage an {{es}} cluster and instances of other Elastic products, like {{kib}} or APM, in one place. Spin up, scale, upgrade, and delete your {{stack}} products without having to manage each one separately. In a deployment, everything works together.

ECE provides a preset of *hardware profiles* that provide a unique blend of storage, memory and vCPU for each component of a deployment. They support a specific purpose, such as a hot-warm architecture, that helps you manage your data storage retention.

All of these profiles are based on [deployment templates](./deployment-templates.md), which are a reusable configuration of Elastic products that you can deploy. You can modify existing deployment templates, or create custom deployment templates, to suit your needs.

## Creating deployments

Refer to [Create a deployment](./create-deployment.md) to launch and configure an {{stack}} environment.

## Administering deployments [ece-administering-deployments]

Maintaining your existing deployments is important. Take a look at the things you can do to keep your deployments and the {{stack}} running smoothly.

Deployments in ECE are managed from the **Deployment** view of the [Cloud UI](./log-into-cloud-ui.md). This section focuses on the different actions you can take from this view.

### Configuration and features

From the deployment main page, you can quickly access the following configuration areas:

* Select **Edit** to change the deployment configuration, its components and data tiers. Refer to [](./customize-deployment.md) for more details.

* Set a [Custom endpoint alias](./ece-regional-deployment-aliases.md) to create human-readable URLs for your {{stack}} applications, making them easier to share and use.

* [Upgrade your deployment](../../upgrade/deployment-or-cluster/upgrade-on-ece.md) if a newer {{stack}} version is available.

* Select **{{es}} > snapshots** to associate a [snapshots repository](../../tools/snapshot-and-restore/cloud-enterprise.md#ece-manage-repositories-clusters) with the deployment.

* Select **Monitoring > Logs and metrics** to set up [Stack monitoring](../../monitor/stack-monitoring/ece-ech-stack-monitoring.md) for your deployment, forwarding its logs and metrics to a dedicated monitoring deployment.

  ::::{note}
  In addition to the monitoring of clusters that is described here, don’t forget that {{ece}} also provides [monitoring information for your entire installation](../../../deploy-manage/monitor/orchestrators/ece-platform-monitoring.md).
  ::::

### Security and access control

From the **Deployment > Security** view, you can manage security settings, authentication, and access controls. Refer to [Secure your clusters](../../../deploy-manage/users-roles/cluster-or-deployment-auth.md) for more details on security options for your deployments.

* [Reset the `elastic` user password](../../users-roles/cluster-or-deployment-auth/manage-elastic-user-cloud.md)
* [Set up IP filters](../../security/ip-filtering-ece.md) to restrict traffic to your deployment
* Configure {{es}} keystore settings, also known as [secure settings](../../security/secure-settings.md)
* Configure trust relationships for [remote clusters](../../remote-clusters/ece-enable-ccs.md)

### Endpoints, monitoring, and troubleshooting

From the deployment view, you can directly access endpoints, platform logs and metrics, and troubleshoot issues using various built-in tools.

* Select **Copy endpoint** links to obtain the different URLs to [](./connect-elasticsearch.md) and [](./access-kibana.md).

* If your deployment includes an integrations server, open the **Integrations server** page to get direct access to APM and Fleet. Refer to [](./manage-integrations-server.md) for more information.

* For {{es}}, {{kib}}, and Integrations Server components, use the **External links** to access each service's logs and metrics, including the associated proxy logs. These logs are part of [](../../../deploy-manage/monitor/orchestrators/ece-platform-monitoring.md), and are separate from user-configured stack monitoring.

* Use the [{{es}} API console](./tools-apis.md#ece-api-console) to send API calls directly to {{es}}.

* [Keep track of your deployment activity](./keep-track-of-deployment-activity.md) and get information about configuration changes results and failures.

* Open the **Operations** page to generate and download diagnostics bundles for {{es}} and {{kib}}, and to access other [tools](./tools-apis.md).

### Operational actions

Use the **Actions** button at deployment or instance level to:

* [Restart a deployment](../../../deploy-manage/maintenance/start-stop-services/restart-an-ece-deployment.md) that has become unresponsive, for example.
* [Terminate a deployment](../../../deploy-manage/uninstall/delete-a-cloud-deployment.md) to stop all running instances and delete all data in the deployment.
* [Restore a deployment](../../../deploy-manage/uninstall/delete-a-cloud-deployment.md#restore-a-deployment) that had been terminated.
* [Delete a deployment](../../../deploy-manage/uninstall/delete-a-cloud-deployment.md) if you no longer need it.
* [Override instance resources](./resource-overrides.md) when needed to stabilize your deployment.
* [Stop routing requests or pause deployment instances](../../../deploy-manage/maintenance/ece/deployments-maintenance.md) to perform corrective actions that might otherwise be difficult to complete.

## Keeping your clusters healthy [ece-monitoring-deployments]

{{ece}} monitors many aspects of your installation, but some issues require a human to resolve them. Use this section to learn how you can:

* [Find clusters](/troubleshoot/deployments/cloud-enterprise/cloud-enterprise.md) that have issues.
* [Move affected instances off an allocator](../../../deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md), if the allocator fails.
