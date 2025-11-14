---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-customize-deployment-components.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-customize-deployment-components.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Customize deployment components [ec-customize-deployment-components]

When you create or edit an existing deployment, you can fine-tune the capacity, add extensions, and select additional features.


## Autoscaling [ec-customize-autoscaling]

Autoscaling reduces some of the manual effort required to manage a deployment by adjusting the capacity as demands on the deployment change. Currently, autoscaling is supported to scale {{es}} data tiers upwards, and to scale machine learning nodes both upwards and downwards. Check [Deployment autoscaling](../../autoscaling.md) to learn more.


## {{es}} [ec-cluster-size]

Depending upon how much data you have and what queries you plan to run, you need to select a cluster size that fits your needs. There is no silver bullet for deciding how much memory you need other than simply testing it. The [cluster performance metrics](../../monitor/stack-monitoring.md) in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) can tell you if your cluster is sized appropriately. You can also [enable deployment monitoring](../../monitor/stack-monitoring/ece-ech-stack-monitoring.md) for more detailed performance metrics. Fortunately, you can change the amount of memory allocated to the cluster later without any downtime for HA deployments.

To change a cluster’s topology, from deployment management, select **Edit deployment** from the **Actions** dropdown. Next, select a storage and RAM setting from the **Size per zone** drop-down list, and save your changes. When downsizing the cluster, make sure to have enough resources to handle the current load, otherwise your cluster will be under stress.

:::{image} /deploy-manage/images/cloud-ec-capacity.png
:alt: Capacity slider to adjust {{es}} cluster size
:::

For trials, larger sizes are not available until you [add a credit card](../../cloud-organization/billing/add-billing-details.md).

For instances up to 64 GB of RAM, half the memory is assigned to the JVM heap (a bit less when monitoring is activated). For instances larger than 64 GB, the heap size is capped at 32 GB. For example, on a 32 GB instance, 16 GB are allotted to heap, while on a 128 GB instance, 32 GB are allotted to heap. Up to 256 GB RAM per instance is supported. The disk-to-RAM ratio currently is 1:24, meaning that you get 24 GB of storage space for each 1 GB of RAM. All clusters are backed by SSD drives.

::::{tip}
For production systems, each {{es}} instance in your cluster should have at least 4 GB of RAM, which assigns 2 GB to the JVM heap. Review [Minimum size recommendations for production use](elastic-cloud-hosted-planning.md#ec-minimum-recommendations) for more details.
::::


The CPU resources assigned to a cluster are relative to the size of your cluster, meaning that a 32 GB cluster gets twice as much CPU resources as a 16 GB cluster. All clusters are guaranteed their share of CPU resources, as we do not overcommit resources. Smaller clusters up to and including 8 GB of RAM benefit from temporary CPU boosting to improve performance when needed most.

If you don’t want to autoscale your deployment, you can manually increase or decrease capacity by adjusting the size of hot, warm, cold, and frozen [data tiers](../../../manage-data/lifecycle/data-tiers.md) nodes. For example, you might want to add warm tier nodes if you have time series data that is accessed less frequently and rarely needs to be updated. Alternatively, you might need cold tier nodes if you have time series data that is accessed occasionally and not normally updated. For clusters that have six or more {{es}} nodes, dedicated master-eligible nodes are introduced. When your cluster grows, it becomes important to consider separating dedicated master-eligible nodes from dedicated data nodes.

::::{tip}
For clusters with dedicated master nodes, we recommend using at least 4 GB of RAM for each dedicated master node. Review [Minimum size recommendations for production use](elastic-cloud-hosted-planning.md#ec-minimum-recommendations) for more details.
::::



## Fault tolerance [ec-high-availability]

High availability is achieved by running a cluster with replicas in multiple data centers (availability zones), to prevent against downtime when infrastructure problems occur or when resizing or upgrading deployments. We offer the options of running in one, two, or three data centers.

:::{image} /deploy-manage/images/cloud-ec-fault-tolerance.png
:alt: High availability features
:::

Running in two data centers or availability zones is our default high availability configuration. It provides reasonably high protection against infrastructure failures and intermittent network problems. You might want three data centers if you need even higher fault tolerance. Just one zone might be sufficient, if the cluster is mainly used for testing or development.

::::{important}
Some [regions](cloud://reference/cloud-hosted/regions.md) might have only two availability zones.
::::


Like many other changes, you change the level of fault tolerance while the cluster is running. For example, when you prepare a new cluster for production use, you can first run it in a single data center and then add another data center right before deploying to production.

While multiple data centers or availability zones increase a cluster’s fault tolerance, they do not protect against problematic searches that cause nodes to run out of memory. For a cluster to be highly reliable and available, it is also important to [have enough memory](../../../troubleshoot/monitoring/high-memory-pressure.md).

The node capacity you choose is per data center. The reason for this is that there is no point in having two data centers if the failure of one will result in a cascading error because the remaining data center cannot handle the total load. Through the allocation awareness in {{es}}, we configure the nodes so that your {{es}} cluster will automatically allocate replicas between each availability zone.


## Sharding [ec_sharding]

You can review your {{es}} shard activity from the {{ecloud}} Console. When viewing a hosted deployment details, at the bottom of the {{es}} page, you can hover over each part of the shard visualization for specific numbers.

:::{image} /deploy-manage/images/cloud-ec-shard-activity.gif
:alt: Shard activity
:::

We recommend that you read [Size your shards](../../production-guidance/optimize-performance/size-shards.md) before you change the number of shards.


## Manage user settings and extensions [ec_manage_user_settings_and_extensions]

Here, you can configure user settings, extensions, and system settings  (older versions only).


### User settings [ec-user-settings]

Set specific configuration parameters to change how {{es}} and other Elastic products run. User settings are appended to the appropriate YAML configuration file, but not all settings are supported in {{ech}} deployments.

For more information, refer to [Edit your user settings](edit-stack-settings.md).


### Extensions [ec_extensions]

Lists the official plugins available for your selected {{es}} version, as well as any custom plugins and user bundles with dictionaries or scripts.

When selecting a plugin from this list you get a version that has been tested with the chosen {{es}} version. The main difference between selecting a plugin from this list and uploading the same plugin as a custom extension is in who decides the version used. To learn more, check [*Add plugins and extensions*](add-plugins-extensions.md).

The reason we do not list the version chosen on this page is because we reserve the option to change it when necessary. That said, we will not force a cluster restart for a simple plugin upgrade unless there are severe issues with the current version. In most cases, plugin upgrades are applied lazily, in other words when something else forces a restart like you changing the plan or {{es}} runs out of memory.

::::{tip}
Only Gold and Platinum subscriptions have access to uploading custom plugins. All subscription levels, including Standard, can upload scripts and dictionaries.
::::



## {{kib}} [ec_kib]

A {{kib}} instance is created automatically as part of every deployment.

::::{tip}
If you use a version before 5.0 or if your deployment didn’t include a {{kib}} instance initially, there might not be a {{kib}} endpoint URL shown, yet. To enable {{kib}}, select **Enable**. Enabling {{kib}} provides you with an endpoint URL, where you can access {{kib}}. It can take a short while to provision {{kib}} right after you select **Enable**, so if you get an error message when you first access the endpoint URL, try again.
::::


Selecting **Open** will log you in to {{kib}} using single sign-on (SSO). For versions older than 7.9.2, you need to log in to {{kib}} with the `elastic` superuser. The password was provided when you created your deployment or [can be reset](../../users-roles/cluster-or-deployment-auth/built-in-users.md).

In production systems, you might need to control what {{es}} data users can access through {{kib}}. Refer to [Securing your deployment](../../users-roles/cluster-or-deployment-auth.md) to learn more.


## {{integrations-server}} [ec_integrations_server]

{{integrations-server}} connects observability and security data from Elastic Agents and APM to {{es}}. An {{integrations-server}} instance is created automatically as part of every deployment.

Refer to [Manage your Integrations Server](manage-integrations-server.md) to learn more.

## Security [ec_security]

Here, you can configure features that keep your deployment secure: reset the password for the `elastic` user, set up network security, and add settings to the {{es}} keystore. You can also set up remote connections to other deployments.


## Actions [ec_actions]

There are a few actions you can perform from the **Actions** dropdown:

* Edit the deployment
* Reset the `elastic` user password.
* Restart {{es}} - Needed only rarely, but full cluster restarts can help with a suspected operational issue before reaching out to Elastic for help.
* Delete your deployment - For deployment that you no longer need and don’t want to be charged for any longer. Deleting a deployment removes the {{es}} cluster and all your data permanently.

::::{important}
Use these actions with care. Deployments are not available while they restart and deleting a deployment does really remove the {{es}} cluster and all your data permanently.
::::


