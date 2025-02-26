# Introducing {{ech}} [ec-getting-started]

::::{note}
Are you just discovering Elastic or are unfamiliar with the core concepts of the Elastic Stack? Would you like to be guided through the very first steps and understand how Elastic can help you? Try one of our [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html) first.
::::



## What is {{ech}}? [ec_what_is_elasticsearch_service]

**The Elastic Stack, managed through {{ecloud}} deployments.**

{{ech}} allows you to manage one or more instances of the Elastic Stack through **deployments**. These deployments are hosted on {{ecloud}}, through the cloud provider and regions of your choice, and are tied to your organization account.

A *deployment* helps you manage an Elasticsearch cluster and instances of other Elastic products, like Kibana or APM instances, in one place. Spin up, scale, upgrade, and delete your Elastic Stack products without having to manage each one separately. In a deployment, everything works together.

::::{note}
If you are instead interested in serverless Elastic Cloud, check the [serverless documentation](https://docs.elastic.co/serverless).
::::


**Hardware profiles to optimize deployments for your usage.**

You can optimize the configuration and performance of a deployment by selecting a **hardware profile** that matches your usage.

*Hardware profiles* are presets that provide a unique blend of storage, memory and vCPU for each component of a deployment. They support a specific purpose, such as a hot-warm architecture that helps you manage your data storage retention.

You can use these presets, or start from them to get the unique configuration you need. They can vary slightly from one cloud provider or region to another to align with the available virtual hardware.

**Solutions to help you make the most out of your data in each deployment.**

Building a rich search experience, gaining actionable insight into your environment, or protecting your systems and endpoints? You can implement each of these major use cases, and more, with the solutions that are pre-built in each Elastic deployment.

:::{image} ../../../images/cloud-ec-stack-components.png
:alt: Elastic Stack components and solutions with Enterprise Search
:::

:::{important}
Enterprise Search is not available in {{stack}} 9.0+.
:::

These solutions help you accomplish your use cases: Ingest data into the deployment and set up specific capabilities of the Elastic Stack.

Of course, you can choose to follow your own path and use Elastic components available in your deployment to ingest, visualize, and analyze your data independently from solutions.


## How to operate {{ech}}? [ec_how_to_operate_elasticsearch_service]

**Where to start?**

* Try one of our solutions by following our [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html).
* Sign up using your preferred method:

    * [Sign Up for a Trial](../../../deploy-manage/deploy/elastic-cloud/create-an-organization.md) - Sign up, check what your free trial includes and when we require a credit card.
    * [Sign Up from Marketplace](../../../deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md) - Consolidate billing portals by signing up through one of the available marketplaces.

* Set up your account by [completing your user or organization profile](../../../deploy-manage/cloud-organization/billing.md) and by [inviting users to your organization](../../../deploy-manage/cloud-organization.md).
* [Create a deployment](../../../deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md) - Get up and running very quickly. Select your desired configuration and let Elastic deploy Elasticsearch, Kibana, and the Elastic products that you need for you. In a deployment, everything works together, everything runs on hardware that is optimized for your use case.
* [Connect your data to your deployment](../../../manage-data/ingest.md) - Ingest and index the data you want, from a variety of sources, and take action on it.

**Adjust the capacity and capabilities of your deployments for production**

There are a few things that can help you make sure that your production deployments remain available, healthy, and ready to handle your data in a scalable way over time, with the expected level of performance. We’ve listed these things for you in [Preparing for production](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md).

**Secure your environment**

Control which users and services can access your deployments by [securing your environment](../../../deploy-manage/users-roles/cluster-or-deployment-auth.md). Add authentication mechanisms, configure [traffic filtering](../../../deploy-manage/security/traffic-filtering.md) for private link, encrypt your deployment data and snapshots at rest [with your own key](../../../deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md), manage trust with Elasticsearch clusters from other environments, and more.

**Monitor your deployments and keep them healthy**

{{ech}} provides several ways to monitor your deployments, anticipate and prevent issues, or fix them when they occur. Check [Monitoring your deployment](../../../deploy-manage/monitor/stack-monitoring.md) to get more details.

**And then?**

Now is the time for you to work with your data. The content of the {{ecloud}} section helps you get your environment up and ready to handle your data the way you need. You can always adjust your deployments and their configuration as your usage evolves over time.

To get the most out of the solutions that the Elastic Stack offers, [log in to {{ecloud}}](https://cloud.elastic.co) or [browse the documentation](https://www.elastic.co/docs).
