---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-configure-settings.html
---

# Configure your deployment [ech-configure-settings]

You might want to change the configuration of your deployment to:

* Add features, such as machine learning or APM (application performance monitoring).
* Increase or decrease capacity by changing the amount of reserved memory and storage for different parts of your deployment.
* Enable [autoscaling](../../autoscaling.md) so that the available resources for deployment components, such as data tiers and machine learning nodes, adjust automatically as the demands on them change over time.
* Enable high availability by adjusting the number of availability zones that parts of your deployment run on.
* Upgrade to new versions of {{es}}. You can upgrade from one major version to another, such as from 7.17.27 to 8.17.1, or from one minor version to another, such as 8.6 to 8.7. You can’t downgrade versions.
* Change what plugins are available on your {{es}} cluster.

::::{note} 
During the free trial, {{ess}} deployments are restricted to a fixed size. You can resize your deployments when your trial is converted into a paid subscription.
::::


You can change the configuration of a running deployment from the **Configuration** pane in the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).

With the exception of major version upgrades for Elastic Stack products, Elasticsearch Add-On for Heroku can perform configuration changes without having to interrupt your deployment. You can continue searching and indexing. The changes can also be done in bulk. For example: in one action you can add more memory, upgrade, adjust the number of {{es}} plugins and adjust the number of availability zones.

We perform all of these changes by creating instances with the new configurations that join your existing deployment before removing the old ones. For example: if you are changing your {{es}} cluster configuration, we create new {{es}} nodes, recover your indexes, and start routing requests to the new nodes. Only when all new {{es}} nodes are ready, do we bring down the old ones.

By doing it this way, we reduce the risk of making configuration changes. If any of the new instances have a problems, the old ones are still there, processing requests.

::::{note} 
If you use a Platform-as-a-Service provider like Heroku, the administration console is slightly different and does not allow you to make changes that will affect the price. That must be done in the platform provider’s add-on system. You can still do things like change {{es}} version or plugins.
::::


To change the {{es}} cluster in your deployment:

1. Log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the deployments page, select your deployment.

    Narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, select **{{es}}** and then **Edit**.
4. Let the user interface guide you through the cluster configuration for your cluster. For a full list of the supported settings, check [What Deployment Settings Are Available?](ech-configure-deployment-settings.md)

    If you are changing an existing deployment, you can make multiple changes to your {{es}} cluster with a single configuration update, such as changing the capacity and upgrading to a new {{es}} version in one step.

5. Save your changes. The new configuration takes a few moments to create.

Review the changes to your configuration on the **Activity** page, with a tab for {{es}} and one for {{kib}}.



