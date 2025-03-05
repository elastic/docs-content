---
applies_to:
  deployment:
    ess: ga
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-customize-deployment.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-configure-settings.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-configure.html
---

# Configure

You might want to change the configuration of your deployment to:

* Add features, such as machine learning or APM (application performance monitoring).
* Increase or decrease capacity by changing the amount of reserved memory and storage for different parts of your deployment.

    ::::{note} 
    During the free trial, {{ech}} deployments are restricted to a limited size. You can increase the size of your deployments when your trial is converted to a paid subscription.
    ::::

* Enable [autoscaling](../../../deploy-manage/autoscaling.md) so that the available resources for deployment components, such as data tiers and machine learning nodes, adjust automatically as the demands on them change over time.
* Enable high availability, also known as fault tolerance, by adjusting the number of data center availability zones that parts of your deployment run on.
* Upgrade to new versions of {{es}}. You can upgrade from one major version to another, such as from 6.8.23 to 7.17.27, or from one minor version to another, such as 6.1 to 6.2. You can’t downgrade versions.
* Change what plugins are available on your {{es}} cluster.

With the exception of major version upgrades for Elastic Stack products, {{ech}} can perform configuration changes without having to interrupt your deployment. You can continue searching and indexing. The changes can also be done in bulk. For example: in one action, you can add more memory, upgrade, adjust the number of {{es}} plugins and adjust the number of availability zones.

We perform all of these changes by creating instances with the new configurations that join your existing deployment before removing the old ones. For example: if you are changing your {{es}} cluster configuration, we create new {{es}} nodes, recover your indexes, and start routing requests to the new nodes. Only when all new {{es}} nodes are ready, do we bring down the old ones.

By doing it this way, we reduce the risk of making configuration changes. If any of the new instances have a problems, the old ones are still there, processing requests.

::::{note} 
If you use a Platform-as-a-Service provider like Heroku, the administration console is slightly different and does not allow you to make changes that will affect the price. That must be done in the platform provider’s add-on system. You can still do things like change {{es}} version or plugins.
::::


To change your deployment:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From the deployment menu, select **Edit**.
4. Let the user interface guide you through the cluster configuration for your cluster.

    If you are changing an existing deployment, you can make multiple changes to your {{es}} cluster with a single configuration update, such as changing the capacity and upgrading to a new {{es}} version in one step.

5. Save your changes. The new configuration takes a few moments to create.

Review the changes to your configuration on the **Activity** page, with a tab for {{es}} and one for {{kib}}.

::::{tip} 
If you are creating a new deployment, select **Edit settings** to change the cloud provider, region, hardware profile, and stack version; or select **Advanced settings** for more complex configuration settings.
::::


That’s it! If you haven’t already, [start exploring with {{kib}}](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md), our visualization tool. If you’re not familiar with adding data yet, {{kib}} can show you how to index your data into {{es}}, or try our basic steps for working with [{{es}}](../../../manage-data/data-store/manage-data-from-the-command-line.md).

::::{tip} 
Some features are not available during the 14-day free trial. If a feature is greyed out, [add a credit card](../../../deploy-manage/cloud-organization/billing/add-billing-details.md) to unlock the feature.
::::
