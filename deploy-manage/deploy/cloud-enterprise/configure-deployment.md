---
navigation_title: Configure
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-change-deployment.html
---

% document scope: introduction to deployment configuration use cases

# Configure your deployment [ece-change-deployment]

You can modify your deployment to adjust resources, enable additional features, or optimize performance. To make sure you’re all set for production, consider the following actions: 

* [](./customize-deployment.md): Learn how to change your deployment architecture, configure resources, autoscaling, data tiers, and other {{stack}} components, from the **Edit** deployment view.
* [](./edit-stack-settings.md): Add, remove, or update {{es}} or {{kib}} YML configuration settings.
* [](./resize-deployment.md): Learn how to scale a deployment, including important considerations, and a practical example.
* [](./add-plugins.md): Enable or disable plugins from the list of available extensions in ECE.
* [](./add-custom-bundles-plugins.md): Add custom plugins or external configuration files to your {{es}} instances.
* [](./ece-regional-deployment-aliases.md): Configure custom aliases to create predictable and human-readable URLs for your {{stack}} components, making them easier to share and use.
* [](./resource-overrides.md): Temporary extend cluster capacity to improve stability.

Refer to [](./working-with-deployments.md) for additional actions and configurable features for your deployments, such as snapshots, secure settings, and monitoring.

## When to modify your deployment [ece-prepare-production]

You might want to change the configuration of your deployment to:

* Add features, such as [machine learning](/explore-analyze/machine-learning.md) or [APM (application performance monitoring)](/solutions/observability/apps/application-performance-monitoring-apm.md).
* [Increase or decrease capacity](./resize-deployment.md) by changing the amount of reserved memory and storage for different parts of your deployment.
* Enable [autoscaling](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md) so that the available resources for deployment components, such as [data tiers](/manage-data/lifecycle/data-tiers.md) and machine learning nodes, adjust automatically as the demands on them change over time.
* Enable [high availability](./ece-ha.md), also known as fault tolerance, by adjusting the number of availability zones that parts of your deployment run on.
* [Upgrade](../../upgrade/deployment-or-cluster/upgrade-on-ece.md) to new versions of {{es}}. You can upgrade from one major version to another, such as from 8.18 to 9.0, or from one minor version to another, such as 8.16 to 8.17. You can’t downgrade versions.
* Change what plugins are available on your deployment.
* Update {{es}}, {{kib}}, or other stack application YML configuration settings.

## Applying deployment changes

When you modify a deployment and select **Save changes**, {{ece}} prepares and executes a **plan** to apply the requested updates and bring the deployment to the desired state. The type of plan depends on the nature of the changes and the selected [configuration strategy](./customize-deployment.md#configuration-strategies). Some plans involve creating new instances and migrating data, while others may require restarting certain components of the deployment.

For single availability zone deployments, there is downtime to portions of your cluster when changes are applied. For [high availability](./ece-ha.md) deployments, with the exception of major version upgrades, we these changes can be made without interrupting your deployment. While these changes are being applied, you can continue to search and index.

::::{note}
When applying changes, existing data may be migrated to new nodes. For clusters containing large amounts of data, this migration can take some time, especially if your deployment is under a heavy workload. Refer to [Configuration strategies](./customize-deployment.md#configuration-strategies) to learn about the different ways ECE applies changes.
::::
